# -*- coding: utf-8 -*-

"""
unmollom.util

some helper functions to solve the mollom captchas
"""

import re
from bs4 import BeautifulSoup
from unmollom.exceptions import NoMollomTagsFoundException

# some words the speech recognition constantly gets wrong
# "x ray" for example should be one word
RECOGNITION_FAILS = {
    'x ray' : 'x-ray',
    'i5' : 'alpha',
    'lulu' : 'zulu',
    'key bank' : 'quebec',
    'dick' : 'quebec',
    'hilo' : 'kilo'
}

def improve_speech_recognition(speech):
    speech = str(speech).lower()
    for k in RECOGNITION_FAILS:
        speech = speech.replace(k, RECOGNITION_FAILS[k])
    return speech

def extract_mollom_audio_file(source):
    soup = BeautifulSoup(source)
    # lets check every image and search for the mollom url
    # they're something like http://ip/v1/captcha/SOMEHASH.png
    for img in soup.findAll('img'):
        matches = re.match('https?://[^/]+/v[0-9]+/captcha/[^.]+\.png', img['src'])
        if matches:
            return img['src'].replace('.png', '.mp3')
    raise NoMollomTagsFoundException("No Mollom found")

def build_captcha(speech):
    if not speech:
        return ''
    speech = improve_speech_recognition(speech)
    # mollom wants the first character of each word
    captcha =  ''.join( [ x[0] for x in speech.split(' ') ] )
    return captcha
