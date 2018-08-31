import csv
import json
import requests
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
##Setup for bundles
dbundle = {'name': [], 'products': [{'item_ids': [], 'item_type': [],'product_bundle': []}],'tools':[]}
dclip = {"clip": {"aoi": {"type": "Polygon","coordinates": []}}}
dtoar = {'toar': {'scale_factor': 10000}}
dzip = {"delivery":{"archive_filename":"{{name}}.zip","archive_type":"zip"}}
dcomposite ={"composite":{}}
dreproject={"reproject": {"projection": [],"kernel":[]}}
dtiff={"tiff_optimize": {"compression": []}}
demail={'notifications':{'email': True}}

try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
url = 'https://api.planet.com/compute/ops/orders/v2'

def order(**kwargs):
    for key,value in kwargs.iteritems():
        if key=='op':
            for items in value:
                if items=='clip':
                    dbundle['tools'].append(dclip)
                elif items=='toar':
                    dbundle['tools'].append(dtoar)
                elif items=='zip':
                    dbundle.update(dzip)
                elif items=='email':
                    dbundle.update(demail)
                elif items=='composite':
                    dbundle['tools'].append(dcomposite)
                elif items=='reproject':
                    dbundle['tools'].append(dreproject)
                elif items=='compression':
                    dbundle['tools'].append(dtiff)
        if key=='name':
            dbundle['name']=value
        if key=='item':
            dbundle['products'][0]['item_type']=value
        if key=='asset':
            dbundle['products'][0]['product_bundle']=value
        if key=='idlist':
            l=[]
            with open(value) as f:
                reader = csv.reader(f)
                first=next(reader)[0]
                if str(first.isalpha())=='True':
                    next(reader)
                    for row in reader:
                        item_id=row[0]
                        l.append(item_id)
                else:
                     for row in reader:
                        item_id=row[0]
                        l.append(item_id)
            dbundle['products'][0]['item_ids'] = l
    k=dbundle
    for key,value in kwargs.iteritems():
        if key=='boundary' and value!=None:
                for items in k['tools']:
                    if items.get('clip'):
                        try:
                            if value.endswith('.geojson'):
                                with open(value) as aoi:
                                    aoi_resp = json.load(aoi)
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
        if key=='projection' and value!=None:
            for items in k['tools']:
                if items.get('reproject'):
                    items['reproject']['projection']=value
        if key=='kernel' and value!=None:
            for items in k['tools']:
                if items.get('reproject'):
                    items['reproject']['kernel']=value
        if key=='compression' and value!=None:
            for items in k['tools']:
                if items.get('tiff_optimize'):
                    items['tiff_optimize']['compression']=value
        #         #print(e)

    json_data = json.dumps(k)
    payload = json_data
    #print(payload)
    headers = {'content-type': 'application/json',
               'cache-control': 'no-cache'}
    response = requests.request('POST', url, data=payload, headers=headers,
                                auth=(PL_API_KEY, ''))
    if response.status_code==202:
        content = response.json()
        print 'Order created at '+str(url) + '/' + str(content['id'])
    else:
        print(response.text)
