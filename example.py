#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
example.py

an example script for testing the success rate of unmollom.
go ahead and run the script. it solves a captcha on the authors site.
please note that the test captcha runs under molloms free API limit. if example.py has some
unusual bad results check manually whether the test captcha is working currently.

:copyright: (c) 2013 by Flurin Rindisbacher.
:license: BSD 2-Clause, see LICENSE for more details.
"""
from bs4 import BeautifulSoup
import requests
import unmollom

class Example(object):

    def __init__(self):
        self.session = requests.Session()

    def solve_and_submit(self):
        captcha = unmollom.solve_url(self.session, 'http://code.flurischt.ch/dev/unmollom/')
        result = self._submit(captcha)
        # server returns SOLVED or FAILED after every post
        return 'SOLVED' in result

    def _submit(self, captcha):
        res = self.session.post('http://code.flurischt.ch/dev/unmollom/', data={'captcha' : captcha,}, allow_redirects=True)
        return res.text


if __name__ == '__main__':
    num_of_tries = int(0)
    num_of_success = int(0)

    try: 
        while True:
            num_of_tries += 1
            success = Example().solve_and_submit()
            if success:
                num_of_success += 1
            print('Try %i success=%s' % (num_of_tries,success))
    except (KeyboardInterrupt):
        pass

    print('Tried %i times and solved the captcha %i times successfully!' % (num_of_tries,num_of_success))
