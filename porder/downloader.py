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
import time
import progressbar
import json
import os
import sys
import csv
from retrying import retry
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key

#Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

# To get redirect link
@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def check_for_redirects(url):
    try:
        r = SESSION.get(url, allow_redirects=False, timeout=0.5)
        if 300 <= r.status_code < 400:
            return r.headers['location']
        else:
            return 'no redirect'
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'

#Get the redirects and download
def download(url,local,ext):
    response=SESSION.get(url).json()
    print("Polling ...")
    while response['state']=='running' or response['state']=='starting':
        bar = progressbar.ProgressBar()
        for z in bar(range(60)):
            time.sleep(1)
        response=SESSION.get(url).json()
    if response['state']=='success':
        for items in response['_links']['results']:
            url=(items['location'])
            url_to_check = url if url.startswith('https') else "http://%s" % url
            redirect_url = check_for_redirects(url_to_check)
            if redirect_url.startswith('https'):
                #print('Processing redirect link for '+str(os.path.split(items['name'])[-1]))
                local_path=os.path.join(local,str(os.path.split(items['name'])[-1]))
                result=SESSION.get(redirect_url)
                if not os.path.exists(local_path) and result.status_code==200:
                    if ext is not None:
                        if local_path.endswith(ext):
                            print("Downloading: " + str(local_path))
                            f = open(local_path, 'wb')
                            for chunk in result.iter_content(chunk_size=512 * 1024):
                                if chunk:
                                    f.write(chunk)
                            f.close()
                    elif ext is None:
                        print("Downloading: " + str(local_path))
                        f = open(local_path, 'wb')
                        for chunk in result.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                else:
                    if int(result.status_code)!=200:
                        print("Encountered error with code: " + str(result.status_code)+' for '+str(os.path.split(items['name'])[-1]))
                    elif int(result.status_code)==200:
                        print("File already exists SKIPPING: "+str(os.path.split(items['name'])[-1]))
    else:
        print('Order Failed with state: '+str(response['state']))
# download(url="https://api.planet.com/compute/ops/orders/v2/0ee9e923-59fc-4c31-8632-9882cb342708",
# local=r"C:\planet_demo\terra",errorlog=r"C:\planet_demo\errorlog.csv")
