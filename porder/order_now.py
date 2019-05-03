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
import sys
import json
import yaml
import requests
import clipboard
from prettytable import PrettyTable
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key


x = PrettyTable()

##Setup for bundles
dbundle = {'name': [], 'order_type': 'partial', 'products': [{'item_ids': [], 'item_type': [],'product_bundle': []}],'tools':[]}
dclip = {"clip": {"aoi": {"type": "Polygon","coordinates": []}}}
dtoar = {'toar': {'scale_factor': 10000}}
dzip = {"delivery":{"archive_filename":"{{name}}.zip","archive_type":"zip"}}
dcomposite ={"composite":{}}
dreproject={"reproject": {"projection": [],"kernel":[]}}
dtiff={"tiff_optimize": {"compression": []}}
demail={'notifications':{'email': True}}
daws= {"delivery":{"amazon_s3":{"bucket":[],"aws_region":[],"aws_access_key_id":[],"aws_secret_access_key":[],"path_prefix":[]}}}
dazure={"delivery":{"azure_blob_storage":{"account":[],"container":[],"sas_token":[],"storage_endpoint_suffix":[],"path_prefix":[]}}}
dgcs={"delivery": {"google_cloud_storage": {"bucket": [],"credentials": [],"path_prefix": []}}}
dbmath={"bandmath":{}}

try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
url = 'https://api.planet.com/compute/ops/orders/v2'

def order(**kwargs):
    for key,value in kwargs.items():
        if key=='name':
            dbundle['name']=value
        if key=='item':
            dbundle['products'][0]['item_type']=value
        if key=='asset':
            dbundle['products'][0]['product_bundle']=value
        if key=='idlist':
            l=[]
            if value.endswith('.csv'):
                with open(value) as f:
                    try:
                        reader = csv.reader(f)
                        for row in reader:
                            item_id=row[0]
                            if str(item_id.isalpha())=='False':
                                l.append(item_id)
                    except Exception as e:
                        print('Issue with reading: '+str(value))
            elif value.endswith('.txt'):
                with open(value) as f:
                    for line in f:
                        item_id=line.strip()
                        l.append(item_id)
            dbundle['products'][0]['item_ids'] = l
    k=dbundle
    for key,value in kwargs.items():
        if key=='op' and value!=None:
            for items in value:
                if items=='clip':
                    dbundle['tools'].append(dclip)
                elif items=='toar':
                    dbundle['tools'].append(dtoar)
                elif items=='zip':
                    dbundle.update(dzip)
                elif items=='email':
                    dbundle.update(demail)
                elif items=='aws':
                    dbundle.update(daws)
                elif items=='azure':
                    dbundle.update(dazure)
                elif items=='gcs':
                    dbundle.update(dgcs)
                elif items=='composite':
                    dbundle['tools'].append(dcomposite)
                elif items=='reproject':
                    dbundle['tools'].append(dreproject)
                elif items=='ndvi':
                    dndvi={"pixel_type": "32R","ndvi": "(b4 - b3) / (b4+b3)"}
                    dbmath['bandmath'].update(dndvi)
                elif items=='gndvi':
                    dgndvi={"pixel_type": "32R","gndvi": "(b4 - b2) / (b4+b2)"}
                    dbmath['bandmath'].update(dgndvi)
                elif items=='ndwi':
                    dndwi={"pixel_type": "32R","ndwi": "(b2 - b4) / (b4+b2)"}
                    dbmath['bandmath'].update(dndwi)
                elif items=='bndvi':
                    bndvi={"pixel_type": "32R","bndvi": "(b4-b1)/(b4+b1)"}
                    dbmath['bandmath'].update(bndvi)
                elif items=='tvi':
                    dtvi={"pixel_type": "32R","tvi": "((b4-b3)/(b4+b3)+0.5) ** 0.5"}
                    dbmath['bandmath'].update(dtvi)
                elif items=='osavi':
                    dosavi={"pixel_type": "32R","osavi": "1.16 * (b4-b3)/(b4+b3+0.16)"}
                    dbmath['bandmath'].update(dosavi)
                elif items=='evi2':
                    devi2={"pixel_type": "32R","evi2": "2.5 * (b4 - b3) / ((b4 + (2.4* b3) + 1))"}
                    dbmath['bandmath'].update(devi2)
                elif items=='sr':
                    dsr={"pixel_type": "32R","sr": "(b4/b3)"}
                    dbmath['bandmath'].update(dsr)
                elif items=='msavi2':
                    dmsavi2={"pixel_type": "32R", "msavi2": "(2 * b4 - ((2 * b4 + 1) ** 2 - 8 * (b4 - b3)) ** 0.5) / 2"}
                    dbmath['bandmath'].update(dmsavi2)
                elif items=='compression':
                    dbundle['tools'].append(dtiff)

    for key,value in kwargs.items():
        if key=='boundary' and value!=None:
                for items in k['tools']:
                    if items.get('clip'):
                        try:
                            if value.endswith('.geojson'):
                                with open(value) as aoi:
                                    aoi_resp = json.loads(aoi.read())
                                    items['clip']['aoi']['coordinates']= aoi_resp['features'][0]['geometry']['coordinates']
                            elif value.endswith('.json'):
                                with open (value) as aoi:
                                    aoi_resp=json.load(aoi)
                                    items['clip']['aoi']['coordinates']=aoi_resp['config'][0]['config']['coordinates']
                            elif value.endswith('.kml'):
                                getcoord=kml2coord(value)
                                items['clip']['aoi']['coordinates']=getcoord
                        except Exception as e:
                            print('Could not parse geometry')
        #         #print(e)
    for key,value in kwargs.items():
        if key=='aws' and value!=None:
            with open(value, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                for section in cfg:
                    k['delivery']['amazon_s3']['bucket']=cfg['amazon_s3']['bucket']
                    k['delivery']['amazon_s3']['aws_region']=cfg['amazon_s3']['aws_region']
                    k['delivery']['amazon_s3']['aws_access_key_id']=cfg['amazon_s3']['aws_access_key_id']
                    k['delivery']['amazon_s3']['aws_secret_access_key']=cfg['amazon_s3']['aws_secret_access_key']
                    k['delivery']['amazon_s3']['path_prefix']=cfg['amazon_s3']['path_prefix']
    for key,value in kwargs.items():
        if key=='azure' and value!=None:
            with open(value, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                for section in cfg:
                    k['delivery']['azure_blob_storage']['account']=cfg['azure']['account']
                    k['delivery']['azure_blob_storage']['container']=cfg['azure']['container']
                    k['delivery']['azure_blob_storage']['sas_token']=cfg['azure']['sas_token']
                    k['delivery']['azure_blob_storage']['storage_endpoint_suffix']=cfg['azure']['storage_endpoint_suffix']
                    k['delivery']['azure_blob_storage']['path_prefix']=cfg['azure']['path_prefix']
    for key,value in kwargs.items():
        if key=='gcs' and value!=None:
            with open(value, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                for section in cfg:
                    k['delivery']['google_cloud_storage']['bucket']=cfg['gcs']['bucket']
                    k['delivery']['google_cloud_storage']['credentials']=cfg['gcs']['credentials']
                    k['delivery']['google_cloud_storage']['path_prefix']=cfg['gcs']['path_prefix']
    for key,value in kwargs.items():
        if key=='compression' and value!=None:
            for items in k['tools']:
                if items.get('tiff_optimize'):
                    items['tiff_optimize']['compression']=value
    for key,value in kwargs.items():
        if key=='kernel' and value!=None:
            for items in k['tools']:
                if items.get('reproject'):
                    items['reproject']['kernel']=value
    for key,value in kwargs.items():
        if key=='projection' and value!=None:
            for items in k['tools']:
                if items.get('reproject'):
                    items['reproject']['projection']=value

    bnames=[]
    for items in dbmath['bandmath']:
        if items !='pixel_type':
            bnames.append(items)

    rg=len(bnames)
    if rg<6:
        dck=['b'+str(el) for el in range(1,rg+1)] #get serialized bands
        plist=[list(pair) for pair in zip(dck, bnames)]
        x.field_names = ["Band Number", "Band Name"]
        for items in plist:
            i=items[0]
            f=items[1]
            x.add_row([i,f])
            dbmath['bandmath'][i]=dbmath['bandmath'].pop(f)
    else:
        print('You can only use upto 5 bands')
        sys.exit()

    if len(dbmath['bandmath'])>0:
        k['tools'].append(dbmath)
    json_data = json.dumps(k)
    payload = json_data
    if len(bnames):
        print('\n')
        print(x)
        print('\n')

    # print('')
    #print(dbmath)

    #print(payload)
    headers = {'content-type': 'application/json',
               'cache-control': 'no-cache'}
    response = requests.request('POST', url, data=payload, headers=headers,
                                auth=(PL_API_KEY, ''))
    if response.status_code==202:
        content = response.json()
        try:
            clipboard.copy(str(url) + '/' + str(content['id']))
            print('Order created at '+str(url) + '/' + str(content['id']+' and url copied to clipboard'))
        except Exception:
            print('Headless Setup: Order created at '+str(url) + '/' + str(content['id']))
    elif response.status_code==400:
        print('Failed with response: Bad request')
    elif response.status_code==401:
        print('Failed with response: Forbidden')
    elif response.status_code==409:
        print('Failed with response: MaxConcurrency')
    else:
        print(response.text)
