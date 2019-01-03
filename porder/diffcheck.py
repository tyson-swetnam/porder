#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import json
import os
import glob
import sys
from planet.api.auth import find_api_key

# Get API key and authenticate session
try:
    PL_API_KEY = find_api_key()
except Exception as e:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

l=[]


def handle_page(page, asset):
    try:
        for items in page['features']:
            for itm in items['_permissions']:
                if itm.split(':')[0]=="assets."+asset:
                    it=items.get('id')
                    #print(it)
                    l.append(it)
    except Exception as e:
        print(e)


def idl(infile, start, end, item, asset, cmin, cmax):
    if cmin is None:
        cmin = 0
    if cmax is None:
        cmax = 1
    headers = {'Content-Type': 'application/json'}

# Parse Geometry
    try:
        if infile.endswith('.geojson'):
            with open(infile) as aoi:
                aoi_resp = json.load(aoi)
                aoi_geom = aoi_resp['features'][0]['geometry']['coordinates']
        elif infile.endswith('.json'):
            with open(infile) as aoi:
                aoi_resp = json.load(aoi)
                aoi_geom = aoi_resp['config'][0]['config']['coordinates']
    except Exception as e:
        print('Could not parse geometry')
        print(e)
# Null payload structure
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
# Configure search payload
    data['filter']['config'][0]['config']['coordinates'] = aoi_geom
    data['filter']['config'][2]['config'][0]['config']['gte'] = str(start)+'T04:00:00.000Z'
    data['filter']['config'][2]['config'][0]['config']['lte'] = str(end)+'T03:59:59.999Z'
    data['filter']['config'][1]['config'][0]['config'][1]['config']['gte'] = float(cmin)
    data['filter']['config'][1]['config'][0]['config'][1]['config']['lte'] = float(cmax)
    data['filter']['config'][1]['config'][0]['config'][0]['config'] = [item]
    data['item_types'] = [item]
    data = str(data).replace("'", '"')

# Send post request
    result = SESSION.post('https://api.planet.com/data/v1/quick-search',
                           headers = headers, data = data)
    if result.status_code==408:
        sys.exit('Unexpected 408 Error might be intermittent try again in sometime')
    page = result.json()
    final_list = handle_page(page,asset)
    while page['_links'].get('_next') is not None:
        page_url = page['_links'].get('_next')
        page = SESSION.get(page_url).json()
        ids = handle_page(page,asset)
    print('Searched total IDs: '+str(len(l)))
    return set(l)


def checker(folder, typ, infile, item, asset, start, end, cmin, cmax,outfile):
    print('Now Searching....')
    allasset = idl(infile = infile, item = item, asset = asset, start = start, end = end, cmin = cmin, cmax = cmax)
    sprefix = {'PSScene4Band': '_3B', 'REOrthoTile': '_R', 'PSScene3Band': '_3B', 'PSOrthoTile': '_BGRN'}
    sval = sprefix.get(item)
    if typ == 'image':
        filenames = glob.glob1(folder,"*.tif")
        l = []
        for items in filenames:
            l.append(items.split(sval)[0])
        print('Number of items not found locally: '+str(len(set(allasset)-set(l))))
        print('IDlist written to '+str(outfile)+' with '+str(len(set(allasset)-set(l))))
        with open(outfile, "w") as f:
            for s in list(set(allasset)-set(l)):
                f.write(str(s) +"\n")
    if typ=='metadata':
        filenames=glob.glob1(folder,"*.xml")
        l=[]
        for items in filenames:
            l.append(items.split(sval)[0])
        print('Number of items not found locally: '+str(len(set(allasset).difference(set(l)))))
        print('IDlist written to '+str(outfile)+' with '+str(len(set(allasset)-set(l)))+' ids')
        with open(outfile, "w") as f:
            for s in list(set(allasset)-set(l)):
                f.write(str(s) +"\n")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Checks the difference between local files and all available Planet assets')
    parser.add_argument('--folder', help='local folder where image or metadata files are stored', required=True)
    parser.add_argument('--typ', help='File type image or metadata', required=True)
    parser.add_argument('--input', help='Input boundary to search (geojson, json)', required=True)
    parser.add_argument('--item', help='Planet Item Type', required=True)
    parser.add_argument('--asset', help='Planet asset Type', required=True)
    parser.add_argument('--start', help='Start Date YYYY-MM-DD', required=True)
    parser.add_argument('--end', help='End Date YYYY-MM-DD', required=True)
    parser.add_argument('--cmin', help='Minimum cloud cover', required=False,default=None)
    parser.add_argument('--cmax', help='Maximum cloud cover', required=False,default=None)
    parser.add_argument('--outfile', help='Full path to text file with difference ID list', required=True)

    args = parser.parse_args()

    checker(folder=args.folder,typ=args.typ,infile=args.input,
        item=args.item,asset=args.asset,start=args.start,end=args.end,
        cmin=args.cmin,cmax=args.cmax,outfile=args.outfile)
# checker(folder=r'C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Planet Tools\DiffCheck\ps4bxml',typ='metadata',
#     infile=r'C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Planet Tools\DiffCheck\geojson\Grid_3.geojson',
#     item='PSScene4Band',asset='analytic',start='2018-01-01',end='2018-08-01',cmin=None,cmax=0.3,outfile='readme.txt')
