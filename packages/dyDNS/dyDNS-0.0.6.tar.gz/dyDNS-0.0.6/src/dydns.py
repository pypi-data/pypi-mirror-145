#!/usr/bin/env python3
# coding:utf-8
import subprocess as sp
from os.path import expanduser
home = expanduser("~")
k=open(home+'/.freedns/key','r')
key=k.read()
#print(str(key))
sp.call('openssl enc -d -aes256 -pbkdf2 -in '+home+'/.freedns/crypted -out result -k '+ str(key),shell=True)
f=open('result','r')
lines=f.read()
#print(lines)
sp.call('rm result',shell=True)
USERNAME = str(lines.split('\n',1)[0].split('"')[1])
PASSWORD = str(lines.split('\n',2)[1].split('"')[1])
DOMAIN = str(lines.split('\n',3)[2].split('"')[1])
UPDATE_DOMAINS = [DOMAIN, ] 
print(DOMAIN+"'s ip",' will be updated')
import requests
import json
def get():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    data = response.json()
    return str(data['ip'])

from hashlib import sha1
import urllib
from urllib.error import *
from urllib.request import urlopen
import datetime 
import os
API_URL = "https://freedns.afraid.org/api/?action=getdyndns&sha={sha1hash}"
def get_sha1(username, password):
    return sha1("{0}|{1}".format(username, password).encode('utf-8')).hexdigest()
def read_url(url):
    try:
        return str(urlopen(url).read())
    except (URLError,HTTPError,ContentTooShortError) as inst:
        return "ERROR: {0}".format(inst).encode('utf-8')
def main():
 shahash = get_sha1(USERNAME, PASSWORD)
 url = API_URL.format(sha1hash=shahash)
 ud=get()
 domains = []
 result = read_url(url)
 domains = []
 name=""
 if result.startswith("ERROR"):
  print("no update")
 else:
  r=result.split(DOMAIN)[1]
  ip=r.split('|')[1]
  ur=r.split('|')[2]
  result = read_url(ur.strip())
  print(result.replace('ERROR','No Updated'))
  #print(DOMAIN,':',result.split("'")[1].split(':')[1])

if __name__ == "__main__":
 main()
