#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
import csv
import sys
from shapely.geometry import shape
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway=os.path.dirname(os.path.realpath(__file__))

#Create an empty geojson template
temp={"coordinates":[],"type":"Polygon"}
try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')


def handle_page(page,asset,num,outfile,gmain,ovp):
    num=int(num)
    [head,tail]=os.path.split(outfile)
    if num<250:
        try:
            n=0
            with open(outfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id"], delimiter=',')
                writer.writeheader()
            open(os.path.join(head,tail.split('.')[0]+'.txt'),'w')
            for items in page['features']:
                for itm in items['_permissions']:
                    if itm.split(':')[0]=="assets."+asset and n<num:
                        it=items.get('id')
                        if items['geometry']['type']=="Polygon":
                            bounds=items['geometry']['coordinates']
                            temp['coordinates']=bounds
                            geom2=shape(temp)
                            intersect=min(gmain,geom2).intersection(max(gmain,geom2))
                            #print('ID '+str(it)+' has percentage overlap: '+str(intersect.area/geommain.area*100))
                            if (intersect.area/gmain.area)*100>=ovp:
                                # print('ID '+str(it)+' has percentage overlap: '+str(intersect.area/geom2.area*100))
                                n=n+1
                                with open(outfile,'a') as csvfile:
                                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                                    writer.writerow([it])
                                with open(os.path.join(head,tail.split('.')[0]+'.txt'), 'a') as the_file:
                                    the_file.write(it+'\n')
            num_lines = sum(1 for line in open(os.path.join(head,tail.split('.')[0]+'.txt')))
            print('Total number of assets written to '+str(os.path.join(head,tail.split('.')[0]+'.txt')+' ===> '+str(num_lines)))
            sys.exit()
        except Exception as e:
            print(e)
    else:
        try:
            n=0
            for items in page['features']:
                for itm in items['_permissions']:
                    if itm.split(':')[0]=="assets."+asset and n<num:
                        it=items.get('id')
                        if items['geometry']['type']=="Polygon":
                            bounds=items['geometry']['coordinates']
                            temp['coordinates']=bounds
                            geom2=shape(temp)
                            intersect=min(gmain,geom2).intersection(max(gmain,geom2))
                            #print('ID '+str(it)+' has percentage overlap: '+str(intersect.area/geommain.area*100))
                            if (intersect.area/gmain.area)*100>=ovp:
                                # print('ID '+str(it)+' has percentage overlap: '+str(intersect.area/geom2.area*100))
                                n=n+1
                                with open(outfile,'a') as csvfile:
                                    writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                                    writer.writerow([it])
            data=csv.reader(open(outfile).readlines()[1: num+1])

            with open(outfile, "wb") as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
            open(os.path.join(head,tail.split('.')[0]+'.txt'), 'w')
            dat=open(outfile).readlines()
            with open(os.path.join(head,tail.split('.')[0]+'.txt'), 'a') as the_file:
                for row in dat:
                    the_file.write(row)
        except Exception as e:
            print(e)
def idl(infile,start,end,item,asset,num,cmin,cmax,outfile,ovp):
    [head,tail]=os.path.split(outfile)
    if cmin==None:
        cmin=0
    if cmax==None:
        cmax=1
    if ovp==None:
        ovp=1
    with open(outfile,'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id"], delimiter=',')
        writer.writeheader()
    open(outfile, 'w')
    headers = {'Content-Type': 'application/json'}
    PL_API_KEY = read_planet_json()['key']

##Parse Geometry
    try:
        if infile.endswith('.geojson'):
            with open(infile) as aoi:
                aoi_resp = json.load(aoi)
                aoi_geom = aoi_resp['features'][0]['geometry']['coordinates']
        elif infile.endswith('.json'):
            with open (infile) as aoi:
                aoi_resp=json.load(aoi)
                aoi_geom=aoi_resp['config'][0]['config']['coordinates']
        elif infile.endswith('.kml'):
            getcoord=kml2coord(infile)
            aoi_geom=getcoord
    except Exception as e:
        print('Could not parse geometry')
        print(e)
## Null payload structure
    data = {'filter': {'type': 'AndFilter',
            'config': [{'type': 'GeometryFilter', 'field_name': 'geometry',
            'config': {'type': 'Polygon', 'coordinates': []}},
            {'type': 'OrFilter', 'config': [{'type': 'AndFilter',
            'config': [{'type': 'StringInFilter', 'field_name': 'item_type'
            , 'config': []}, {'type': 'RangeFilter',
            'field_name': 'cloud_cover', 'config': {'gte': [],
            'lte': []}}, {'type': 'RangeFilter',
            'field_name': 'sun_elevation', 'config': {'gte': 0,
            'lte': 90}}]}]}, {'type': 'OrFilter',
            'config': [{'type': 'DateRangeFilter', 'field_name': 'acquired'
            , 'config': {'gte': [],
            'lte': []}}]}]},
            'item_types': []}
## Configure search payload
    data['filter']['config'][0]['config']['coordinates'] = aoi_geom
    data['filter']['config'][2]['config'][0]['config']['gte'] = str(start)+'T04:00:00.000Z'
    data['filter']['config'][2]['config'][0]['config']['lte'] = str(end)+'T03:59:59.999Z'
    data['filter']['config'][1]['config'][0]['config'][1]['config']['gte'] = float(cmin)
    data['filter']['config'][1]['config'][0]['config'][1]['config']['lte'] = float(cmax)
    data['filter']['config'][1]['config'][0]['config'][0]['config'] = [item]
    data['item_types'] = [item]
    data = str(data).replace("'", '"')
    temp['coordinates']=aoi_geom
    gmain=shape(temp)
## Send post request
    querystring = {"strict":"true"}
    result = requests.post('https://api.planet.com/data/v1/quick-search',
                           headers=headers, data=data, params=querystring,
                           auth=(PL_API_KEY, ''))
    page=result.json()
    final_list = handle_page(page,asset,num,outfile,gmain,ovp)
    while page['_links'].get('_next') is not None:
        page_url = page['_links'].get('_next')
        page = SESSION.get(page_url).json()
        ids = handle_page(page,asset,num,outfile,gmain,ovp)
    num_lines = sum(1 for line in open(os.path.join(head,tail.split('.')[0]+'.txt')))
    print('Total number of assets written to '+str(os.path.join(head,tail.split('.')[0]+'.txt')+' ===> '+str(num_lines)))
