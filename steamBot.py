import urllib.request
import http.cookiejar
import json
import time
import base64
import webbrowser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# Construct and install the HTTP(cookiejar)-Opener
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

class steamBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
        url = 'http://steamcommunity.com/'
        values = {}
        post = urllib.parse.urlencode(values)
        headers = {}
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        resp = urllib.request.urlopen(request)

        for cookie in cj:
            print(cookie.name, cookie.value)
            if cookie.name == 'sessionid':
                self.sessionid = cookie.value
            if cookie.name == 'steamCountry':
                self.steamcountry = cookie.value

    def getRSA(self):

        url = 'https://steamcommunity.com/login/getrsakey/'
        values = {'username' : 'icraftedyou', 'donotcache' : str(int(time.time()*1000))}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        headers = {}
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))

        self.rsatimestamp = data['timestamp']
        mod = int(str(data['publickey_mod']), 16)

        exp = int(str(data['publickey_exp']), 16)

        steamid = data['steamid']

        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.new(rsa_key)
        self.encrypted_password = rsa.encrypt('Kat12345'.encode('utf-8'))
        self.encrypted_password = base64.b64encode(self.encrypted_password)

    def doLogin(self, type):
        url = 'https://steamcommunity.com/login/dologin'
        values = {'password' : self.encrypted_password.decode('utf-8'),
                  'username' : self.username,
                  'twofactorcode' : '',
                  'emailauth' : '' if type != 'emailauth' else str(input('Please input the key you received by e-mail: ')),
                  'loginfriendlyname' : '',
                  'captchagid' : '-1' if type != 'captcha' else self.captchagid,
                  'captcha_text' : '' if type != 'captcha' else str(input('Please input the captcha')),
                  'emailsteamid' : '',
                  'rsatimestamp' : self.rsatimestamp,
                  'remember_login' : 'true',
                  'donotcache' : str(int(time.time()*1000))}
        headers = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))
        
        if data['success'] == True:
            self.securetoken = data['transfer_parameters']['token_secure']
            print(self.securetoken)
            self.token = data['transfer_parameters']['token']
            print(self.token)
            self.webcookie = data['transfer_parameters']['webcookie']
            print(self.webcookie)
            self.auth = data['transfer_parameters']['auth']
            print(self.auth)

            for cookie in cj:
                print(cookie.name, cookie.value)
            return True
        else:
            if data['emailauth_needed'] == True:
                print('- Result: Email-authentication needed')
                print('- E-mail: ...' + data['emaildomain'])
                self.emailsteamid = str(data['emailsteamid'])
                self.emaildomain = data['emaildomain']

            else:
                print('[X] Login details incorrect')
                return False
            
    def placeOrder(self, valuta, itemid, markethash, price, quantity):
        url = 'https://steamcommunity.com/market/createbuyorder/'
        values = {'sessionid' : self.sessionid,
                  'currency' : str(valuta),
                  'appid' : str(itemid),
                  'market_hash_name' : str(markethash),
                  'price_total' : str(price),
                  'quantity' : str(quantity)}
        headers = {'Accept' : '*/*',
                   'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer' : 'http://steamcommunity.com/market/listings/730/Chroma%202%20Case',
                   'Accept-Language' : 'nl-NL',
                   'Origin' : 'http://steamcommunity.com',
                   'Accept-Encoding' : 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()
        
        #data = json.loads(response.decode('utf-8'))
        return response.decode('utf-8')

# Command the bot here, this is just an example!
mybot = steamBot('username', 'password')
mybot.getRSA()
mybot.doLogin('')
mybot.doLogin('emailauth')
mybot.placeOrder(3, 730, 'Chroma 2 Case', 4, 1)
