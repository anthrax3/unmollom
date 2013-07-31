# -*- coding: utf-8 -*-

__author__ = 'Flurin Rindisbacher'

import unittest
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

class TestMollomExtract(unittest.TestCase):
    def test_empty_source(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '')

    def test_invalid_html(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '<html></head>')

    def test_html_without_mollom(self):
        self.assertRaises(NoMollomTagsFoundException, util.extract_mollom_audio_file, '<html><head></head><body><div><u>test</u></div></body></html>') 