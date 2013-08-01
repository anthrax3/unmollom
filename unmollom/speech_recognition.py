# -*- coding: utf-8 -*-

"""
unmollom.speech_recognition

a python wrapper for Google's speech recognition API. 
this module can be used independently of the remaining unmollom code

:copyright: (c) 2013 by Flurin Rindisbacher.
:license: BSD 2-Clause, see LICENSE for more details.
"""

import requests
import json
import wave
from exceptions import RecognitionException, CommunicationException, AudioFormatException
from tempfile import NamedTemporaryFile
from pydub import AudioSegment


class GoogleSpeechRecognition(object):
    def __init__(self):
        self.samplerate = '48000'
        self.url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
        self.headers={'Content-Type': 'audio/x-flac; rate=%s' % self.samplerate, 'User-Agent':'Mozilla/5.0'}

    def recognize(self, audio_file_name, format='mp3'):
        flac = self.convert_to_flac(audio_file_name, format)
        result = self.send_request(self.url, flac, self.headers)
        if result.ok:
            try:
                response = json.loads(result.text)
                if response['status'] == 0 and len(response['hypotheses']) > 0:
                    hypo = response['hypotheses'][0]
                    return {'confidence' : hypo['confidence'], 'text' : hypo['utterance']}
                else:
                    raise RecognitionException("Voice recognition failed")
            except (ValueError, KeyError):
                raise RecognitionException("Speech Recognition Server did return no or a wrong json format")
        else:
            raise CommunicationException("Google does not like you!: " + result.text)

    def convert_to_flac(self, audio_file_name, format):
        if format == 'flac':
            return open(audio_file_name,'rb').read()
        converted = NamedTemporaryFile('rb')
        try:
            audio = AudioSegment.from_file(audio_file_name, format=format)
            audio.export(converted.name, format='flac', parameters=['-ar', self.samplerate])
            flac = converted.read()
            converted.close()
            return flac
        except (EOFError,wave.Error): #unfortunately pydub uses a lot of different exceptions
            raise AudioFormatException("file not in given format or unsupported format")

    def send_request(self, url, data, headers):
        """
        returns a result object with:
            result.ok   = True/False 
            result.text = server response text

        either a requests respnose object or a hardcoded stub. 
        """
        return  requests.post(url, data=data, headers=headers)

def recognize_file(audio_file_name, format='mp3'):
    return GoogleSpeechRecognition().recognize(audio_file_name, format)

def recognize(audio_data, format='mp3'):
    input_file = NamedTemporaryFile('wb')
    input_file.write(audio_data)
    input_file.flush()
    ret = recognize_file(input_file.name, format)
    input_file.close()
    return ret
