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

import requests
import json
import os
import sys
from planet.api.auth import find_api_key

try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

#Check running orders
def handle_page(page):
    i=0
    try:
        for items in page['orders']:
            if items['state']=='running':
                i=i+1
        return i
    except Exception as e:
        print(e)

#Check for concurrenct orders that are running
runlist=[]
def conc():
    print('Checking on all running orders...')
    result = SESSION.get('https://api.planet.com/compute/ops/orders/v2')
    page=result.json()
    final_list=handle_page(page)
    while page['_links'].get('next') is not None:
        try:
            page_url = page['_links'].get('next')
            result = SESSION.get(page_url)
            page=result.json()
            ids = handle_page(page)
            runlist.append(ids)
        except Exception as e:
            pass
    print('Running '+str(sum(runlist))+' orders')
    return sum(runlist)
conc()
