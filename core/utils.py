from telethon import TelegramClient
from telethon.sessions import StringSession
import random
import string
from telethon.tl.types import PeerUser
from telethon.tl.functions.contacts import ResolvePhoneRequest
from dotenv import load_dotenv
import os
import requests

load_dotenv()
token = os.getenv('AFRO_SMS_KEY')

session = requests.Session()
base_url = 'https://api.afromessage.com/api/challenge'


SESSION = StringSession('1BJWap1wBuwEalTHTTSn9P19Ugo3MGKKIsfEAcZ6JMWcY2CID3ebquHb5oRmBmkIt0w2o3eeNpaudwVKFrpS6v8p1jBo534d-qV8FNfmkPWRvjpYJ4ot4UXJx8bYms3bKlzoNDaw-QvADUHNChwUAey7TfZSy48dDC_ak91oug3-3p3cTvgt8J-_VHZzRg0fg33TlAlrMu-UXwvAwhD_smaEPCyyK3WPmLqfriawj8zLPzDFxkZtauq5q0NPu0tvV_C1x0pxY2Oqf1NRq4M9kom9EMr4GbnCmu3DuHk19NU-2VTW4FucCUN_EFqbcbkpcNKVHVdoe4zTnrNTl67IlIwVmd9m1CO4=')
API_ID = 28147328
API_HASH = '8746ffebd74e79663dcbbcd891bad8a6'

client = TelegramClient(SESSION, api_id=API_ID, api_hash=API_HASH)

def random_text_generator(length=16):
    characters = list(string.digits + string.ascii_letters + string.punctuation)
    random.shuffle(characters)
    return ''.join(random.choices(characters, k=length))


class OtpDoesNotSent(Exception):
     def __init__(self, *args):
          super().__init__(*args)

def send_otp(phonenumber):
        headers = {'Authorization': 'Bearer ' + token}
        to = phonenumber
        pre = "Your Zion Verification Code is"
        post = "Thanks Being Part Of Us"
        sb = 1
        sa = 1
        ttl = 0
        len = 4
        t = 0
        url = '%s?from=&sender=&to=%s&pr=%s&ps=%s&callback=&sb=%d&sa=%d&ttl=%d&len=%d&t=%d' % (
            base_url,  to, pre, post,  sb, sa, ttl, len, t)
        result = session.get(url, headers=headers)
        if result.status_code == 200:
            json = result.json()
            if json['acknowledge'] == 'success':
                print(json)
                return json['response']['code']
            else:
                return OtpDoesNotSent
        else:
            print('http error ... code: %d , msg: %s ' %
                (result.status_code, result.content))
            return OtpDoesNotSent
