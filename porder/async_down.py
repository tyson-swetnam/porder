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
import asyncio
import os
import json
import glob
import progressbar
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from retrying import retry
from planet.api.auth import find_api_key

# Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print("Failed to get Planet Key")
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, "")

suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def check_for_redirects(url):
    try:
        r = SESSION.get(url, allow_redirects=False, timeout=0.5)
        if 300 <= r.status_code < 400:
            return r.headers["location"]
        elif r.status_code == 429:
            raise Exception("rate limit error")
    except requests.exceptions.Timeout:
        return "[timeout]"
    except requests.exceptions.ConnectionError:
        return "[connection error]"
    except requests.HTTPError as e:
        print(r.status_code)
        if r.status_code == 429:  # Too many requests
            raise Exception("rate limit error")


START_TIME = default_timer()


def fetch(session, url):
    urlcheck = url.split("|")[0]
    fullpath = url.split("|")[1]
    [head, tail] = os.path.split(fullpath)
    # print("Starting download of %s" % fullpath.split('/')[-1])
    if not os.path.exists(head):
        os.makedirs(head)
    os.chdir(head)
    if not os.path.isfile(fullpath):
        r = session.get(urlcheck, stream=True)
        with open(fullpath, "wb") as f:
            for ch in r:
                f.write(ch)
    elapsed = default_timer() - START_TIME
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("{0:100} {1:20}".format(tail, time_completed_at))

    return tail


urls = []
size_list = []


def funct(url, final, ext):
    filenames = glob.glob1(final, "*")
    if not os.path.exists(final):
        os.makedirs(final)
    os.chdir(final)
    response = SESSION.get(url).json()
    print("Polling with exponential backoff..")
    while (
        response["state"] == "queued"
        or response["state"] == "running"
        or response["state"] == "starting"
    ):
        bar = progressbar.ProgressBar()
        for z in bar(range(60)):
            time.sleep(1)
        response = SESSION.get(url).json()
    if response["state"] == "success" or response["state"] == "partial":
        print("Order completed with status: " + str(response["state"]))
        print("")
        for files in response["_links"]["results"]:
            if files["name"].endswith("manifest.json"):
                time.sleep(0.2)
                resp = SESSION.get(files["location"]).json()
                for things in resp["files"]:
                    size_list.append(things["size"])
        print("Estimated Download Size for order: {}".format(humansize(sum(size_list))))
        print("")
        for items in response["_links"]["results"]:
            url = items["location"]
            name = items["name"]
            if name.endswith("manifest.json"):
                time.sleep(0.2)
                resp = SESSION.get(url)
                if int(resp.status_code) == 200:
                    r = resp.content
                    inp = json.loads(r)
                    for things in inp["files"]:
                        try:
                            local_path = os.path.join(
                                final, things["path"].split("/")[-1]
                            )
                        except Exception as e:
                            print(e)
                else:
                    print(resp.status_code)
            else:
                local_path = os.path.join(final, str(os.path.split(items["name"])[-1]))
            filenames = [os.path.join(final, files) for files in filenames]
            if not local_path in filenames:
                url_to_check = url if url.startswith("https") else "http://%s" % url
                redirect_url = check_for_redirects(url_to_check)
                if not os.path.isfile(local_path) and ext is None:
                    urls.append(str(redirect_url) + "|" + local_path)
                    print("Processing total URLs " + str(len(urls)), end="\r")
                if not os.path.isfile(local_path) and ext is not None:
                    if local_path.endswith(ext):
                        urls.append(str(redirect_url) + "|" + local_path)
                        print("Processing total URLs " + str(len(urls)), end="\r")
    else:
        print("Order Failed with state: " + str(response["state"]))
    print("Processing a url list with " + str(len(urls)) + " items")
    print("\n")
    return urls


async def get_data_asynchronous(url, final, ext):
    urllist = funct(url=url, final=final, ext=ext)
    print("{0:100} {1:20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(
                        session,
                        url,
                    )  # Allows us to pass in multiple arguments to `fetch`
                )
                for url in urllist
            ]
            for response in await asyncio.gather(*tasks):
                pass


def downloader(url, final, ext):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(url, final, ext))
    loop.run_until_complete(future)


# downloader(url='https://api.planet.com/compute/ops/orders/v2/bbccc868-bada-4a4c-8c1d-9d8ef81c1d75',final=r'C:\planet_demo\mp2',ext=None)
