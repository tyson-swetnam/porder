import getpass
import json

import jwt
import requests

token = response.json()['token']
print(jwt.decode(token, options={'verify_signature': False}))

# Initialize Spotify Credentials


def planet_init():
    try:
        url = "https://api.planet.com/auth/v1/experimental/public/users/authenticate"
        payload = json.dumps({
            "email": input("Email address:  "),
            "password": getpass.getpass("Password:  ")
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            with open(os.path.join(expanduser("~"), "planet.auth.json"), "w") as outfile:
                json.dump(response.json(), outfile)
        else:
            print(f'Failed with status code {response.status_code}')
    except Exception as error:
        print(error)


planet_init()
