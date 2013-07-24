# -*- coding: utf-8 -*-

__author__ = 'Flurin Rindisbacher'

import unittest
import os
import json
import uuid
from .. import speech_recognition
from ..exceptions import RecognitionException, CommunicationException, AudioFormatException

def server_response_stub(success_answer=True,response_text=''):
    """ a stub for injecting our own server responses into 
    the GoogleSpeechRecognition class. testing Googles api does not really make sense"""
    class ServerResponse(object):
        def __init__(self, a, t):
            self.ok = a
            self.text = t
    def send_request(url, data, headers):
        return ServerResponse(success_answer, response_text)

    return send_request

class TestGoogleSpeechRecognition(unittest.TestCase):
    def setUp(self):
        # set up some possible API server response
        # request was unsuccessful
        self.no_server_response = server_response_stub(False)
        # server did response, but could not recognize the data
        self.no_recognition = server_response_stub(True, '{"status":0,"id":"7eea7cfb6a09168431e8d76b10842947-1","hypotheses":[]}\n')
        # server responds with code=200 but not in json
        self.no_valid_json = server_response_stub(True, 'wtf?')
        # server responds with json but without our expected elements
        self.valid_but_wrong_json = server_response_stub(True, '{"blubb":0,"id":"7eea7cfb6a09168431e8d76b10842947-1"}\n')
        # server successfully recognized "just an example"
        self.recognition_success = server_response_stub(True, '{"status":0,"id":"7eea7cfb6a09168431e8d76b10842947-1","hypotheses":[{"utterance":"just an example","confidence":0.9}]}\n')        
        self.input_flac = os.path.dirname(os.path.realpath(__file__)) + '/files/1.flac'
        self.input_mp3 = self.input_flac.replace('.flac', '.mp3')

    def test_recognize_success(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.recognition_success
        result = cls.recognize(self.input_flac, format='flac')
        self.assertEqual(result['text'], 'just an example')

    def test_recognize_failure(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_recognition
        self.assertRaises(RecognitionException, cls.recognize, self.input_flac, 'flac')

    def test_recognize_invalid_json(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_valid_json
        self.assertRaises(RecognitionException, cls.recognize, self.input_flac, 'flac')

    def test_recognize_valid_but_wrong_json(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.valid_but_wrong_json
        self.assertRaises(RecognitionException, cls.recognize, self.input_flac, 'flac')

    def test_recognize_no_server_response(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_server_response
        self.assertRaises(CommunicationException, cls.recognize, self.input_flac, 'flac')   

    def test_recognize_wrong_file(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.send_request = self.no_server_response
        self.assertRaises(IOError, cls.recognize, '/dev/nullwtf', 'flac')

    def test_send_request(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        randomdata = str(uuid.uuid4())
        response =  cls.send_request('https://httpbin.org/post', randomdata, cls.headers)
        self.assertEqual(response.ok, True)
        resp_obj = json.loads(response.text)
        self.assertEqual(resp_obj['data'], randomdata)
        for h in cls.headers:
            self.assertEqual(resp_obj['headers'][h], cls.headers[h])

    def test_conversion_no_conv_needed(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        flac = open(self.input_flac, 'rb').read()
        converted = cls.convert_to_flac(self.input_flac, 'flac')
        self.assertEqual(flac, converted)

    def test_conversion_codecs(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        cls.convert_to_flac(self.input_mp3, 'mp3') # should not raise
        cls.convert_to_flac(self.input_flac, 'flac') # should work toonot raise
        # supported formats, but wrong datatype
        self.assertRaises(AudioFormatException, cls.convert_to_flac, self.input_mp3, 'ogg')
        self.assertRaises(AudioFormatException, cls.convert_to_flac, self.input_mp3, 'wav')
        # unsupported format
        self.assertRaises(AudioFormatException, cls.convert_to_flac, self.input_mp3, 'wtf')

    def test_conversion_mp3(self):
        cls = speech_recognition.GoogleSpeechRecognition()
        converted = cls.convert_to_flac(self.input_mp3, 'mp3')
        #this is cheated. we only check if the mp3 has been converted. 
        #it would be better to really check, whether the result is really flac
        self.assertNotEqual(converted, open(self.input_flac, 'rb').read())

    # rename to test_compare_... to run this too. 
    # it's deactivated because its too slow
    #def test_compare_recognition_functions(self):
    def test_compare_recognition_functions(self):
        """
        test the two recognize_*() functions 

        these are tested by calling the google API twice and comparing the result
        """
        flac = open(self.input_flac,'rb').read()
        result_file = speech_recognition.recognize_file(self.input_mp3, 'mp3')
        result_data = speech_recognition.recognize(flac, 'flac')
        self.assertEqual(result_file['text'], result_data['text'])
        #self.assertEqual(result_file['confidence'], result_data['confidence'])
