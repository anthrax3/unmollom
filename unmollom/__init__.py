# -*- coding: utf-8 -*-

"""
a mollom captcha solver

unmollom is a python module that solves mollom captchas using Google's speech recognition.
use it in your "requests" based python code.

USAGE:
    >>> import requests
    >>> import unmollom
    >>> session = requests.Session()
    >>> captcha = unmollom.solve_url(session, 'http://YOUR_MOLLOM_FORM_HERE')
    >>> # now post your form data using the SAME session and the captcha

    You can also download the html yourself and pass it to unmollom.solve()

    >>> import requests
    >>> import unmollom
    >>> session = requests.Session()
    >>> html = session.get('http://SOME_URL')
    >>> captcha = unmollom.solve(session, html)
    >>> # ... 

:copyright: (c) 2013 by Flurin Rindisbacher.
:license: BSD 2-Clause, see LICENSE for more details.
"""

__title__ = 'unmollom'
__version__ = '1.0'
__author__ = 'Flurin Rindisbacher'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 Flurin Rindisbacher'

import unmollom.speech_recognition
import unmollom.exceptions
from .api import solve_url, solve
