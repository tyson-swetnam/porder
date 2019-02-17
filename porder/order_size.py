import requests
import time
import progressbar
import json
import os
import sys
from retrying import retry
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


#Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

#Get the redirects and ordersize
@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def parsesize(url):
    result=SESSION.get(url)
    mfsize=[]
    mfname=[]
    if result.status_code==200:
        r=result.content
        inp=json.loads(r)
        for things in inp['files']:
            mfname.append(things['path'])
            mfsize.append(things['size'])
        return (len(mfname),sum(mfsize))
            #time.sleep(0.3)
        #print('Total of '+str(len(fname)/3)+' items has filesize of '+str(humansize(sum(sz))))
    elif result.status_code == 429:
        raise Exception("rate limit error")
    elif result.status_code !=(429,200):
        return (result.status_code)

    #
def ordersize(url):
    response=SESSION.get(url).json()
    print("Polling ...")
    while response['state']=='running' or response['state']=='starting':
        bar = progressbar.ProgressBar()
        for z in bar(range(60)):
            time.sleep(1)
        response=SESSION.get(url).json()
    sz=[]
    fname=[]
    if response['state']=='success':
        for items in response['_links']['results']:
            if items['name'].endswith('manifest.json'):
                url=(items['location'])
                #print(url)
                try:
                    name,size=parsesize(url)
                    sz.append(size)
                    fname.append(name)
                except:
                    error_code=parsesize(url)
                    print('Order has expired or exited with error '+str(error_code))
                    sys.exit()
        print('Total of '+str(sum(fname)/3)+' items has filesize of '+str(humansize(sum(sz))))

    else:
        print('Order Failed with state: '+str(response['state']))

#ordersize(url='https://api.planet.com/compute/ops/orders/v2/6433d78f-c695-4763-b68b-01f2ef2ccb9c')
