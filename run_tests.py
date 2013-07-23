#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

if __name__ == '__main__':
    dir = os.path.dirname(os.path.realpath(__file__))
    suite = unittest.TestLoader().discover(dir, pattern = "test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite) 
