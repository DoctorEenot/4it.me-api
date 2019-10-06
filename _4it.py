'''
since this beautiful site https://4it.me/ doesn`t have open api
I decided to write this
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse   import quote
import socket, struct


class api:
    def __init__(self):
        self.BASE_URL = 'https://4it.me/'
        self.API_URL = 'https://4it.me/api/'
        self.session = requests.Session()

    def get_city_list(self,city:str):
        #Returns all found cities
        
        city_encoded = quote(city)
        
        headers = {'Referer':self.BASE_URL+'getlistip?q='+city_encoded,                  
                   'X-Requested-With':'XMLHttpRequest'}

        payload = {'city':city}        
        ans = self.session.get(self.API_URL+'getcitylist',params = payload ,headers=headers)
        cities = ans.json()
        return cities

    def convert(self,ip_encoded:int):
        return socket.inet_ntoa(struct.pack('!L', ip_encoded))

    def get_ip_list(self,city,id_net=None, id_nic=None):
        #id_net and id_nic can be found with get_city_list()
        city_encoded = quote(city)
        headers = {'Referer':self.BASE_URL+'getlistip?q='+city_encoded,                   
                   'X-Requested-With':'XMLHttpRequest'}

        to_return = []
        if id_net != None:
            payload = {'cityid':id_net,
                       'base':'net',
                       'city':city_encoded}
            ans = self.session.get(self.API_URL+'getlistip', params = payload, headers = headers)
            ans_json = ans.json()
            for el in ans_json:
                to_return.append(self.convert(el['b'])+'-'+self.convert(el['e']))
        if id_nic != None:
            payload = {'cityid':id_nic,
                       'base':'nic',
                       'city':city_encoded}
            ans = self.session.get(self.API_URL+'getlistip', params = payload, headers = headers)
            ans_json = ans.json()
            for el in ans_json:
                to_return.append(self.convert(el['b'])+'-'+self.convert(el['e']))
        return to_return


    def get_whois(self,target:str):#Function of site api

        headers = {'Referer':self.BASE_URL+'whois',                   
                   'X-Requested-With':'XMLHttpRequest'}

        response = self.session.get(self.API_URL+'getwhois?query='+target,headers = headers)
        rp_json = response.json()
        return rp_json

    def get_yandex(self,target:str):#Function of site api
        headers = {'Referer':self.BASE_URL+'whois',                   
                   'X-Requested-With':'XMLHttpRequest'}

        response = self.session.get(self.API_URL+'getyandex?domain='+target,headers = headers)
        rp_json = response.json()
        return rp_json

    def get_Alexa(self,target:str):#Function of site api
        headers = {'Referer':self.BASE_URL+'whois',                   
                   'X-Requested-With':'XMLHttpRequest'}

        response = self.session.get(self.API_URL+'getAlexa?domain='+target,headers = headers)
        if response.text == '"No Data"':
            return {'Alexa':None}
        rp_json = response.json()
        return rp_json

    def get_google_dns(self,target:str):#Not function of site api, but...
        headers = {'Referer':self.BASE_URL+'whois'}
        payload = {'name':target,
                   'type':'ANY'}

        response = self.session.get('https://dns.google.com/resolve',params = payload,headers = headers)
        
        rp_json = response.json()
        return rp_json

    def get_available_status(self,target:str):#Function of site api
        headers = {'Referer':self.BASE_URL+'whois',                   
                   'X-Requested-With':'XMLHttpRequest'}

        response = self.session.get(self.API_URL+'getavaiblestatus?query='+target,headers = headers)
        rp_json = response.json()
        return rp_json

    def whois(self,target:str):
        #Returns raw information about ip adress or domain
        to_return=[]
        to_return.append(self.get_whois(target))
        to_return.append(self.get_yandex(target))
        to_return.append(self.get_Alexa(target))
        to_return.append(self.get_google_dns(target))
        to_return.append(self.get_available_status(target))
        return to_return

    def port_scan(self,target:str,ports:list):
        headers = {'Referer':self.BASE_URL+'portscan',                   
                   'X-Requested-With':'XMLHttpRequest'}
        port_str = str(ports[0])
        for i in range(1,len(ports)):
            port_str += ','
            port_str += str(ports[i])

        payload = {'host':target,
                   'ports':port_str}

        response = self.session.get(self.API_URL+'checkports',params = payload,headers = headers)
        rp_json = response.json()
        return rp_json

if __name__ == '__main__':
    it = api()
    #info = it.get_city_list('Курск')
    #ips = it.get_ip_list('Курск',id_net = info[0]['id_net'], id_nic = info[0]['id_nic'])
    #print(ips)
    inf = it.port_scan('rootgame.org',[80,8080])
    print(inf)
    input()