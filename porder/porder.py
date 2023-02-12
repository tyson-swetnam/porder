from __future__ import print_function

import visvalingamwyatt as vw
from planet.api.auth import find_api_key

from .async_downloader import asyncdownload
from .diffcheck import checker
from .downloader import download
from .geojson2id import idl
from .idcheck import idc
from .order_now import order
from .order_size import ordersize
from .ordstat import ostat
from .resubmit import reorder
from .text_split import idsplit

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

import argparse
import base64
import datetime
import json
import os
import platform
import subprocess
import sys
import time
import webbrowser
from os.path import expanduser

import clipboard
import dateutil.parser
import pkg_resources
import requests
from bs4 import BeautifulSoup
from logzero import logger
from pySmartDL import SmartDL


class Solution:
    def compareVersion(self, version1, version2):
        versions1 = [int(v) for v in version1.split(".")]
        versions2 = [int(v) for v in version2.split(".")]
        for i in range(max(len(versions1), len(versions2))):
            v1 = versions1[i] if i < len(versions1) else 0
            v2 = versions2[i] if i < len(versions2) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


ob1 = Solution()

if str(platform.system().lower()) == "windows":
    version = sys.version_info[0]
    try:
        import pipgeo
        response = requests.get('https://pypi.org/pypi/pipgeo/json')
        latest_version = response.json()['info']['version']
        vcheck = ob1.compareVersion(
            latest_version,
            pkg_resources.get_distribution("pipgeo").version,
        )
        if vcheck == 1:
            subprocess.call(
                f"{sys.executable}" + " -m pip install pipgeo --upgrade", shell=True
            )
    except ImportError:
        subprocess.call(
            f"{sys.executable}" + " -m pip install pipgeo", shell=True
        )
    except Exception as e:
        logger.exception(e)
    try:
        from osgeo import gdal
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipgeo fetch --lib gdal", shell=True)
    except Exception as e:
        logger.exception(e)
    try:
        import pyproj
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipgeo fetch --lib pyproj", shell=True)
        import pyproj
    except Exception as e:
        logger.exception(e)
    try:
        import shapely
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipgeo fetch --lib shapely", shell=True)
    except Exception as e:
        logger.exception(e)
    try:
        import fiona
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipgeo fetch --lib fiona", shell=True)
    except Exception as e:
        logger.exception(e)
    try:
        import geopandas as gpd
    except ImportError:
        subprocess.call(
            f"{sys.executable}" + " -m pip install geopandas", shell=True
        )
        import geopandas as gpd
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    except Exception as e:
        logger.exception(e)


if str(platform.python_version()) > "3.3.0":
    from .async_down import downloader
os.chdir(os.path.dirname(os.path.realpath(__file__)))
lpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)


def version_latest(package):
    response = requests.get(f'https://pypi.org/pypi/{package}/json')
    latest_version = response.json()['info']['version']
    return latest_version


def porder_version():
    vcheck = ob1.compareVersion(
        version_latest('porder'),
        pkg_resources.get_distribution("porder").version,
    )
    if vcheck == 1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of porder is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("porder").version,
                version_latest('porder'),
            )
        )
        print(
            "========================================================================="
        )
    elif vcheck == -1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Possibly running staging code {} compared to pypi release {}".format(
                pkg_resources.get_distribution("porder").version,
                version_latest('porder'),
            )
        )
        print(
            "========================================================================="
        )


porder_version()


# Go to the readMe
def readme():
    try:
        a = webbrowser.open("https://tyson-swetnam.github.io/porder/", new=2)
        if a == False:
            print("Your setup does not have a monitor to display the webpage")
    except Exception as e:
        print(e)


def read_from_parser(args):
    readme()


# Function to get user's quota
def planet_quota():
    # Get API Key: Requires user to have initialized Planet CLI
    try:
        api_key = find_api_key()
    except Exception as e:
        print("Failed to get Planet Key: Try planet init")
        sys.exit()
    """Print allocation and remaining quota in Sqkm."""
    try:
        main = requests.get(
            "https://api.planet.com/auth/v1/experimental/public/my/subscriptions",
            auth=(api_key, ""),
        )
        if main.status_code == 200:
            content = main.json()
            for item_id in content:
                try:
                    print(" ")
                    print("Subscription ID: %s" % item_id["id"])
                    print("Plan ID: %s" % item_id["plan_id"])
                    print("Allocation Name: %s" %
                          item_id["organization"]["name"])
                    print(
                        "Allocation active from: %s"
                        % item_id["active_from"].split("T")[0]
                    )
                    if item_id["active_to"] is not None:
                        print(
                            "Allocation active to: %s"
                            % item_id["active_to"].split("T")[0]
                        )
                    print("Quota Enabled: %s" % item_id["quota_enabled"])
                    print("Total Quota in SqKm: %s" % item_id["quota_sqkm"])
                    print("Total Quota used: %s" % item_id["quota_used"])
                    if (item_id["quota_sqkm"]) is not None:
                        leftquota = float(
                            item_id["quota_sqkm"] -
                            float(item_id["quota_used"])
                        )
                        print("Remaining Quota in SqKm: %s" % leftquota)
                    else:
                        print("No Quota Allocated")
                    print("")
                except Exception as e:
                    pass
        elif main.status_code == 500:
            print("Temporary issue: Try again")
        else:
            print("Failed with exception code: " + str(main.status_code))

    except IOError:
        print("Initialize client or provide API Key")


def planet_quota_from_parser(args):
    planet_quota()


def convert(folder, export):
    for items in os.listdir(folder):
        if items.endswith(".shp"):
            inD = gpd.read_file(os.path.join(folder, items), encoding="utf-8")
            # Reproject to EPSG 4326
            try:
                data_proj = inD.copy()
                data_proj["geometry"] = data_proj["geometry"].to_crs(epsg=4326)
                data_proj.to_file(
                    os.path.join(export, str(
                        items).replace(".shp", ".geojson")),
                    driver="GeoJSON",
                )
                print(
                    f"Export completed to {os.path.join(export, str(items).replace('.shp', '.geojson'))}")
            except Exception as e:
                print(e)
        elif items.endswith(".kml"):
            try:
                gdf = gpd.read_file(
                    os.path.join(folder, items), driver='KML')
                gdf.to_file(
                    os.path.join(export, str(
                        items).replace(".kml", ".geojson")),
                    driver="GeoJSON",
                )
                print(
                    f"Export completed to {os.path.join(export, str(items).replace('.kml', '.geojson'))}")
            except Exception as e:
                print(e)

# Convert folder with multiple shapefiles to geojsons


def convert_metadata_from_parser(args):
    convert(folder=args.source, export=args.destination)


# base64 encoding for GCS credentials
def gcs_cred(cred):
    with open(cred) as file:
        aoi_resp = json.load(file)
        filestr = json.dumps(aoi_resp)
        print("")
        bstr = filestr.encode("utf-8")
        try:
            clipboard.copy(base64.b64encode(bstr).decode("ascii"))
            print("base64 encoding copied to clipboard")
        except Exception as e:
            print("Unable to copy to clipboard" + "\n")
            print(base64.b64encode(bstr).decode("ascii"))


def gcs_cred_from_parser(args):
    gcs_cred(cred=args.cred)


def vertexcount(inp):
    gdf = gpd.read_file(inp)
    nodes = []
    for index, row in gdf.iterrows():
        for pt in list(row['geometry'].exterior.coords):
            nodes.append(pt)

    return len(nodes)


def geosimple(inp, output, num):
    gdf = gpd.read_file(inp)
    print(f"Vertex count {vertexcount(inp)}")
    ft = gdf.to_json()
    ft = json.loads(ft).get('features')[0]
    try:
        b = vw.simplify_feature(ft, number=num-1)
        ft["geometry"]["coordinates"] = b["geometry"]["coordinates"]
        with open(output, "w") as g:
            json.dump(ft, g)
        print(f"Write Completed to: {output}")
        print(f"New vertex count {vertexcount(output)}")
    except Exception as e:
        print(e)

# Simplify geojson by vertex count


def simplify_from_parser(args):
    geosimple(inp=args.input, output=args.output, num=args.number)


# Create ID List with structured JSON
def idlist_from_parser(args):
    print("")
    if args.asset is None:
        with open(os.path.join(lpath, "bundles.json")) as f:
            r = json.load(f)
            for key, value in r["bundles"].items():
                mydict = r["bundles"][key]["assets"]
                for item_types in mydict:
                    if args.item == item_types:
                        print(
                            "Assets for item "
                            + str(args.item)
                            + " of Bundle type "
                            + str(key)
                            + ": "
                            + str(", ".join(mydict[args.item]))
                        )
        sys.exit()
    idl(
        infile=args.input,
        start=args.start,
        end=args.end,
        item=args.item,
        asset=args.asset,
        num=args.number,
        cmin=args.cmin,
        cmax=args.cmax,
        ovp=args.overlap,
        outfile=args.outfile,
        filters=args.filters,
    )


# Convert folder with multiple shapefiles to geojsons
def idcheck_from_parser(args):
    idc(idlist=args.idlist, item=args.item,
        asset=args.asset, geometry=args.geometry)


# Check difference from local filelist
def difflist_from_parser(args):
    checker(
        folder=args.folder,
        typ=args.typ,
        infile=args.input,
        item=args.item,
        asset=args.asset,
        start=args.start,
        end=args.end,
        cmin=args.cmin,
        cmax=args.cmax,
        outfile=args.outfile,
    )


# Offcourse all good merge sometimes needs a split
def idsplit_from_parser(args):
    idsplit(infile=args.idlist, linenum=args.lines, output=args.local)


# Get package version
def bundles(item):
    page_url = "https://developers.planet.com/apis/orders/product-bundles-reference/"
    req = requests.get(page_url)
    soup = BeautifulSoup(req.text, "html.parser")
    for link in soup.find_all('a', href=True):
        if link.get('href').endswith('.json'):
            bundle_url = link.get('href')
    date_response = requests.get(bundle_url).json()
    ref_date = dateutil.parser.parse(date_response['version'])
    with open(os.path.join(lpath, "bundles.json")) as f:
        r = json.load(f)
        current = r['version']
        curr_date = dateutil.parser.parse(current)
    if curr_date < ref_date:
        print("Refreshing bundles to " + "\n" + str(date_response['version']))
        try:
            url = bundle_url
            dest = os.path.join(lpath, "bundles.json")
            obj = SmartDL(url, dest)
            obj.start()
            path = obj.get_dest()
        except Exception as e:
            print(e)
    else:
        print("Bundles version: " + str(current) + "\n")
    print("")
    with open(os.path.join(lpath, "bundles.json")) as f:
        r = json.load(f)
        for key, value in r["bundles"].items():
            mydict = r["bundles"][key]["assets"]
            for item_types in mydict:
                if item == item_types:
                    print(
                        "Bundle type: "
                        + str(key)
                        + "\n"
                        + str(", ".join(mydict[item]))
                        + "\n"
                    )


def bundles_from_parser(args):
    bundles(item=args.item)


# Place the order
def order_from_parser(args):
    order(
        name=args.name,
        idlist=args.idlist,
        item=args.item,
        asset=args.bundle,
        sid=args.sid,
        op=args.op,
        anchor=args.anchor,
        format=args.format,
        boundary=args.boundary,
        projection=args.projection,
        gee=args.gee,
        kernel=args.kernel,
        compression=args.compression,
        aws=args.aws,
        azure=args.azure,
        gcs=args.gcs,
    )


# Reorer an old or failed order
def reorder_from_parser(args):
    reorder(url=args.url, notification=args.notification)


# Cancel an order or all order
def cancel(id):
    headers = {"Content-Type": "application/json"}
    # Get API Key: Requires user to have initialized Planet CLI
    try:
        api_key = find_api_key()
    except Exception as e:
        print("Failed to get Planet Key: Try planet init")
        sys.exit()
    if id == "all":
        url = "https://api.planet.com/compute/ops/bulk/orders/v2/cancel"
        resp = requests.post(
            url, data="{}", headers=headers, auth=(api_key, ""))
        if resp.status_code == 200:
            print(
                "Number of orders failed to cancel: "
                + str(resp.json()["result"]["failed"]["count"])
            )
            print(
                "Number of orders successfully cancelled: "
                + str(resp.json()["result"]["succeeded"]["count"])
            )
        else:
            print(
                "Failed wth status code & error: "
                + str(resp.status_code)
                + " : "
                + str(resp.json())
            )
    else:
        url = "https://api.planet.com/compute/ops/orders/v2/" + str(id)
        resp = requests.put(url, headers=headers, auth=(api_key, ""))
        if resp.status_code == 200:
            print("Orders ID " + str(id) + " successfully cancelled")
        else:
            print(
                "Failed wth status code & error: "
                + str(resp.status_code)
                + " : "
                + str(resp.json())
            )


def cancel_from_parser(args):
    cancel(id=args.id)


# Get size of order in human size
def ordersize_from_parser(args):
    ordersize(url=args.url)


# Get concurrent orders that are running
def stats():
    # Get API Key: Requires user to have initialized Planet CLI
    try:
        api_key = find_api_key()
    except Exception as e:
        print("Failed to get Planet Key: Try planet init")
        sys.exit()

    SESSION = requests.Session()
    SESSION.auth = (api_key, "")
    print("Checking on all running orders...")
    result = SESSION.get("https://api.planet.com/compute/ops/stats/orders/v2")
    if int(result.status_code) == 200:
        page = result.json()
        try:
            print(
                "\n"
                + "Total queued order for organization: "
                + str(page["organization"]["queued_orders"])
            )
            print(
                "Total running orders for organization: "
                + str(page["organization"]["running_orders"])
            )
            print(
                "\n"
                + "Total queued orders for user: "
                + str(page["user"]["queued_orders"])
            )
            print(
                "Total running orders for user: " +
                str(page["user"]["running_orders"])
            )
        except Exception as e:
            print(e)
    elif int(result.status_code) == 401:
        print("Access denied - insufficient privileges")
    elif int(result.status_code) == 500:
        print("Server Error")
    else:
        print("Failed with " + str(result.status_code) + " " + str(result.text))


def stats_from_parser(args):
    stats()


# Get order list by state and date
def ostate_from_parser(args):
    ostat(state=args.state, start=args.start, end=args.end, limit=args.limit)


# Download the order
def download_from_parser(args):
    download(url=args.url, local=args.local, ext=args.ext)


# Multithreaded downloader
def asyncdownload_from_parser(args):
    asyncdownload(url=args.url, local=args.local, ext=args.ext)


def multiproc_from_parser(args):
    if str(platform.python_version()) > "3.3.0":
        downloader(url=args.url, final=args.local, ext=args.ext)
    elif str(platform.python_version()) <= "3.3.0":
        if args.ext == None:
            subprocess.call(
                "python multiproc_pydl.py " + args.url + " " + args.local + " ",
                shell=True,
            )
        else:
            subprocess.call(
                "python multiproc_pydl.py "
                + args.url
                + " "
                + args.local
                + " "
                + args.ext,
                shell=True,
            )


print("")

spacing = "                               "


def main(args=None):
    parser = argparse.ArgumentParser(description="Ordersv2 Simple Client")
    subparsers = parser.add_subparsers()

    parser_read = subparsers.add_parser(
        "readme", help="Go the web based porder readme page"
    )
    parser_read.set_defaults(func=read_from_parser)

    parser_planet_quota = subparsers.add_parser(
        "quota", help="Prints your Planet Quota Details"
    )
    parser_planet_quota.set_defaults(func=planet_quota_from_parser)

    parser_convert = subparsers.add_parser(
        "convert", help="Convert all shapefiles or kmls in folder to GeoJSON"
    )
    parser_convert.add_argument("--source", help="Choose Source Folder")
    parser_convert.add_argument(
        "--destination", help="Choose Destination Folder")
    parser_convert.set_defaults(func=convert_metadata_from_parser)

    parser_gcs_cred = subparsers.add_parser(
        "base64", help="Base 64 encode a JSON file")
    required_named = parser_gcs_cred.add_argument_group(
        "Required named arguments.")
    required_named.add_argument(
        "--cred", help="Path to GCS credential file", required=True
    )
    parser_gcs_cred.set_defaults(func=gcs_cred_from_parser)

    parser_simplify = subparsers.add_parser(
        "simplify",
        help="Simplifies geometry to number of vertices specified using Visvalingam-Wyatt line simplification algorithm",
    )
    parser_simplify.add_argument("--input", help="Input GeoJSON file")
    parser_simplify.add_argument(
        "--output", help="Output simplified GeoJSON file")
    parser_simplify.add_argument(
        "--number", help="Total number of vertices in output GeoJSON"
    )
    parser_simplify.set_defaults(func=simplify_from_parser)

    parser_idlist = subparsers.add_parser(
        "idlist", help="Get idlist using geometry & filters"
    )
    required_named = parser_idlist.add_argument_group(
        "Required named arguments.")
    required_named.add_argument(
        "--input", help="Input geometry file for now geojson/json/kml", required=True
    )
    required_named.add_argument(
        "--start", help="Start Date &/or Time yyyy-mm-ddTHH:MM:SS", required=True
    )
    required_named.add_argument(
        "--end", help="End Date &/or Time yyyy-mm-ddTHH:MM:SS", required=True
    )
    required_named.add_argument(
        "--item",
        help="Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc",
        required=True,
    )
    required_named.add_argument(
        "--asset", help="Asset Type analytic, analytic_sr,visual etc", default=None
    )
    required_named.add_argument(
        "--outfile", help="Output csv file", required=True)
    optional_named = parser_idlist.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--cmin", help="Minimum cloud cover 0-1 represents 0 to 100", default=None
    )
    optional_named.add_argument(
        "--cmax", help="Maximum cloud cover 0-1 represents 0 to 100", default=None
    )
    optional_named.add_argument(
        "--number",
        help="Total number of assets, give a large number if you are not sure",
        default=None,
    )
    optional_named.add_argument(
        "--overlap",
        help="Percentage overlap of image with search area range between 0 to 100",
        default=None,
    )
    optional_named.add_argument(
        "--filters",
        nargs="+",
        help="Add an additional string or range filter, Read Me",
        default=None,
    )
    parser_idlist.set_defaults(func=idlist_from_parser)

    parser_difflist = subparsers.add_parser(
        "difflist",
        help="Checks the difference between local files and available Planet assets",
    )
    required_named = parser_difflist.add_argument_group(
        "Required named arguments.")
    required_named.add_argument(
        "--folder",
        help="local folder where image or metadata files are stored",
        required=True,
    )
    required_named.add_argument(
        "--typ", help="File type image or metadata", required=True
    )
    required_named.add_argument(
        "--input", help="Input boundary to search (geojson, json)", required=True
    )
    required_named.add_argument(
        "--item",
        help="Planet Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc",
        required=True,
    )
    required_named.add_argument(
        "--asset", help="Asset Type analytic, analytic_sr,visual etc", required=True
    )
    required_named.add_argument(
        "--start", help="Start date in format YYYY-MM-DD", required=True)
    required_named.add_argument(
        "--end", help="End date in format YYYY-MM-DD", required=True)
    required_named.add_argument(
        "--outfile", help="Full path to CSV file with difference ID list", required=True
    )
    optional_named = parser_difflist.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--cmin", help="Minimum cloud cover 0-1 represents 0 to 100"
    )
    optional_named.add_argument(
        "--cmax", help="Maximum cloud cover 0-1 represents 0 to 100"
    )
    parser_difflist.set_defaults(func=difflist_from_parser)

    parser_idsplit = subparsers.add_parser(
        "idsplit", help="Splits ID list incase you want to run them in small batches"
    )
    parser_idsplit.add_argument("--idlist", help="Idlist txt file to split")
    parser_idsplit.add_argument(
        "--lines", help="Maximum number of lines in each split files"
    )
    parser_idsplit.add_argument(
        "--local", help="Output folder where split files will be exported"
    )
    parser_idsplit.set_defaults(func=idsplit_from_parser)

    parser_idcheck = subparsers.add_parser(
        "idcheck", help="Check idlist for estimating clipped area"
    )
    parser_idcheck.add_argument("--idlist", help="Idlist csv file")
    parser_idcheck.add_argument("--item", help="Item type")
    parser_idcheck.add_argument("--asset", help="Asset type")
    optional_named = parser_idcheck.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--geometry", help="Geometry file for clip if any", default=None
    )
    parser_idcheck.set_defaults(func=idcheck_from_parser)

    parser_bundles = subparsers.add_parser(
        "bundles", help="Check bundles of assets for given tiem type"
    )
    parser_bundles.add_argument("--item", help="Item type")
    parser_bundles.set_defaults(func=bundles_from_parser)

    parser_order = subparsers.add_parser(
        "order",
        help='Place an order & get order url currently supports "toar","clip","composite","reproject","compression"',
    )
    required_named = parser_order.add_argument_group(
        "Required named arguments.")
    required_named.add_argument(
        "--name", help="Order Name to be Submitted", required=True
    )
    required_named.add_argument(
        "--idlist", help="CSV idlist with item IDs", required=True
    )
    required_named.add_argument(
        "--item",
        help="Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc",
        required=True,
    )
    required_named.add_argument(
        "--bundle",
        help="Bundle Type: analytic, analytic_sr,analytic_sr_udm2",
        required=True,
    )
    optional_named = parser_order.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument("--sid", help="Subscription ID", default=None)
    optional_named.add_argument(
        "--boundary",
        help="Boundary/geometry for clip operation geojson|json|kml",
        default=None,
    )
    optional_named.add_argument(
        "--projection",
        help='Projection for reproject operation of type "EPSG:4326"',
        default=None,
    )
    optional_named.add_argument(
        "--gee",
        help='provide gee-project,gee-collection',
        default=None,
    )
    optional_named.add_argument(
        "--kernel",
        help='Resampling kernel used "near", "bilinear", "cubic", "cubicspline", "lanczos", "average" and "mode"',
        default=None,
    )
    optional_named.add_argument(
        "--compression",
        help='Compression type used for tiff_optimize tool, "lzw"|"deflate"',
        default=None,
    )
    optional_named.add_argument(
        "--anchor",
        help='Anchor Item ID to use for the coregistration tool',
        default=None,
    )
    optional_named.add_argument(
        "--format",
        help='Delivery format choose from COG/PL_NITF to use for the format tool',
        default=None,
    )
    optional_named.add_argument(
        "--aws", help="AWS cloud credentials config yml file", default=None
    )
    optional_named.add_argument(
        "--azure", help="Azure cloud credentials config yml file", default=None
    )
    optional_named.add_argument(
        "--gcs", help="GCS cloud credentials config yml file", default=None
    )
    optional_named.add_argument(
        "--op",
        nargs="+",
        help="Add operations, delivery & notification clip|toar|harmonize|composite|zip|zipall|compression|projection|kernel|coreg|format|aws|azure|gcs|gee|email <Choose indices from>: ndvi|gndvi|ndwi|bndvi|tvi_deering|tvi_brogeleblanc|osavi|evi2|sr|msavi2",
        default=None,
    )

    parser_order.set_defaults(func=order_from_parser)

    parser_reorder = subparsers.add_parser(
        "reorder", help="Reorder an existing order")
    required_named = parser_reorder.add_argument_group(
        "Required named arguments.")
    required_named.add_argument(
        "--url", help="Order url to be ordered", required=True)
    optional_named = parser_reorder.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--notification", help='Use "email" to get an email notification', default=None
    )
    parser_reorder.set_defaults(func=reorder_from_parser)

    parser_cancel = subparsers.add_parser(
        "cancel", help="Cancel queued order(s)")
    parser_cancel.add_argument(
        "--id", help='order id you want to cancel use "all" to cancel all'
    )
    parser_cancel.set_defaults(func=cancel_from_parser)

    parser_ordersize = subparsers.add_parser(
        "ordersize", help="Estimate total download size"
    )
    parser_ordersize.add_argument(
        "--url", help="order url you got for your order")
    parser_ordersize.set_defaults(func=ordersize_from_parser)

    parser_ostate = subparsers.add_parser(
        "ostate", help="Get list of orders by state and date range"
    )
    parser_ostate.add_argument(
        "--state",
        help="choose state between queued| running | success | failed | partial",
    )
    parser_ostate.add_argument(
        "--start", help="start date in format YYYY-MM-DD")
    parser_ostate.add_argument("--end", help="end date in format YYYY-MM-DD")
    optional_named = parser_ostate.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--limit", help="Limit the maximum table size", default=None
    )
    parser_ostate.set_defaults(func=ostate_from_parser)

    parser_stats = subparsers.add_parser(
        "stats", help="Prints number of orders queued and running for org & user"
    )
    parser_stats.set_defaults(func=stats_from_parser)

    parser_download = subparsers.add_parser(
        "download", help="Downloads all files in your order"
    )
    parser_download.add_argument(
        "--url", help="order url you got for your order")
    parser_download.add_argument(
        "--local", help="Output folder where ordered files will be exported"
    )
    optional_named = parser_download.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--ext", help="File Extension to download", default=None
    )
    parser_download.set_defaults(func=download_from_parser)

    parser_asyncdownload = subparsers.add_parser(
        "multipart", help="Uses multiprocessing to download for all files in your order"
    )
    parser_asyncdownload.add_argument(
        "--url", help="order url you got for your order")
    parser_asyncdownload.add_argument(
        "--local", help="Output folder where ordered files will be exported"
    )
    optional_named = parser_asyncdownload.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--ext", help="File Extension to download", default=None
    )
    parser_asyncdownload.set_defaults(func=asyncdownload_from_parser)

    parser_multiproc = subparsers.add_parser(
        "multiproc",
        help="Multiprocess based downloader to download for all files in your order",
    )
    parser_multiproc.add_argument(
        "--url", help="order url you got for your order")
    parser_multiproc.add_argument(
        "--local", help="Output folder where ordered files will be exported"
    )
    optional_named = parser_multiproc.add_argument_group(
        "Optional named arguments")
    optional_named.add_argument(
        "--ext", help="File Extension to download", default=None
    )
    parser_multiproc.set_defaults(func=multiproc_from_parser)
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
