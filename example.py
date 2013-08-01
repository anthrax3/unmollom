#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

a demo script that shows the usage of unmollom
have a look at LurinFactsContributor.contribute() 
the rest of the code is specific to the demo site used in this example

:copyright: (c) 2013 by Flurin Rindisbacher.
:license: BSD 2-Clause, see LICENSE for more details.
"""
from bs4 import BeautifulSoup
import requests
import unmollom
from unmollom.exceptions import CommunicationException

class LurinSpamException(RuntimeError):
    """The target site thinks you're a spammer!"""

class LurinFactsContributor(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Referer' : 'http://lurinfacts.ch/contribute/'
            }
        )
        self.secId = None

    def make_request(self, slogan='', captcha=''):
        if not self.secId:
            self.extractSecId()

        data = {
            'Slogan' : slogan,
            'SecurityID' : self.secId,
            'signsLeft' : '140',
            'Captcha' : captcha,
            'action_sendContactForm' : 'Submit',
        }
        res = self.session.post('http://lurinfacts.ch/contribute/SubmitSloganForm', data=data, allow_redirects=True)
        self.extractSecId(res.text)
        return res.text

    def extractSecId(self, source=None):
        if not source:
            source = self.session.get('http://lurinfacts.ch/contribute/').text
        if 'Your submission has been rejected because it was treated as spam.' in source:
            raise LurinSpamException('spam')
        soup = BeautifulSoup(source)
        self.secId =  soup('input', attrs={'id': 'Form_SubmitSloganForm_SecurityID'})[0]['value']


    def contribute(self, slogan='Lurin owns this site'):
        # make an empty request to force the site to show the mollom form
        html = self.make_request()
        # solve the captcha (using the same http session!)
        try:
            captcha = unmollom.solve(self.session, html)
            # post a "contribution"
            success = 'Really this is your contribution?' in self.make_request(slogan, captcha)
        except CommunicationException as e:
            print(e)
            success = False
        return success


if __name__ == '__main__':
    num_of_tries = int(0)
    num_of_success = int(0)

    try: 
        while True:
            num_of_tries += 1
            success = LurinFactsContributor().contribute()
            if success:
                num_of_success += 1
            print('Try %i success=%s' % (num_of_tries,success))
    except (KeyboardInterrupt,LurinSpamException):
        pass

    print('Tried %i times and solved the captcha %i times successfully!' % (num_of_tries,num_of_success))
