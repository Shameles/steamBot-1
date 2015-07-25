import urllib.request
import http.cookiejar
import json
import time
import base64
import pickle
import os.path
import random
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
            
            with open('cookies.pkl', 'wb') as output:
                for cookie in self.cj:
                    pickle.dump(cookie, output, -1)
       
    def getSession(self):
        url = 'http://steamcommunity.com/'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

    def getRSA(self):
        url = 'https://steamcommunity.com/login/getrsakey/'
        values = {'username' : self.username, 'donotcache' : str(int(time.time()*1000))}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))

        self.rsatimestamp = data['timestamp']
        steamid = data['steamid']
        mod = int(str(data['publickey_mod']), 16)
        exp = int(str(data['publickey_exp']), 16)

        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.new(rsa_key)
        self.encrypted_password = rsa.encrypt(self.password.encode('utf-8'))
        self.encrypted_password = base64.b64encode(self.encrypted_password)

    def doLogin(self, type):
        url = 'https://steamcommunity.com/login/dologin'
        if 'email' in type:
            self.emailkey = input('INPUT KEY FROM E-MAIL: ')
        if 'captcha' in type:
            webbrowser.open('http://steamcommunity.com/public/captcha.php?gid=' + self.captchagid)
            self.captchakey = input('PLEASE INPUT THE CAPTCHA: ')
        values = {'password' : self.encrypted_password.decode('utf-8'),
                  'username' : self.username,
                  'twofactorcode' : '',
                  'emailauth' : self.emailkey if 'email' in type else '',
                  'loginfriendlyname' : '',
                  'captchagid' : self.captchagid if 'captcha' in type else '-1',
                  'captcha_text' : self.captchakey if 'captcha' in type else '',
                  'emailsteamid' : self.emailsteamid if 'email' in type else '',
                  'rsatimestamp' : self.rsatimestamp,
                  'remember_login' : 'true',
                  'donotcache' : str(int(time.time()*1000))}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data)
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
            if 'emailsteamid' in data:
                self.emailsteamid = data['emailsteamid']
                self.doLogin('emailauth')
            if data['message'].startswith('Please verify'):
                self.captchagid = data['captcha_gid']
                self.doLogin('captcha')
            if data['message'] == 'Incorrect login':
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
        headers = {'Referer' : 'http://steamcommunity.com/market/'}
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
        headers = {'Referer' : 'http://steamcommunity.com/market/'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

        data = json.loads(response.decode('utf-8'))
        return data

    def getInventory(self, contextid):
        url = 'http://steamcommunity.com/profiles/' + self.steamid + '/'
        request = urllib.request.Request(url)
        self.profile = urllib.request.urlopen(request).geturl()
        
        url = self.profile + '/inventory/json/' + str(contextid) + '/2/'
        request = urllib.request.Request(url)
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
        request = urllib.request.Request(url)
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

    def getListings(self):
        url = 'http://steamcommunity.com/market/mylistings'
        request = urllib.request.Request(url)
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
        values = {'sessionid' : self.sessionid}
        headers = {'Referer' : 'http://steamcommunity.com/market/'}
        post = urllib.parse.urlencode(values)
        binary_data = post.encode('utf-8')
        request = urllib.request.Request(url, binary_data, headers)
        response = urllib.request.urlopen(request).read()

    def sendMessage(self, message, person):
        # This function will be improved asap.
        if self.chat == False:
            url = 'http://steamcommunity.com/chat'
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request).read().decode('utf-8')
            self.apikey = response[response.find("'https://api.steampowered.com/'") + 34:response.find("'https://api.steampowered.com/'") + 66]
            self.friends = json.loads(response[response.find('[{"m_unAccountID"'):response.find('$J( InitializeChat );') - 12] + ']')
            self.chat = True

            self.jquery = ''.join(random.choice('0123456789') for i in range(22))
            self.timestamp = str(int(time.time()*1000))
                                  
            url = 'https://api.steampowered.com/ISteamWebUserPresenceOAuth/Logon/v0001/?jsonp=jQuery' + self.jquery + '_' + self.timestamp + '&ui_mode=web&access_token=' + self.apikey + '&_=' + self.timestamp
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request).read().decode('utf-8')
            logondata = json.loads(response[ response.index("(") + 1 : response.rindex(")") ])
            self.umqid = logondata['umqid'] 
            
        for friend in self.friends:
            if friend['m_strName'] == person:
                self.dst = friend['m_ulSteamID']
                
        self.timestamp = str(int(time.time()*1000))
        url = 'https://api.steampowered.com/ISteamWebUserPresenceOAuth/Message/v0001/?jsonp=jQuery' + self.jquery + '_' + self.timestamp + '&umqid=' + self.umqid + '&type=saytext&steamid_dst=' + self.dst + '&text=' + urllib.parse.quote_plus(message) +'&access_token=' + self.apikey + '&_=' + self.timestamp
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

# Nothing is here, what was here before will be moved to the wiki asap.
