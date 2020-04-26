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
import glob
from retrying import retry
from pySmartDL import SmartDL
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
from datetime import datetime


#Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


i=1

@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def check_for_redirects(url):
    try:
        r = SESSION.get(url, allow_redirects=False, timeout=0.5)
        if 300 <= r.status_code < 400:
            return r.headers['location']
        elif r.status_code==429:
            raise Exception("rate limit error")
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'
    except requests.HTTPError as e:
        if r.status_code == 429:  # Too many requests
            raise Exception("rate limit error")


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def downonly(redirect_url,local_path,ext,items,ulength):
    global i
    result=SESSION.get(redirect_url)
    if not os.path.exists(local_path) and result.status_code==200:
        if ext is not None:
            if local_path.endswith(ext):
                print(str(ulength-i)+" remaining ==> Downloading: " + str(local_path))
                i=i+1
                obj = SmartDL(redirect_url, local_path)
                obj.start()
                path = obj.get_dest()
        elif ext is None:
            print(str(ulength-i)+" remaining ==> Downloading: " + str(local_path))
            i=i+1
            obj = SmartDL(redirect_url, local_path)
            obj.start()
            path = obj.get_dest()
    elif result.status_code==429:
        raise Exception("rate limit error")
    else:
        if int(result.status_code)!=200:
            print("Encountered error with code: " + str(result.status_code)+' for '+str(os.path.split(items['name'])[-1]))
        elif int(result.status_code)==200:
            print("Checking "+str(ulength-i)+" remaining ==> "+"File already exists SKIPPING: "+str(os.path.split(local_path)[-1]))
            i=i+1

def get_session_response(url):
    response=SESSION.get(url).json()
    print("Polling ...")
    while response['state']=='queued' or response['state']=='running' or response['state']=='starting':
        bar = progressbar.ProgressBar()
        for _ in bar(range(60)):
            time.sleep(1)
        response=SESSION.get(url).json()

    return response

size_list=[]
# Get the redirects and download
def asyncdownload(url,local,ext):
    filenames = glob.glob1(local,'*')
    response = get_session_response(url)
    if response['state']=='success' or response['state']=='partial':
        print('Order completed with status: '+str(response['state']))
        ulength=len(response['_links']['results'])-len(filenames)
        print('')
        for files in response['_links']['results']:
            if files['name'].endswith('manifest.json'):
                time.sleep(0.2)
                resp=SESSION.get(files['location']).json()
                for things in resp['files']: size_list.append(things['size'])
        print('Estimated Download Size for order: {}'.format(humansize(sum(size_list))))
        print('')
        for index, items in enumerate(response['_links']['results']):
            expiration_time = datetime.strptime(items['expires_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            if datetime.now() > expiration_time:
                print('The URL links have expired.  Refreshing.')
                response[:] = get_session_response(url)
                if response['state']=='success' or response['state']=='partial':
                    items = response['_links']['results'][index]
                else:
                    print('Order Failed with state: '+str(response['state']))
                    return
            url=(items['location'])
            name=(items['name'])
            if name.endswith('manifest.json'):
                time.sleep(0.2)
                resp=SESSION.get(url)
                if int(resp.status_code)==200:
                    r=resp.content
                    inp=json.loads(r)
                    for things in inp['files']:
                        try:
                            local_path=os.path.join(local,things['path'].split('/')[-1])
                        except Exception as e:
                            print(e)
                else:
                    print(resp.status_code)
            else:
                local_path=os.path.join(local,str(os.path.split(items['name'])[-1]))
            filenames=[os.path.join(local,files) for files in filenames]
            if not local_path in filenames:
                url_to_check = url if url.startswith('https') else "http://%s" % url
                redirect_url = check_for_redirects(url_to_check)
                if redirect_url.startswith('https'):
                        try:
                            downonly(redirect_url,local_path,ext,items,ulength)
                        except Exception as e:
                            print(e)
                        except (KeyboardInterrupt, SystemExit) as e:
                            print('\n'+'Program escaped by User')
                            sys.exit()
            else:
                print("File already exists SKIPPING: "+str(local_path))
    else:
        print('Order Failed with state: '+str(response['state']))

##download(url="https://api.planet.com/compute/ops/orders/v2/0ee9e923-59fc-4c31-8632-9882cb342708",
##         local=r"C:\planet_demo\terra",errorlog=r"C:\planet_demo\errorlog.csv")
