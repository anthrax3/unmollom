#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

#make sure, python can find your ffmpeg installation (for pydub)
PATH_TO_FFMPEG = '/usr/local/bin/'

if __name__ == '__main__':
    os.environ['PATH'] = os.environ['PATH'] + ':' + PATH_TO_FFMPEG
    dir = os.path.dirname(os.path.realpath(__file__))
    suite = unittest.TestLoader().discover(dir, pattern = "test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite) 
