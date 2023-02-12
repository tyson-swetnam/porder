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

import csv
import json
import sys
from datetime import date

import clipboard
import requests
import visvalingamwyatt as vw
import yaml
from planet.api.auth import find_api_key
from planet.api.utils import read_planet_json
from prettytable import PrettyTable

x = PrettyTable()

ovall = []

# get coordinates list depth


def list_depth(dic, level=1):
    counter = 0
    str_dic = str(dic)
    if "[[[[[" in str_dic:
        counter += 2
    elif "[[[[" in str_dic:
        counter += 1
    elif "[[[" in str_dic:
        counter += 0
    return counter


# Setup for bundles
dbundle = {
    "name": [],
    "subscription_id": [],
    "order_type": "partial",
    "products": [{"item_ids": [], "item_type": [], "product_bundle": []}],
    "tools": [],
    "delivery": {},
}
dclip = {"clip": {"aoi": {"type": "MultiPolygon", "coordinates": []}}}
dtoar = {"toar": {"scale_factor": 10000}}
dzip = {"delivery": {"archive_filename": "{{name}}.zip", "archive_type": "zip"}}
dcoreg = {"coregister": {"anchor_item": []}}
dformat = {"file_format": {"format": []}}
dcomposite = {"composite": {}}
dharmonize = {"harmonize": {"target_sensor": "PS2"}}
dreproject = {"reproject": {"projection": [], "kernel": []}}
dtiff = {"tiff_optimize": {"compression": []}}
demail = {"notifications": {"email": True}}
daws = {
    "delivery": {
        "amazon_s3": {
            "bucket": [],
            "aws_region": [],
            "aws_access_key_id": [],
            "aws_secret_access_key": [],
            "path_prefix": [],
        }
    }
}
dazure = {
    "delivery": {
        "azure_blob_storage": {
            "account": [],
            "container": [],
            "sas_token": [],
            "storage_endpoint_suffix": [],
            "path_prefix": [],
        }
    }
}
dgcs = {
    "delivery": {
        "google_cloud_storage": {"bucket": [], "credentials": [], "path_prefix": []}
    }
}
dgee = {
    "delivery": {
        "google_earth_engine": {
            "project": [],
            "collection": []
        }
    }
}

dbmath = {"bandmath": {}}
dszip = {
    "delivery": {
        "archive_filename": "{{name}}_{{order_id}}.zip",
        "archive_type": "zip",
        "single_archive": True,
    }
}
try:
    PL_API_KEY = find_api_key()
except:
    print("Failed to get Planet Key")
    sys.exit()
url = "https://api.planet.com/compute/ops/orders/v2"


def multipoly(poly):
    multipoly_empty = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"id": 0},
                "geometry": {"type": "MultiPolygon", "coordinates": []},
            }
        ],
    }
    poly_list = []
    with open(poly) as jsonfile:
        data = json.load(jsonfile)
        if len(data["features"]) > 1:
            for things in data["features"]:
                poly_list.append(things["geometry"]["coordinates"])
            multipoly_empty["features"][0]["geometry"]["coordinates"] = poly_list
            return json.dumps(multipoly_empty)
        elif len(data["features"]) == 1:
            return data


def vdepth(dic, level=1):
    counter = 0
    str_dic = str(dic)
    if "[[[[" in str_dic:
        counter += 1
    return counter


def vertexcount(input):
    aoi_resp = input
    if vdepth(aoi_resp["geometry"]["coordinates"]) == 0:
        return str(len(aoi_resp["geometry"]["coordinates"][0]))
    elif vdepth(aoi_resp["geometry"]["coordinates"]) == 1:
        return str(len(aoi_resp["geometry"]["coordinates"][0][0]))
    else:
        print("Please check GeoJSON: Could not parse coordinates")


def order(**kwargs):
    import shapely
    from shapely.geometry import shape
    for key, value in kwargs.items():
        if key == "name":
            dbundle["name"] = value
        if key == "sid":
            if value is not None:
                dbundle["subscription_id"] = int(value)
            else:
                dbundle.pop("subscription_id", None)
        if key == "item":
            dbundle["products"][0]["item_type"] = value
        if key == "asset":
            dbundle["products"][0]["product_bundle"] = value
        if key == "idlist":
            l = []
            if value.endswith(".csv"):
                with open(value) as f:
                    try:
                        reader = csv.reader(f)
                        for row in reader:
                            item_id = row[0]
                            if str(item_id.isalpha()) == "False":
                                l.append(item_id)
                    except Exception as e:
                        print("Issue with reading: " + str(value))
            elif value.endswith(".txt"):
                with open(value) as f:
                    for line in f:
                        item_id = line.strip()
                        l.append(item_id)
            dbundle["products"][0]["item_ids"] = l
    k = dbundle
    for key, value in kwargs.items():
        if key == "op" and value != None:
            for items in value:
                if items == "clip":
                    dbundle["tools"].append(dclip)
                elif items == "toar":
                    dbundle["tools"].append(dtoar)
                elif items == "harmonize":
                    dbundle["tools"].append(dharmonize)
                elif items == "coreg":
                    dbundle["tools"].append(dcoreg)
                elif items == "format":
                    dbundle["tools"].append(dformat)
                elif items == "zip":
                    dbundle["delivery"].update(dzip["delivery"])
                elif items == "zipall":
                    dbundle["delivery"].update(dszip["delivery"])
                elif items == "email":
                    dbundle.update(demail)
                elif items == "aws":
                    dbundle["delivery"].update(daws["delivery"])
                elif items == "azure":
                    dbundle["delivery"].update(dazure["delivery"])
                elif items == "gcs":
                    dbundle["delivery"].update(dgcs["delivery"])
                elif items == "gee":
                    dbundle["delivery"].update(dgee["delivery"])
                elif items == "composite":
                    dbundle["tools"].append(dcomposite)
                elif items == "projection":
                    dbundle["tools"].append(dreproject)
                elif items == "ndvi":
                    dndvi = {"pixel_type": "32R",
                             "ndvi": "(b4 - b3) / (b4 + b3)"}
                    dbmath["bandmath"].update(dndvi)
                elif items == "gndvi":
                    dgndvi = {"pixel_type": "32R",
                              "gndvi": "(b4 - b2) / (b4 + b2)"}
                    dbmath["bandmath"].update(dgndvi)
                elif items == "ndwi":
                    dndwi = {"pixel_type": "32R",
                             "ndwi": "(b2 - b4) / (b4 + b2)"}
                    dbmath["bandmath"].update(dndwi)
                elif items == "bndvi":
                    bndvi = {"pixel_type": "32R",
                             "bndvi": "(b4 - b1) / (b4 + b1)"}
                    dbmath["bandmath"].update(bndvi)
                elif items == "tvi_deering":
                    dtvi_deering = {
                        "pixel_type": "32R", "tvi_deering": "(((b4 - b3) / (b4 + b3)) + 0.5) ** 0.5"}
                    dbmath["bandmath"].update(dtvi_deering)
                elif items == "tvi_brogeleblanc":
                    dtvi_brogeleblanc = {
                        "pixel_type": "32R", "tvi_brogeleblanc": "0.5 * ((120 * (b4 - b2) / 10000) - (200 * (b3 - b2) / 10000))"}
                    dbmath["bandmath"].update(dtvi_brogeleblanc)
                elif items == "osavi":
                    dosavi = {
                        "pixel_type": "32R",
                        "osavi": "1.16 * (b4 - b3) / (b4 + b3 + (0.16 * 10000))",
                    }
                    dbmath["bandmath"].update(dosavi)
                elif items == "evi2":
                    devi2 = {
                        "pixel_type": "32R",
                        "evi2": "2.5 * (b4 - b3) / (b4 + (2.4 * b3) + (1 * 10000))",
                    }
                    dbmath["bandmath"].update(devi2)
                elif items == "sr":
                    dsr = {"pixel_type": "32R", "sr": "(b4 / b3)"}
                    dbmath["bandmath"].update(dsr)
                elif items == "msavi2":
                    dmsavi2 = {
                        "pixel_type": "32R",
                        "msavi2": "((2 * b4 / 10000) + 1 - (((((2 * b4 / 10000) + 1) ** 2) - (8 * (b4 - b3) / 10000)) ** 0.5)) / 2",
                    }
                    dbmath["bandmath"].update(dmsavi2)
                elif items == "compression":
                    dbundle["tools"].append(dtiff)
            # dbundle[]
    for key, value in kwargs.items():
        if key == "boundary" and value != None:
            for items in k["tools"]:
                if items.get("clip"):
                    try:
                        if value.endswith(".geojson"):
                            aoi_resp = multipoly(value)
                            try:
                                for things in aoi_resp["features"]:
                                    ovall.append(
                                        things["geometry"]["coordinates"])
                            except Exception:
                                for things in json.loads(aoi_resp)["features"]:
                                    ovall.append(
                                        things["geometry"]["coordinates"])

                            aoi_geom = ovall
                            if (
                                list_depth(ovall) == 2
                                and json.loads(aoi_resp)["features"][0]["geometry"][
                                    "type"
                                ]
                                == "MultiPolygon"
                            ):
                                items["clip"]["aoi"]["coordinates"] = aoi_geom[0]
                            elif (
                                list_depth(ovall) == 2
                                and json.loads(aoi_resp)["features"][0]["geometry"][
                                    "type"
                                ]
                                != "MultiPolygon"
                            ):
                                aoi_geom = ovall[0][0]
                                items["clip"]["aoi"]["type"] = "Polygon"
                                items["clip"]["aoi"]["coordinates"] = aoi_geom
                            elif list_depth(ovall) == 1:
                                aoi_geom = ovall[0]
                                items["clip"]["aoi"]["type"] = "Polygon"
                                items["clip"]["aoi"]["coordinates"] = aoi_geom
                            elif list_depth(ovall) == 0:
                                aoi_geom = ovall
                                items["clip"]["aoi"]["type"] = "Polygon"
                                items["clip"]["aoi"]["coordinates"] = aoi_geom
                            else:
                                print(
                                    "Please check GeoJSON: Could not parse coordinates"
                                )
                            try:
                                temp = shape(items.get("clip")["aoi"])
                            except Exception as e:
                                print(e)
                            if not temp.is_valid:
                                print(
                                    "Solving shapely self intersection for multipolygon"
                                )
                                temp = temp.buffer(0)
                                geojson_string = json.dumps(
                                    shapely.geometry.mapping(temp)
                                )
                                items["clip"]["aoi"]["coordinates"] = json.loads(
                                    geojson_string
                                )["coordinates"]
                                ft = {
                                    "type": "Feature",
                                    "geometry": {"type": "Polygon", "coordinates": []},
                                    "properties": {},
                                }
                                ft["geometry"]["coordinates"] = json.loads(
                                    geojson_string
                                )["coordinates"]
                                print(
                                    "Total number of vertices in geometry: "
                                    + str(vertexcount(ft))
                                )
                                if int(vertexcount(ft)) > 500:
                                    print(
                                        "Simplifying geometry since Ordersv2 will only accept up to 500 vertex points"
                                    )
                                    b = vw.simplify_feature(ft, number=495)
                                    print(
                                        "Total number of vertices in simplified geometry: "
                                        + str(vertexcount(b))
                                        + "\n"
                                    )
                                    items["clip"]["aoi"]["coordinates"] = b["geometry"][
                                        "coordinates"
                                    ]
                                    temp = shape(b["geometry"])
                                    if not temp.is_valid:
                                        temp = temp.buffer(0)
                                        geojson_string = json.dumps(
                                            shapely.geometry.mapping(temp)
                                        )
                                        items["clip"]["aoi"][
                                            "coordinates"
                                        ] = json.loads(geojson_string)["coordinates"]
                                    elif temp.is_valid:
                                        items["clip"]["aoi"]["coordinates"] = b[
                                            "geometry"
                                        ]["coordinates"]
                        elif value.endswith(".json"):
                            with open(value) as aoi:
                                aoi_resp = json.load(aoi)
                                items["clip"]["aoi"]["coordinates"] = aoi_resp[
                                    "config"
                                ][0]["config"]["coordinates"]
                    except Exception as e:
                        print(e)
                        # print('Could not parse geometry')
        #         #print(e)
    for key, value in kwargs.items():
        if key == "aws" and value != None:
            with open(value, "r") as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
                for section in cfg:
                    k["delivery"]["amazon_s3"]["bucket"] = cfg["amazon_s3"]["bucket"]
                    k["delivery"]["amazon_s3"]["aws_region"] = cfg["amazon_s3"][
                        "aws_region"
                    ]
                    k["delivery"]["amazon_s3"]["aws_access_key_id"] = cfg["amazon_s3"][
                        "aws_access_key_id"
                    ]
                    k["delivery"]["amazon_s3"]["aws_secret_access_key"] = cfg[
                        "amazon_s3"
                    ]["aws_secret_access_key"]
                    k["delivery"]["amazon_s3"]["path_prefix"] = cfg["amazon_s3"][
                        "path_prefix"
                    ]
    for key, value in kwargs.items():
        if key == "azure" and value != None:
            with open(value, "r") as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
                for section in cfg:
                    k["delivery"]["azure_blob_storage"]["account"] = cfg["azure"][
                        "account"
                    ]
                    k["delivery"]["azure_blob_storage"]["container"] = cfg["azure"][
                        "container"
                    ]
                    k["delivery"]["azure_blob_storage"]["sas_token"] = cfg["azure"][
                        "sas_token"
                    ]
                    k["delivery"]["azure_blob_storage"][
                        "storage_endpoint_suffix"
                    ] = cfg["azure"]["storage_endpoint_suffix"]
                    k["delivery"]["azure_blob_storage"]["path_prefix"] = cfg["azure"][
                        "path_prefix"
                    ]
    for key, value in kwargs.items():
        if key == "gcs" and value != None:
            with open(value, "r") as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
                for section in cfg:
                    k["delivery"]["google_cloud_storage"]["bucket"] = cfg["gcs"][
                        "bucket"
                    ]
                    k["delivery"]["google_cloud_storage"]["credentials"] = cfg["gcs"][
                        "credentials"
                    ]
                    k["delivery"]["google_cloud_storage"]["path_prefix"] = cfg["gcs"][
                        "path_prefix"
                    ]
    for key, value in kwargs.items():
        if key == "gee" and value != None:
            project = value.split(',')[0]
            collection = value.split(',')[-1]
            k["delivery"]["google_earth_engine"]["project"] = project
            k["delivery"]["google_earth_engine"]["collection"] = collection

    for key, value in kwargs.items():
        if key == "compression" and value != None:
            for items in k["tools"]:
                if items.get("tiff_optimize"):
                    items["tiff_optimize"]["compression"] = value
    for key, value in kwargs.items():
        if key == "kernel" and value != None:
            for items in k["tools"]:
                if items.get("reproject"):
                    items["reproject"]["kernel"] = value
    for key, value in kwargs.items():
        if key == "projection" and value != None:
            for items in k["tools"]:
                if items.get("reproject"):
                    items["reproject"]["projection"] = value
    for key, value in kwargs.items():
        if key == "anchor" and value != None:
            for items in k["tools"]:
                if items.get("coregister"):
                    items["coregister"]["anchor_item"] = value
    for key, value in kwargs.items():
        if key == "format" and value != None:
            for items in k["tools"]:
                if items.get("file_format"):
                    items["file_format"]["format"] = value
    bnames = []
    for items in dbmath["bandmath"]:
        if items != "pixel_type":
            bnames.append(items)

    rg = len(bnames)
    if rg < 6:
        dck = ["b" + str(el)
               for el in range(1, rg + 1)]  # get serialized bands
        plist = [list(pair) for pair in zip(dck, bnames)]
        x.field_names = ["Band Number", "Band Name"]
        for items in plist:
            i = items[0]
            f = items[1]
            x.add_row([i, f])
            dbmath["bandmath"][i] = dbmath["bandmath"].pop(f)
    else:
        print("You can only use up to 5 bands")
        sys.exit()

    if len(dbmath["bandmath"]) > 0:
        k["tools"].append(dbmath)
    json_data = json.dumps(k)
    payload = json_data
    if len(bnames):
        print("\n")
        print(x)
        print("\n")

    # print('')
    # print(dbmath)

    # print(payload)
    ordname = k["name"]
    payload = payload.replace(
        "{{name}}_{{order_id}}.zip",
        "{{name}}_{{order_id}}_" + str(date.today()) + ".zip",
    )
    # print(payload)
    headers = {"content-type": "application/json", "cache-control": "no-cache"}
    response = requests.request(
        "POST", url, data=payload, headers=headers, auth=(PL_API_KEY, "")
    )
    if response.status_code == 202:
        content = response.json()
        try:
            clipboard.copy(str(url) + "/" + str(content["id"]))
            print(
                "Order created at "
                + str(url)
                + "/"
                + str(content["id"] + " and url copied to clipboard")
            )
            return str(url) + "/" + str(content["id"])
        except Exception:
            print(
                "Headless Setup: Order created at "
                + str(url)
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
