#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

# some words google gets constantly wrong
RECOGNITION_FAILS = {
    'x ray' : 'x-ray',
    'i5' : 'alpha',
    'lulu' : 'zulu',
    'key bank' : 'quebec',
    'dick' : 'quebec',
    'hilo' : 'kilo'
}

class UnMollom:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Referer' : 'http://lurinfacts.ch/contribute/'
            }
        )
        self.secId = None

    def req(self, slogan='', captcha=''):
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
            raise Exception('spam')
        soup = BeautifulSoup(source)
        self.secId =  soup('input', attrs={'id': 'Form_SubmitSloganForm_SecurityID'})[0]['value']
        

    def extractMollomFile(self, source):
        soup = BeautifulSoup(source)
        mollom_span = soup.find('span', attrs={'class' : 'mollom-audio-captcha'})
        if mollom_span:
            return mollom_span.find('object')['data']
        else:
            #print source
            raise Exception("No Mollom found")

    def getCaptcha(self, mp3_url):
        mp3file = self.session.get(mp3_url).content
        (flac,samplerate) = self.toFlac(mp3file)
        recognition_result = self.recognize(flac,samplerate)
        if recognition_result['confidence'] > 0.5:
            text = recognition_result['text'].lower()
            
            # some words are constantly recognized wrong
            # let's correct theem
            for k in RECOGNITION_FAILS:
                text = text.replace(k, RECOGNITION_FAILS[k])

            # mollom wants the first character of each word
            captcha =  ''.join( [ x[0] for x in text.split(' ') ] ).lower()

            # debug
            f = file('testdata/%s_%s.flac' % (text.replace(' ','-'),captcha),'wb')
            f.write(flac)
            f.close()

            return captcha
        else:
            raise Exception('Google is not sure enough')

    def recognize(self, flac, samplerate):
        url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
        headers={'Content-Type': 'audio/x-flac; rate=%i' % samplerate, 'User-Agent':'Mozilla/5.0'}
        req =  requests.post(url, data=flac, headers=headers)
        if req.ok:
            response = json.loads(req.text)
            if response['status'] == 0 and len(response['hypotheses']) > 0:
                hypo = response['hypotheses'][0]
                return {'confidence' : hypo['confidence'], 'text' : hypo['utterance']}
            else:
                raise Exception("Voice recognition failed")
        else:
            raise Exception("Google does not like you!")

    def toFlac(self, mp3data):
        SAMPLERATE = '48000'
        converted = NamedTemporaryFile('rb')
        toConvert = NamedTemporaryFile('wb')
        toConvert.write(mp3data)
        toConvert.flush()
        mp3 = AudioSegment.from_mp3(toConvert.name)
        mp3.export(converted.name, format='flac', parameters=['-ar', SAMPLERATE])
        flac = converted.read()
        toConvert.close()
        converted.close()
        return (flac,int(SAMPLERATE))

    def go(self, slogan='Lurin owns this site'):
        mollomurl = self.extractMollomFile(self.req(slogan))
        captcha = self.getCaptcha(mollomurl)
        success =  'Really this is your contribution?' in  self.req(slogan=slogan, captcha=captcha)
        if success:
            print('%s was correct' % captcha)
        else:
            print('%s was wrong' % captcha)
        return success

if __name__ == '__main__':
    num_of_tries = int(0)
    num_of_success = int(0)
    try:
        while True:
            try:
                num_of_tries += 1
                if num_of_tries % 10 == 0:
                    print('Trying the %ith time' % num_of_tries)
                if UnMollom().go():
                    num_of_success +=1
            except Exception as e:
                print(e)
                pass # ignore and continue
    except KeyboardInterrupt:
        pass
    print('Tried %i times and was %i times successful!' % (num_of_tries,num_of_success))