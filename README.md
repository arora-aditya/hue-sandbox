# hue-music

## Current Functionality:
- Changes color of Hue lights based on dominant album art color

## Setup
- initialize `virtualenv`: `python3 -m venv /path/to/new/virtual/environment`
- activate `virtualenv`: `cd /path/to/new/virtual/environment & source bin/activate`
- install dependencies: `pip3 install -r requirements.txt`
- Get Client Secret and Client ID from Spotify [here](https://developer.spotify.com/dashboard/applications) and store them in a `.env` file as:
```
CLIENT_ID = '978287e6a3394728b04ce529b6934bc5',
CLIENT_SECRET = '127cbd41d3314564b8f046024c7e2e64'
```
- Change username in `base.py` line 43 to your spotify username
- Run: `python3 base.py`
