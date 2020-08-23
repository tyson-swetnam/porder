from __future__ import print_function

__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"


import requests
import json
import time
import clipboard
import sys
from datetime import date
from planet.api.auth import find_api_key

# Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print("Failed to get Planet Key")
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, "")

base_payload = {
    "name": [],
    "order_type": "partial",
    "products": [],
    "tools": [],
    "delivery": {},
}

order_url = "https://api.planet.com/compute/ops/orders/v2"

idlist = []


def reorder(url, notification):
    submitted_order = SESSION.get(url)
    if submitted_order.status_code == 200 and (
        submitted_order.json()["state"] == "partial"
        or submitted_order.json()["state"] == "success"
    ):
        payload = submitted_order.json()
        for files in payload["_links"]["results"]:
            if files["name"].endswith("manifest.json"):
                time.sleep(0.2)
                resp = SESSION.get(files["location"]).json()
                for items in resp["files"]:
                    if items["path"].endswith(".tif"):
                        idlist.append(items["annotations"]["planet/item_id"])
        for items in payload["products"]:
            if not len(list(set(items["item_ids"]) - set(idlist))) == 0:
                items["item_ids"] = list(set(items["item_ids"]) - set(idlist))
                print(
                    "Submitting a total of {} items".format(
                        len(list(set(items["item_ids"]) - set(idlist)))
                    ),
                    end="\r",
                )
            else:
                print(
                    "All items were delivered successfully resubmitting complete order",
                    end="\r",
                )
                items["item_ids"] = list(set(items["item_ids"]))

        print("")
        run_complete = input("Proceed with complete reorder: y/n ")
        if run_complete == "y":
            pass
        else:
            sys.exit("Exiting application now")
        if notification is not None and notification == "email":
            base_payload.update({"notifications": {"email": True}})
        today = date.today()
        base_payload["name"] = payload["name"].replace(
            payload["name"], payload["name"] + "-resubmit-" + str(today)
        )
        base_payload["products"] = payload["products"]
        if "tools" in payload:
            base_payload["tools"] = payload["tools"]
        else:
            base_payload.pop("tools", None)
        if "delivery" in payload:
            base_payload["delivery"] = payload["delivery"]
        if "notifications" in payload:
            base_payload["notifications"] = payload["notifications"]
        payload_final = json.dumps(base_payload)
        time.sleep(1)
        headers = {"content-type": "application/json", "cache-control": "no-cache"}
        response = SESSION.post(order_url, data=payload_final, headers=headers)
        if response.status_code == 202:
            content = response.json()
            try:
                clipboard.copy(str(order_url) + "/" + str(content["id"]))
                print(
                    "Order created at "
                    + str(order_url)
                    + "/"
                    + str(content["id"] + " and url copied to clipboard")
                )
                return str(order_url) + "/" + str(content["id"])
            except Exception:
                print(
                    "Headless Setup: Order created at "
                    + str(order_url)
                    + "/"
                    + str(content["id"])
                )
        elif response.status_code == 400:
            print("Failed with response: Bad request")
            print(response.json()["general"][0]["message"])
        elif response.status_code == 401:
            print("Failed with response: Forbidden")
        elif response.status_code == 409:
            print("Failed with response: MaxConcurrency")
        else:
            print(response.text)
    else:
        print("Order has status: {}".format(submitted_order.json()["state"]))


# reorder(url='https://api.planet.com/compute/ops/orders/v2/65295800-5ca8-4560-acba-11b2e8cb7f1a',notification='email')
