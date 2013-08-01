# -*- coding: utf-8 -*-

"""
unmollom.util


"""

from bs4 import BeautifulSoup
from unmollom.exceptions import NoMollomTagsFoundException

# some words google gets constantly wrong
RECOGNITION_FAILS = {
    'x ray' : 'x-ray',
    'i5' : 'alpha',
    'lulu' : 'zulu',
    'key bank' : 'quebec',
    'dick' : 'quebec',
    'hilo' : 'kilo'
}

def improve_speech_recognition(speech):
    speech = str(speech)
    for k in RECOGNITION_FAILS:
        speech = speech.replace(k, RECOGNITION_FAILS[k])
    return speech

def extract_mollom_audio_file(source):
    soup = BeautifulSoup(source)
    mollom_span = soup.find('span', attrs={'class' : 'mollom-audio-captcha'})
    if mollom_span:
        return mollom_span.find('object')['data']
    else:
        raise NoMollomTagsFoundException("No Mollom found")

def build_captcha(speech):
    if not speech:
        return ''
    speech = improve_speech_recognition(speech)
    # mollom wants the first character of each word
    captcha =  ''.join( [ x[0] for x in speech.split(' ') ] ).lower()
    return captcha