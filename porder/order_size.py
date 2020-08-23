import requests
import time
import progressbar
import json
import os
import sys
from retrying import retry
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key


sz = []
fname = []
suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


# Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print("Failed to get Planet Key")
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, "")


def get_session_response(url):
    response = SESSION.get(url).json()
    while (
        response["state"] == "queued"
        or response["state"] == "running"
        or response["state"] == "starting"
    ):
        bar = progressbar.ProgressBar()
        for _ in bar(range(60)):
            time.sleep(1)
        response = SESSION.get(url).json()

    return response


size_list = []


def ordersize(url):
    response = get_session_response(url)
    if response["state"] == "success" or response["state"] == "partial":
        print("")
        print("Order completed with status: " + str(response["state"]))
        for files in response["_links"]["results"]:
            if files["name"].endswith("manifest.json"):
                time.sleep(0.2)
                resp = SESSION.get(files["location"]).json()
                for things in resp["files"]:
                    size_list.append(things["size"])
        print("Estimated Download Size for order: {}".format(humansize(sum(size_list))))
