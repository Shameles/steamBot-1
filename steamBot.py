import urllib.request
import http.cookiejar
import json
import time
import base64
import pickle
import os.path
import webbrowser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

class steamBot():
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)
        self.inventory = {}
        
        if os.path.isfile('cookies.pkl'):
            with open('cookies.pkl', 'rb') as input:
                for c in range (6):
                    self.cj.set_cookie(pickle.load(input))
                for cookie in self.cj:
                    if cookie.name == 'sessionid':
                        self.sessionid = cookie.value
            with open('credentials.json', 'r') as credfile:
                credentials = json.load(credfile)
                self.steamid = credentials['steamid']
                
        else:
            with open('credentials.json', 'r') as credfile:
                credentials = json.load(credfile)
                self.username = credentials['username']
                self.password = credentials['password']
            self.getSession()
            self.getRSA()
            self.doLogin('')
            self.doLogin('emailauth')
            
            with open('cookies.pkl', 'wb') as output:
                for cookie in self.cj:
                    pickle.dump(cookie, output, -1)
       
    def getSession(self):
        url = 'http://steamcommunity.com/'
        values = {}
        post = urllib.parse.urlencode(values)
        headers = {}
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        resp = urllib.request.urlopen(request)

    def getRSA(self):
        url = 'https://steamcommunity.com/login/getrsakey/'
        values = {'username' : self.username, 'donotcache' : str(int(time.time()*1000))}
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
            self.steamid = data['transfer_parameters']['steamid']
            with open('credentials.json', 'r') as file:
                credentials = json.load(file)
                credentials['steamid'] = self.steamid
            with open('credentials.json', 'w') as outfile:
                outfile.write(json.dumps(credentials, indent=4, sort_keys=True))

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
            
    def placeOrder(self, valuta, appid, markethash, price, quantity):
        url = 'https://steamcommunity.com/market/createbuyorder/'
        values = {'sessionid' : self.sessionid,
                  'currency' : str(valuta),
                  'appid' : str(appid),
                  'market_hash_name' : str(markethash),
                  'price_total' : str(price),
                  'quantity' : str(quantity)}
        headers = {'Accept' : '*/*',
                   'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer' : 'http://steamcommunity.com/market/',
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
        
        data = json.loads(response.decode('utf-8'))
        return data

    def cancelOrder(self, buyorderid):
        url = 'http://steamcommunity.com/market/cancelbuyorder/'
        values = {'sessionid' : self.sessionid,
                  'buy_orderid' : buyorderid}
        headers = {'Accept' : '*/*',
                   'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Referer' : 'http://steamcommunity.com/market/',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))
        return data

    def getInventory(self, contextid):
        url = 'http://steamcommunity.com/profiles/' + self.steamid + '/'
        values = {}
        headers = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        self.profile = urllib.request.urlopen(request).geturl()
        
        url = self.profile + '/inventory/json/' + str(contextid) + '/2/'
        values = {}
        headers = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()
        data = json.loads(response.decode('utf-8'))

        self.inventory[contextid] = {}
        for item in data['rgInventory']:
            self.inventory[contextid][item] = {}
            for property in data['rgInventory'][item]:
                self.inventory[contextid][item][property] = data['rgInventory'][item][property]
            for property in data['rgDescriptions'][self.inventory[contextid][item]['classid'] + '_' + self.inventory[contextid][item]['instanceid']]:
                self.inventory[contextid][item][property] = data['rgDescriptions'][self.inventory[contextid][item]['classid'] + '_' + self.inventory[contextid][item]['instanceid']][property]
            for key in ['name_color', 'pos', 'type', 'icon_drag_url', 'icon_url', 'icon_url_large', 'market_actions', 'owner_descriptions', 'tags', 'descriptions', 'background_color', 'actions']:
                self.inventory[contextid][item].pop(key, None)
                
        with open('inventory.json', 'w') as outfile:
            outfile.write(json.dumps(self.inventory, indent=4, sort_keys=True))

        return self.inventory

    def getSupplyDemand(self, currency, item_nameid):
        url = 'http://steamcommunity.com/market/itemordershistogram?country=EN&language=English&currency={0}&item_nameid={1}'.format(currency, item_nameid)
        values = {}
        headers = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))
        if data['success'] == 1:
            supply = {}
            demand = {}
            for sellprice in data['sell_order_graph']:
                supply[sellprice[0]] = sellprice[1]
            for buyprice in data['buy_order_graph']:
                demand[buyprice[0]] = buyprice[1]

            return {'minsupply' : data['lowest_sell_order'],  'maxdemand' : data['highest_buy_order'], 'supply' : supply, 'demand': demand}   

    def sellItem(self, appid, itemid, price, quantity):
        url = 'https://steamcommunity.com/market/sellitem/'
        values = {'sessionid' : self.sessionid,
                  'appid' : str(appid),
                  'contextid' : '2',
                  'assetid' : str(itemid),
                  'price' : str(price),
                  'amount' : str(quantity)}
        headers = {'Accept' : '*/*',
                   'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer' : 'http://steamcommunity.com/market/',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))
        return data

    def getMyListings(self):
        url = 'http://steamcommunity.com/market/mylistings'
        values = {}
        headers = {}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()
        
        data = json.loads(response.decode('utf-8'))

        listings = {}
        templistings = data['hovers'].split(';')
        for listing in templistings:
            index = templistings.index(listing)
            listing = listing[listing.find('('):listing.find(')') + 1]
            listing = listing.replace('( g_rgAssets, ', '(')
            if not 'image' in listing and listing is not '':
                temp = listing.split(',')
                temptwo = []
                for i in temp:
                    index = temp.index(i)
                    i = i.replace(' ', '').replace('(', '').replace(')', '').replace("'", '')
                    temptwo.append(i)
                listings[temptwo[0].replace('mylisting_', '').replace('_name', '')] = [temptwo[1], temptwo[2], temptwo[3], temptwo[4]]
                    
        return listings

    def removeListing(self, listingid):
        url = 'http://steamcommunity.com/market/removelisting/' + str(listingid)
        print(url)
        values = {'sessionid' : self.sessionid}
        headers = {'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Requested-With' : 'XMLHttpRequest',
                   'X-Prototype-Version' : '1.7',
                   'Accept' : 'text/javascript, text/html, application/xml, text/xml, */*',
                   'Referer' : 'http://steamcommunity.com/market/',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Host' : 'steamcommunity.com',
                   'Connection' : 'Keep-Alive',
                   'Cache-Control' : 'no-cache'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

# Nothing is here, what was here before will be moved to the wiki asap.
