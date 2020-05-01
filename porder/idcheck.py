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

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import csv
import os
import pyproj
from functools import partial
from planet import api
from planet.api import filters
from planet.api.auth import find_api_key
from shapely.geometry import shape
from shapely.ops import transform


try:
    PL_API_KEY = find_api_key()
except Exception as e:
    print('Failed to get Planet Key')
    sys.exit()

client = api.ClientV1(PL_API_KEY)


temp={"coordinates":[],"type":"Polygon"}
aoi = {
  "type": "Polygon",
  "coordinates": []
}

# Area lists
ar = []
far = []

# get coordinates list depth
def list_depth(dic, level = 1):
    counter = 0
    str_dic = str(dic)
    if "[[[[" in str_dic:
        counter += 1
    return(counter)


# Function to use the client and then search
def idc(idlist,item,asset,geometry):
    if geometry is not None:
        try:
            if geometry.endswith('.geojson'):
                with open(geometry) as aoi:
                    aoi_resp = json.load(aoi)
                    if list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==0:
                        aoi_geom = aoi_resp['features'][0]['geometry']['coordinates']
                    elif list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==1:
                        aoi_geom = aoi_resp['features'][0]['geometry']['coordinates'][0]
                    else:
                        print('Please check GeoJSON: Could not parse coordinates')
        except Exception as e:
            print('Could not parse geometry')
            print(e)
        l=[]
        stbase={'config': [], 'field_name': 'id', 'type': 'StringInFilter'}
        with open(idlist) as f:
            try:
                reader = csv.reader(f)
                for row in reader:
                    item_id=row[0]
                    if str(item_id.isalpha())=='False':
                        l.append(item_id)
            except Exception as e:
                print(e)
        stbase['config']=l
        temp['coordinates']=aoi_geom
        sgeom=filters.geom_filter(temp)
        aoi_shape = shape(temp)
        asset_filter=filters.permission_filter('assets.'+str(asset)+':download')
        and_filter = filters.and_filter(asset_filter,stbase)
        item_types = [item]
        req = filters.build_search_request(and_filter, item_types)
        res = client.quick_search(req)
        num_lines = sum(1 for line in open(os.path.join(idlist.split('.')[0]+'.csv')))
        n=1
        print('Checking assets in idlist...')
        for things in res.items_iter(num_lines): # A large number as max number to check against
            itemid=things['id']
            #print('Processing '+str(n)+' of '+str(num_lines))
            n=n+1
            footprint = things["geometry"]
            s = shape(footprint)
            if item.startswith('SkySat'):
                epsgcode='3857'
            else:
                epsgcode=things['properties']['epsg_code']
            if aoi_shape.area>s.area:
                intersect=(s).intersection(aoi_shape)
            elif s.area>=aoi_shape.area:
                intersect=(aoi_shape).intersection(s)
            proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),
                pyproj.Proj(init='epsg:'+str(epsgcode)))
            if transform(proj,aoi_shape).area>transform(proj,s).area:
                ar.append(transform(proj,intersect).area/1000000)
                far.append(transform(proj,s).area/1000000)
            elif transform(proj,s).area>transform(proj,aoi_shape).area:
                ar.append(transform(proj,intersect).area/1000000)
                far.append(transform(proj,s).area/1000000)
    elif geometry is None:
        l=[]
        stbase={'config': [], 'field_name': 'id', 'type': 'StringInFilter'}
        with open(idlist) as f:
            try:
                reader = csv.reader(f)
                for row in reader:
                    item_id=row[0]
                    if str(item_id.isalpha())=='False':
                        l.append(item_id)
            except Exception as e:
                print(e)
        stbase['config']=l
        asset_filter=filters.permission_filter('assets.'+str(asset)+':download')
        and_filter = filters.and_filter(asset_filter,stbase)
        item_types = [item]
        req = filters.build_search_request(and_filter, item_types)
        res = client.quick_search(req)
        num_lines = sum(1 for line in open(os.path.join(idlist.split('.')[0]+'.csv')))
        n=1
        print('Checking assets in idlist...')
        for things in res.items_iter(num_lines): # A large number as max number to check against
            itemid=things['id']
            #print('Processing '+str(n)+' of '+str(num_lines))
            n=n+1
            footprint = things["geometry"]
            s = shape(footprint)
            if item.startswith('SkySat'):
                epsgcode='3857'
            else:
                epsgcode=things['properties']['epsg_code']
            proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),
                pyproj.Proj(init='epsg:'+str(epsgcode)))
            far.append(transform(proj,s).area/1000000)

    print('\n'+'Total estimated cost to quota: ' + str("{:,}".format(round(sum(far)))) + ' sqkm')
    if not len(ar)==0:
        print('Total estimated cost to quota if clipped: ' + str("{:,}".format(round(sum(ar)))) + ' sqkm')
# idc(idlist=r'C:\planet_demo\opencadover.csv',item='PSScene4Band',asset='analytic',geometry=r'C:\Users\samapriya\Downloads\sfo.geojson')

