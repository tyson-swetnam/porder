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


#!/usr/bin/env python

import multiprocessing
import os
import csv
import requests
import time
import progressbar
import json
import sys
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
        if r.status_code == 429:
            raise Exception("rate limit error")
        if 300 <= r.status_code < 400:
            return r.headers['location']
        else:
            return 'no redirect'
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'
########################################################################
class MultiProcDownloader(object):
    """
    Downloads urls with Python's multiprocessing module
    """

    #----------------------------------------------------------------------
    def __init__(self, urls):
        """ Initialize class with list of urls """
        self.urls = urls

    #----------------------------------------------------------------------
    def run(self):
        """
        Download the urls and waits for the processes to finish
        """
        jobs = []
        for url in self.urls:
            process = multiprocessing.Process(target=self.worker, args=(url,))
            jobs.append(process)
            process.start()
        for job in jobs:
            job.join()

    #----------------------------------------------------------------------
    def worker(self, url):
        """
        The target method that the process uses tp download the specified url
        """
        try:
            urlcheck=url.split('|')[0]
            fullpath=url.split('|')[1]
            [head,tail]=os.path.split(fullpath)
            msg = "Starting download of %s" % fullpath.split('/')[-1]
            if not os.path.exists(head):
                os.makedirs(head)
            os.chdir(head)
            if not os.path.isfile(fullpath):
                print msg, multiprocessing.current_process().name
                r = requests.get(urlcheck)
                with open(fullpath, "wb") as f:
                    f.write(r.content)
            else:
                print("File already exists skipping "+str(tail))
        except Exception as e:
            print(e)
            print('Issues with file: '+str(fullpath))

def funct(url,final,ext):
    if not os.path.exists(final):
        os.makedirs(final)
    os.chdir(final)
    urls=[]
    response=SESSION.get(url).json()
    print("Polling with exponential backoff..")
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
                local_path=os.path.join(final,str(os.path.split(items['name'])[-1]))
                if ext is None:
                    urls.append(str(redirect_url)+'|'+local_path)
                elif ext is not None:
                    if local_path.endswith(ext):
                        urls.append(str(redirect_url)+'|'+local_path)
    else:
        print('Order Failed with state: '+str(response['state']))
    downloader = MultiProcDownloader(urls)
    downloader.run()

#----------------------------------------------------------------------
if __name__ == "__main__":
    funct(url=sys.argv[1],final=os.path.normpath(sys.argv[2]),ext=sys.argv[3])
    # funct(url='https://api.planet.com/compute/ops/orders/v2/4ebfa89e-dc59-41cc-ad82-dbad2b5375b2',final=r'C:\planet_demo',ext='.zip')
    # downloader = MultiProcDownloader(urls)
    # downloader.run()
