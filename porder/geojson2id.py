from __future__ import print_function

__copyright__ = """

    Copyright 2021 Samapriya Roy

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

import csv
import json
import os
import sys
from datetime import datetime, timezone
from time import mktime

import jwt
from planet.api import filters
from planet.api.utils import strp_lenient

try:
    if not os.path.exists(os.path.join(expanduser("~"), "planet.auth.json")):
        os.system('porder init')
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


client = api.ClientV1(PL_API_KEY)


temp = {"coordinates": [], "type": "MultiPolygon"}
tempsingle = {"coordinates": [], "type": "Polygon"}
stbase = {"config": [], "field_name": [], "type": "StringInFilter"}
rbase = {"config": {"gte": [], "lte": []},
         "field_name": [], "type": "RangeFilter"}


# Get time right
def time2epoch(st):
    str_time = datetime.strptime(st.isoformat(), "%Y-%m-%dT%H:%M:%S")
    str_tuple = str_time.timetuple()
    epoch_time = mktime(str_tuple)
    return epoch_time


def time2utc(st):
    st_time = strp_lenient(st)
    if st_time is not None:
        dt_ts = datetime.fromtimestamp(time2epoch(st_time), tz=timezone.utc)
        return dt_ts.isoformat().replace("+00:00", "Z")
    else:
        sys.exit("Could not parse time {}: check and retry".format(st))


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


# Area lists
ar = []
far = []
ovall = []


# Handle MultiPolygon
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


# Function to use the client and then search
def idl(**kwargs):
    import pyproj
    from shapely.geometry import shape
    from shapely.ops import transform
    for key, value in kwargs.items():
        if key == "infile" and value is not None:
            infile = value
            try:
                if infile.endswith(".geojson"):
                    aoi_resp = multipoly(infile)
                    try:
                        for things in aoi_resp["features"]:
                            ovall.append(things["geometry"]["coordinates"])
                    except Exception:
                        for things in json.loads(aoi_resp)["features"]:
                            ovall.append(things["geometry"]["coordinates"])
                    # print(list_depth(ovall))
                    aoi_geom = ovall
                    if (
                        list_depth(ovall) == 2
                        and json.loads(aoi_resp)["features"][0]["geometry"]["type"]
                        == "MultiPolygon"
                    ):
                        temp["coordinates"] = aoi_geom[0]
                    elif (
                        list_depth(ovall) == 2
                        and json.loads(aoi_resp)["features"][0]["geometry"]["type"]
                        != "MultiPolygon"
                    ):
                        aoi_geom = ovall[0][0]
                        temp["type"] = "Polygon"
                        temp["coordinates"] = aoi_geom
                    elif list_depth(ovall) == 1:
                        aoi_geom = ovall[0]
                        temp["type"] = "Polygon"
                        temp["coordinates"] = aoi_geom
                    elif list_depth(ovall) == 0:
                        aoi_geom = ovall
                        temp["type"] = "Polygon"
                        temp["coordinates"] = aoi_geom
                    else:
                        print("Please check GeoJSON: Could not parse coordinates")
                elif infile.endswith(".json"):
                    with open(infile) as aoi:
                        aoi_resp = json.load(aoi)
                        aoi_geom = aoi_resp["config"][0]["config"]["coordinates"]
            except Exception as e:
                print("Could not parse geometry")
                print(e)
        if key == "item" and value is not None:
            try:
                item = value
            except Exception as e:
                sys.exit(e)
        if key == "start" and value is not None:
            try:
                start = time2utc(value)
                st = filters.date_range("acquired", gte=start)
            except Exception as e:
                sys.exit(e)
        if key == "end" and value is not None:
            try:
                end = time2utc(value)
                ed = filters.date_range("acquired", lte=end)
            except Exception as e:
                sys.exit(e)
        if key == "asset" and value is not None:
            try:
                asset = value
            except Exception as e:
                sys.exit(e)
        if key == "cmin":
            if value == None:
                try:
                    cmin = 0
                except Exception as e:
                    print(e)
            if value is not None:
                try:
                    cmin = float(value)
                except Exception as e:
                    print(e)
        if key == "cmax":
            if value == None:
                try:
                    cmax = 1
                except Exception as e:
                    print(e)
            elif value is not None:
                try:
                    cmax = float(value)
                except Exception as e:
                    print(e)
        if key == "num":
            if value is not None:
                num = value
            elif value == None:
                num = 1000000
        if key == "outfile" and value is not None:
            outfile = value
            try:
                open(outfile, "w")
            except Exception as e:
                sys.exit(e)
        if key == "ovp":
            if value is not None:
                ovp = int(value)
            elif value == None:
                ovp = 0.01
        if key == "filters" and value is not None:
            for items in value:
                ftype = items.split(":")[0]
                if ftype == "string":
                    try:
                        fname = items.split(":")[1]
                        fval = items.split(":")[2]
                        # stbase={'config': [], 'field_name': [], 'type': 'StringInFilter'}
                        stbase["config"] = fval.split(",")  # fval
                        stbase["field_name"] = fname
                    except Exception as e:
                        print(e)
                elif ftype == "range":
                    fname = items.split(":")[1]
                    fgt = items.split(":")[2]
                    flt = items.split(":")[3]
                    # rbase={'config': {'gte': [], 'lte': []},'field_name': [], 'type': 'RangeFilter'}
                    rbase["config"]["gte"] = int(fgt)
                    rbase["config"]["lte"] = int(flt)
                    rbase["field_name"] = fname

    print("Running search for a maximum of: " + str(num) + " assets")
    l = 0
    [head, tail] = os.path.split(outfile)
    sgeom = filters.geom_filter(temp)
    aoi_shape = shape(temp)
    if not aoi_shape.is_valid:
        aoi_shape = aoi_shape.buffer(0)
        # print('Your Input Geometry is invalid & may have issues:A valid Polygon may not possess anyoverlapping exterior or interior rings.'+'\n')
    date_filter = filters.date_range("acquired", gte=start, lte=end)
    cloud_filter = filters.range_filter("cloud_cover", gte=cmin, lte=cmax)
    asset_filter = filters.permission_filter(
        "assets." + str(asset.split(",")[0]) + ":download"
    )
    # print(rbase)
    # print(stbase)
    if len(rbase["field_name"]) != 0 and len(stbase["field_name"]) != 0:
        and_filter = filters.and_filter(
            date_filter, cloud_filter, asset_filter, sgeom, stbase, rbase
        )
    elif len(rbase["field_name"]) == 0 and len(stbase["field_name"]) != 0:
        and_filter = filters.and_filter(
            date_filter, cloud_filter, asset_filter, sgeom, stbase
        )
    elif len(rbase["field_name"]) != 0 and len(stbase["field_name"]) == 0:
        and_filter = filters.and_filter(
            date_filter, cloud_filter, asset_filter, sgeom, rbase
        )
    elif len(rbase["field_name"]) == 0 and len(stbase["field_name"]) == 0:
        and_filter = filters.and_filter(
            date_filter, cloud_filter, asset_filter, sgeom)
    item_types = [item]
    req = filters.build_search_request(and_filter, item_types)
    res = client.quick_search(req)
    for things in res.items_iter(
        1000000
    ):  # A large number as max number to check against
        try:
            all_assets = [
                assets.split(":")[0].replace("assets.", "")
                for assets in things["_permissions"]
            ]
            if things["properties"]["quality_category"] == "standard" and all(
                elem in all_assets for elem in asset.split(",")
            ):
                itemid = things["id"]
                footprint = things["geometry"]
                s = shape(footprint)
                if aoi_shape.area > s.area:
                    intersect = (s).intersection(aoi_shape)
                elif s.area >= aoi_shape.area:
                    intersect = (aoi_shape).intersection(s)
                proj_transform = pyproj.Transformer.from_proj(
                    pyproj.Proj(4326), pyproj.Proj(3857), always_xy=True
                ).transform  # always_xy determines correct coord order
                print(
                    "Processing "
                    + str(len(ar) + 1)
                    + " items with total area "
                    + str("{:,}".format(round(sum(far))))
                    + " sqkm",
                    end="\r",
                )
                if (
                    transform(proj_transform, (aoi_shape)).area
                    > transform(proj_transform, s).area
                ):
                    if (
                        transform(proj_transform, intersect).area
                        / transform(proj_transform, s).area
                        * 100
                    ) >= ovp:
                        ar.append(transform(proj_transform,
                                  intersect).area / 1000000)
                        far.append(transform(proj_transform, s).area / 1000000)
                        with open(outfile, "a") as csvfile:
                            writer = csv.writer(
                                csvfile, delimiter=",", lineterminator="\n"
                            )
                            writer.writerow([itemid])
                elif (
                    transform(proj_transform, s).area
                    >= transform(proj_transform, aoi_shape).area
                ):
                    if (
                        transform(proj_transform, intersect).area
                        / transform(proj_transform, aoi_shape).area
                        * 100
                    ) >= ovp:
                        ar.append(transform(proj_transform,
                                  intersect).area / 1000000)
                        far.append(transform(proj_transform, s).area / 1000000)
                        with open(outfile, "a") as csvfile:
                            writer = csv.writer(
                                csvfile, delimiter=",", lineterminator="\n"
                            )
                            writer.writerow([itemid])
            if int(len(ar)) == int(num):
                break
        except Exception as e:
            pass
        except (KeyboardInterrupt, SystemExit) as e:
            print("\n" + "Program escaped by User")
            sys.exit()
    num_lines = sum(1 for line in open(
        os.path.join(head, tail.split(".")[0] + ".csv")))
    print(
        "Total number of item ids written to "
        + str(
            os.path.join(head, tail.split(".")[
                         0] + ".csv") + " ===> " + str(num_lines)
        )
    )
    print(
        "Total estimated cost to quota: "
        + str("{:,}".format(round(sum(far))))
        + " sqkm"
    )
    print(
        "Total estimated cost to quota if clipped: "
        + str("{:,}".format(round(sum(ar))))
        + " sqkm"
    )


# idl(infile=r"C:\Users\samapriya\Downloads\vertex.geojson",item='PSScene4Band',asset='analytic',cmin=0.0,cmax=0.9,start='2018-01-01',end='2019-12-31',ovp=8,num=40,outfile=r'C:\planet_demo\vertexidl.csv')
