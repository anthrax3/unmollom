# -*- coding: utf-8 -*-

__author__ = 'Flurin Rindisbacher'

import unittest
import os
from unmollom import util
from unmollom.exceptions import NoMollomTagsFoundException

class TestBuildCaptcha(unittest.TestCase):
    def test_empty(self):
        captcha = util.build_captcha('')
        self.assertEqual('', captcha)

    def test_valid(self):
        captcha = util.build_captcha('this is a test')
        self.assertEqual('tiat', captcha)

    def test_lowercase(self):
        captcha = util.build_captcha('Lorem ipsum Dolor Sit amet')
        self.assertEqual('lidsa', captcha)

    def test_int(self):
        captcha = util.build_captcha(int(1))
        self.assertEqual('1', captcha)

    def test_none(self):
        captcha = util.build_captcha(None)
        self.assertEqual('', captcha)

    def test_recognition_improvement(self):
        # "x ray" should be one word, if google recognizes "hilo", mollom means "kilo"
        captcha = util.build_captcha('x ray i5 lorem Quebec Hilo')
        self.assertEqual('xalqk', captcha)

class TestMollomExtract(unittest.TestCase):
    def setUp(self):
        self.pwd = os.path.dirname(os.path.realpath(__file__))

    def test_empty_source(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '')

    def test_invalid_html(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '<html></head>')

    def test_html_without_mollom(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '<html><head></head><body><div><u>test</u></div></body></html>') 

    def test_big_page_without_mollom(self):
        data = open(self.pwd + '/files/no_mollom.html', 'r').read()
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, data)

    def test_big_page_with_mollom(self):
        data = open(self.pwd + '/files/mollom.html', 'r').read()
        mollom_url = util.extract_mollom_audio_file(data)
        self.assertEqual('http://174.37.205.126:80/v1/captcha/130731d44153a3e241.mp3', mollom_url)