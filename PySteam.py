import urllib.request
import http.cookiejar
import json
import time
import base64
import webbrowser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class steamBot():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        print('[X] Requesting Session ID')

        url = 'http://steamcommunity.com/'
        values = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        headers = {'Accept' : 'text/html, application/xhtml+xml, */*',
                   'Accept-Language' : 'nl-NL',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Accept-Encoding' : 'gzip, deflate',
                   'Host' : 'steamcommunity.com',
                   'DNT' : '1',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache'}
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request)

        # Process the data
        headers = str(response.info())

        SESSION_ID=headers[headers.find('sessionid') + 10:headers.find('sessionid') + 34]

        print('[X] Session ID: ' + SESSION_ID)
        STEAM_COUNTRY=headers[headers.find('steamCountry') + 13:headers.find('steamCountry') + 50]

        print('[X] Country: ' + STEAM_COUNTRY[0:2])

        # Request an RSA key

        url = 'https://steamcommunity.com/login/getrsakey/'
        values = {'username' : username, 'donotcache' : str(int(time.time()*1000))}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
                   'Referer' : 'https://steamcommunity.com/login/home/?goto=0',
                   'Accept-Language' : 'nl-NL',
                   'Accept-Encoding' : 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'DNT' : '1',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache',
                   'Cookie' : 'sessionid=' + SESSION_ID + '; ' + 'steamCountry=' + STEAM_COUNTRY + '; ' + 'timezoneOffset=7200,0;'}
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        # Process the data
        data = json.loads(response.decode('utf-8'))

        mod = int(str(data['publickey_mod']), 16)
        exp = int(str(data['publickey_exp']), 16)

        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.new(rsa_key)
        encrypted_password = rsa.encrypt(password.encode('utf-8'))
        encrypted_password = base64.b64encode(encrypted_password)

        # Do the login

        url = 'https://steamcommunity.com/login/dologin'
        values = {'password' : encrypted_password.decode('utf-8'),
                  'username' : username,
                  'twofactorcode' : '',
                  'emailauth' : '',
                  'loginfriendlyname' : '',
                  'captchagid' : '-1',
                  'captcha_text' : '',
                  'emailsteamid' : '',
                  'rsatimestamp' : str(data['timestamp']),
                  'remember_login' : 'false',
                  'donotcache' : str(int(time.time()*1000))}
        headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
                   'Referer' : 'https://steamcommunity.com/login/home/?goto=0',
                   'Accept-Language' : 'nl-NL',
                   'Accept-Encoding' : 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'DNT' : '1',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache',
                   'Cookie' : 'sessionid=' + SESSION_ID + '; ' + 'steamCountry=' + STEAM_COUNTRY + '; ' + 'timezoneOffset=7200,0;'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        # Process the data
        data = json.loads(response.decode('utf-8'))
        print(data)

        EMAIL_STEAM_ID = str(data['emailsteamid'])

        # Here we have to solve the e-mail auth

        # Request an RSA key again

        url = 'https://steamcommunity.com/login/getrsakey/'
        values = {'username' : username, 'donotcache' : str(int(time.time()*1000))}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
                   'Referer' : 'https://steamcommunity.com/login/home/?goto=0',
                   'Accept-Language' : 'nl-NL',
                   'Accept-Encoding' : 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'DNT' : '1',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache',
                   'Cookie' : 'sessionid=' + SESSION_ID + '; ' + 'steamCountry=' + STEAM_COUNTRY + '; ' + 'timezoneOffset=7200,0;'}
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        # Process the data
        data = json.loads(response.decode('utf-8'))

        mod = int(str(data['publickey_mod']), 16)
        exp = int(str(data['publickey_exp']), 16)

        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.new(rsa_key)
        encrypted_password = rsa.encrypt(password.encode('utf-8'))
        encrypted_password = base64.b64encode(encrypted_password)
                  
        # Do the login again

        url = 'https://steamcommunity.com/login/dologin'
        values = {'password' : encrypted_password.decode('utf-8'),
                  'username' : username,
                  'twofactorcode' : '',
                  'emailauth' : str(input('Please input the key you received by e-mail: ')),
                  'loginfriendlyname' : '',
                  'captchagid' : '-1',
                  'captcha_text' : '',
                  'emailsteamid' : EMAIL_STEAM_ID,
                  'rsatimestamp' : str(data['timestamp']),
                  'remember_login' : 'false',
                  'donotcache' : str(int(time.time()*1000))}
        headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
                   'Referer' : 'https://steamcommunity.com/login/home/?goto=0',
                   'Accept-Language' : 'nl-NL',
                   'Accept-Encoding' : 'gzip, deflate',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'DNT' : '1',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache',
                   'Cookie' : 'sessionid=' + SESSION_ID + '; ' + 'steamCountry=' + STEAM_COUNTRY + '; ' + 'timezoneOffset=7200,0;'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        #Process the data

        data = json.loads(response.decode('utf-8'))
        print(data)

steamBot('yourusername', 'yourpassword')
