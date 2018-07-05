import hashlib
import hmac as hmac_lib
import requests
import time
from urllib.parse import urlparse


def hmac(hmac_key, hmac_secret, server='https://localbitcoins.net'):
    conn = Connection()
    conn._set_hmac(server, hmac_key, hmac_secret)
    return conn

class Connection():
    def __init__(self):
        self.server = None

        self.hmac_key = None
        self.hmac_secret = None

    def call(self, method, url, params=None, stream=False, files=None):
        method = method.upper()
        if method not in ['GET', 'POST']:
            raise Exception(u'Invalid method {}!'.format(method))

        if method == 'GET' and files:
            raise Exception(u'You cannot send files with GET method!')

        if url.startswith(self.server):
            url = url[len(self.server):]

        if self.hmac_key:
            for retry in range(10):
                nonce = str(int(time.time() * 1000))

                if method == 'POST':
                    api_request = requests.Request('POST', self.server + url, data=params, files=files).prepare()
                    params_encoded = api_request.body

                else:
                    api_request = requests.Request('GET', self.server + url, params=params).prepare()
                    params_encoded = urlparse(api_request.url).query

                message = nonce + self.hmac_key + str(url)

                if params_encoded:
                    message += str(params_encoded)

                message = bytes(message, 'UTF-8')
                signature = hmac_lib.new(self.hmac_secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

                api_request.headers['Apiauth-Key'] = self.hmac_key
                api_request.headers['Apiauth-Nonce'] = nonce
                api_request.headers['Apiauth-Signature'] = signature

                session = requests.Session()
                response = session.send(api_request, stream=stream)

                try:
                    response_json = response.json()
                    if int(response_json.get('error', {}).get('error_code')) == 42:
                        time.sleep(0.1)
                        continue
                except:
                    pass

                return response
            raise Exception(u'Nonce is too small!')
        raise Exception(u'No HMAC connection initialized!')

    def _set_hmac(self, server, hmac_key, hmac_secret):
        self.server = server
        self.hmac_key = str(hmac_key)
        self.hmac_secret = bytes(hmac_secret, 'UTF-8')
