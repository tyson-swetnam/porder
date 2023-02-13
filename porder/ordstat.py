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

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime

import jwt
import requests
from datetimerange import DateTimeRange
from prettytable import PrettyTable

x = PrettyTable()


def authenticate_session():
    try:
        if not os.path.exists(os.path.join(expanduser("~"), "planet.auth.json")):
            init()
        else:
            with open(os.path.join(expanduser("~"), "planet.auth.json")) as json_file:
                token_data = json.load(json_file)
                encoded = token_data["token"]
                api_key = jwt.decode(encoded, options={"verify_signature": False})[
                    'api_key']
        PL_API_KEY = api_key
    except:
        print("Failed to get Planet Key")
        sys.exit()
    SESSION = requests.Session()
    SESSION.auth = (PL_API_KEY, "")
    return SESSION


def handle_page(page, start, end):
    for things in page["orders"]:
        s = datetime.strptime(things["created_on"].split("T")[0], "%Y-%m-%d")
        if s in DateTimeRange(start, end):
            try:
                x.field_names = ["name", "items", "url", "created_on"]
                x.add_row(
                    [
                        things["name"],
                        len(things["products"][0]["item_ids"]),
                        things["_links"]["_self"],
                        things["created_on"].split("T")[0],
                    ]
                )
            except Exception as e:
                print(e)


def ostat(state, start, end, limit):
    SESSION = authenticate_session()
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    mpage = "https://api.planet.com/compute/ops/orders/v2?state=" + str(state)
    result = SESSION.get(mpage)
    if result.status_code == 200:
        page = result.json()
        final_list = handle_page(page, start, end)
        while page["_links"].get("next") is not None:
            page_url = page["_links"].get("next")
            result = SESSION.get(page_url)
            if result.status_code == 200:
                page = result.json()
                ids = handle_page(page, start, end)
            elif result.status_code == 429:
                time.sleep(1)
                result = SESSION.get(page_url)
                page = result.json()
                ids = handle_page(page, start, end)
            else:
                print(result.status_code)
    if limit is not None:
        print(x.get_string(start=0, end=int(limit)))
    else:
        print(x)


# idl(state="success", start="2019-08-02", end="2019-08-02")
