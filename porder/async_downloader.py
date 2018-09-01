import requests
import time
import progressbar
import json
import os
import sys
import csv
from pySmartDL import SmartDL
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#Get Planet API and Authenticate SESSION
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

# To get redirect link
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
def asyncdownload(url,local,errorlog):
    with open(errorlog,'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
        writer.writeheader()
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
                    print("Downloading: " + str(local_path))
                    obj = SmartDL(redirect_url, local_path)
                    obj.start()
                    path = obj.get_dest()
                else:
                    if int(result.status_code)!=200:
                        print("Encountered error with code: " + str(result.status_code)+' for '+str(os.path.split(items['name'])[-1]))
                        with open(errorlog,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([str(os.path.split(items['name'])[-1])])
                        csvfile.close()
                    elif int(result.status_code)==200:
                        print("File already exists SKIPPING: "+str(os.path.split(items['name'])[-1]))
    else:
        print('Order Failed with state: '+str(response['state']))
##download(url="https://api.planet.com/compute/ops/orders/v2/0ee9e923-59fc-4c31-8632-9882cb342708",
##         local=r"C:\planet_demo\terra",errorlog=r"C:\planet_demo\errorlog.csv")
