# -*- coding: utf-8 -*-

"""
unmollom.util


"""

from bs4 import BeautifulSoup
from unmollom.exceptions import NoMollomTagsFoundException

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
    speech = str(speech)
    # mollom wants the first character of each word
    captcha =  ''.join( [ x[0] for x in speech.split(' ') ] ).lower()
    return captcha