from phue import Bridge
import sys
import os
import spotipy
import spotipy.util as util
import pprint as pp
from PIL import Image
import requests
from io import BytesIO
from time import sleep
from math import pow
from random import randint
import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from dotenv import load_dotenv
load_dotenv()
from os import getenv
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")


def EnhanceColor(normalized):
    if normalized > 0.04045:
        return pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceColor(gNorm)
    bFinal = EnhanceColor(bNorm)

    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)

        return (xFinal, yFinal)
def get_current_track(
        CLIENT_ID=CLIENT_ID,
        CLIENT_SECRET=CLIENT_SECRET,
        REDIRECT_URI = 'http://arora-aditya.com',
        SCOPE = 'user-read-currently-playing',
        username = 'arora_aditya'):
    '''
    Get information for current playing song
    '''
    try:
        token = util.prompt_for_user_token(
            username,
            SCOPE,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI
        )
    except (AttributeError, JSONDecodeError):
        token =  util.prompt_for_user_token(
                                    username,
                                    SCOPE,
                                    client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri=REDIRECT_URI
                                )

    if token:
        sp = spotipy.Spotify(auth=token)
        # print(sp.me())
        current_track = sp.current_user_playing_track()
        albumArt = ''
        songName = ''
        if current_track is not None:
            return current_track
        else:
            print('Spotify is not running.')

def get_wait_time(current_track):
    return 0.001 *(current_track['item']['duration_ms'] -
                current_track['progress_ms'])

def get_album_art(current_track):
    albumArt = current_track['item']['album']['images'][0]['url']

    response = requests.get(albumArt)
    return response

def get_dominant_color(response):
    img = Image.open(BytesIO(response.content))
    NUM_CLUSTERS = 5


    im = img
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    r,g,b = peak[0], peak[1], peak[2]
    return r,g,b

if __name__ == '__main__':
    bridge = Bridge('192.168.0.10')
    bridge.connect()

    lightstrip = bridge.get_light_objects('name')['Lightstrip']
    current_track = get_current_track()
    while current_track['is_playing'] == True:
        current_track = get_current_track()
        seconds = get_wait_time(current_track)
        pp.pprint(current_track['item']['name'])
        response = get_album_art(current_track)
        r,g,b = get_dominant_color(response)
        xy = RGBtoXY(r,g,b)
        lightstrip.on = True
        lightstrip.transitiontime = seconds/10
        lightstrip.brightness = randint(150,255)
        lightstrip.xy = xy
        print(xy)
        sleep(max(seconds/10, 2))
