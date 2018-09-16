import os
import json
import requests
from requests.auth import HTTPBasicAuth

def quota():
    '''Print allocation and remaining quota in Sqkm.'''
    try:
        fname = os.path.join(os.path.expanduser('~'), '.planet.json')
        contents = {}
        if os.path.exists(fname):
            with open(fname, 'r') as fp:
                contents = json.loads(fp.read())
        else:
            raise IOError('Escape to End and Initialize')
        if not len(contents) !=0:
            raise IOError('Escape to End and Initialize')
        else:
            k = contents['key']
        main = requests.get(
            'https://api.planet.com/auth/v1/' +
            'experimental/public/my/subscriptions',
            auth=HTTPBasicAuth(
                k, ''))
        if main.status_code == 200:
            content = main.json()
            for item_id in content:
                print(" ")
                print(
                    'Allocation Name: %s'
                    % item_id['organization']['name'])
                print(
                    'Allocation active from: %s'
                    % item_id['active_from'].split("T")[0])
                print(
                    'Quota Enabled: %s'
                    % item_id['quota_enabled'])
                print(
                    'Total Quota in SqKm: %s'
                    % item_id['quota_sqkm'])
                print(
                    'Total Quota used: %s'
                    % item_id['quota_used'])
                if (item_id['quota_sqkm'])is not None:
                    leftquota = (float(
                        item_id['quota_sqkm'] - float(item_id['quota_used'])))
                    print(
                        'Remaining Quota in SqKm: %s' % leftquota)
                else:
                    print('No Quota Allocated')
                print('')
        else:
            print('Failed with exception code: ' + str(
                main.status_code))

    except IOError:
        print('Initialize client or provide API Key')
quota()
