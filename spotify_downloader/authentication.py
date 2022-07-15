import base64
import json
import logging
import os
import sys
import urllib.parse
import webbrowser

import requests
from flask import Flask, redirect, request

# Silence all flask output
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
logging.getLogger('werkzeug').disabled = True

app = Flask(__name__)


@app.route('/')
def _index():
    # Once Authorization Code Flow is complete and the user is redirected, continue the authentication process
    _initial_auth(request.args['code'])
    return redirect('https://open.spotify.com/')


def _create_secrets():
    # Create a secrets.json file to store the Spotify client_id and client_secret
    with open('secrets.json', 'w') as file:
        data = {
            'client_id': '',
            'client_secret': '',
        }
        json.dump(data, file)
    print('Please follow the steps detailed in the README.md to populate the secrets.json file with the appropriate '
          'information.')
    exit(0)


def _read_secrets():
    # Read from the secrets.json
    with open('secrets.json', 'r') as file:
        data = json.load(file)
        return data


def _initialize_webserver():
    # Initializes a Flask webserver to capture the redirect from the Spotify Authorization Code Flow
    secrets = _read_secrets()
    client_id = secrets['client_id']

    authorization_url = 'https://accounts.spotify.com/authorize'
    authorization_payload = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8080/',
        'scope': 'playlist-read-private user-library-read',
        'show_dialog': True
    }

    encoded_payload = urllib.parse.urlencode(authorization_payload)
    url = authorization_url + '?' + encoded_payload
    webbrowser.open(url)

    app.run(port=8080, debug=False)


def _initial_auth(code):
    # Use the code that was generated in the URL Redirect to request a Spotify access token and a refresh token
    secrets = _read_secrets()
    client_id = secrets['client_id']
    client_secret = secrets['client_secret']

    authentication_str = f'{client_id}:{client_secret}'
    b64_authentication_str = base64.b64encode(authentication_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_authentication_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    access_token_payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8080/'
    }

    data = requests.post('https://accounts.spotify.com/api/token', data=access_token_payload, headers=headers).json()

    with open('authentication.json', 'w') as file:
        json.dump(data, file)

    print('Authentication successful. Restart the program to unlock full functionality.')


def _refresh_access_token():
    # Using the refresh token found in the authentication.json file, request a new Spotify access token
    with open('authentication.json', 'r') as file:
        data = json.load(file)
        refresh_token = data['refresh_token']

    secrets = _read_secrets()
    client_id = secrets['client_id']
    client_secret = secrets['client_secret']

    authentication_str = f'{client_id}:{client_secret}'
    b64_authentication_str = base64.b64encode(authentication_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_authentication_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    access_token_payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    data = requests.post('https://accounts.spotify.com/api/token', data=access_token_payload, headers=headers).json()
    data['refresh_token'] = refresh_token

    with open('authentication.json', 'w') as file:
        json.dump(data, file)
        return data['access_token']


def authenticate_user():
    if not os.path.exists('secrets.json'):
        _create_secrets()
    if not os.path.exists('authentication.json'):  # Create a webserver to handle Spotify Authorization Code Flow
        _initialize_webserver()
    else:  # Open the created authentication.json file and request a new access token using the refresh token
        return _refresh_access_token()
