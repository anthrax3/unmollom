# -*- coding: utf-8 -*-

"""
unmollom.voice_recognition


"""

import requests
import json
from exceptions import RecognitionException, CommunicationException
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

class GoogleSpeechRecognition(object):
    def __init__(self):
        self.samplerate = '48000'
        self.url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
        self.headers={'Content-Type': 'audio/x-flac; rate=%s' % self.samplerate, 'User-Agent':'Mozilla/5.0'}

    def recognize(self, in_file_name, format='mp3'):
        flac = self.convert_to_flac(in_file_name, format)
        result = self.send_request(self.url, flac, self.headers)
        if result.ok:
            try:
                response = json.loads(result.text)
                if response['status'] == 0 and len(response['hypotheses']) > 0:
                    hypo = response['hypotheses'][0]
                    return {'confidence' : hypo['confidence'], 'text' : hypo['utterance']}
                else:
                    raise RecognitionException("Voice recognition failed")
            except ValueError:
                raise RecognitionException("Speech Recognition Server did not return a json")
            except KeyError: 
                raise RecognitionException("Server returned the wrong json structure")
        else:
            raise CommunicationException("Google does not like you!: " + result.text)

    def convert_to_flac(self, in_file_name, format):
        if format == 'flac':
            return open(in_file_name,'rb').read()
        converted = NamedTemporaryFile('rb')
        mp3 = AudioSegment.from_mp3(in_file_name)
        mp3.export(converted.name, format='flac', parameters=['-ar', self.samplerate])
        flac = converted.read()
        converted.close()
        return flac

    def send_request(self, url, data, headers):
        """
        returns a result object with:
            result.ok   = True/False 
            result.text = server response text
        """
        return  requests.post(url, data=data, headers=headers)

def recognize_file(fname, format='mp3'):
    return GoogleSpeechRecognition().recognize(fname, format)

def recognize(data, format='mp3'):
    input_file = NamedTemporaryFile('wb')
    input_file.write(data)
    input_file.flush()
    ret = recognize_file(input_file.name, format)
    input_file.close()
    return ret
