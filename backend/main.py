import random
import string
import os
import sys
import logging

from flask import Flask, request
from flask_cors import CORS
from sqlitedict import SqliteDict
from switchcase import case, enable

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('con.log'))

print = logger.info

app = Flask('app')
CORS(app)
linkdb = SqliteDict('./linksdb.sqlite')

args = []

def generate_url_code():
  return ''.join(random.choices(string.ascii_lowercase, k = 4))

def get_link(code):
  try:
    t = linkdb[code]
  except:
    t = 'Code: ' + code + ' does not exist'
  return t

def add_link(url):
  shorturl_code = generate_url_code()

  while linkdb.get(shorturl_code) is not None:
    shorturl_code = generate_url_code()
  
  shorturl = 'jurl.rf.gd/' + shorturl_code
  
  linkdb[shorturl_code] = url
  linkdb.commit()
  print('Added short url: ' + shorturl + ' ' + url)
  return shorturl

def addcustom_link(url, shorturl_code):
  while linkdb.get(shorturl_code) is not None:
    shorturl_code = generate_url_code()
  
  shorturl = 'jurl.rf.gd/' + shorturl_code
  
  linkdb[shorturl_code] = url
  linkdb.commit()
  print('Added custom short url: ' + shorturl + ' ' + url)
  return shorturl

def remove_link(code):
  t = linkdb.pop(code, None)
  linkdb.commit()
  if(t != None):
    print("Removed URL: jurl.rf.gd/" + code)
  return 'URL does not exist' if t == None else 'URL removed'

def con_login(username, password):
  if os.getenv('USERNAME') == username and os.getenv('PASSWORD') == password:
    return True
  return False

class conSwitch:
  @case("add")
  def caseAdd(ctx):
    ctx = add_link(args[0])
    return ctx
  
  @case("addc")
  def caseAddc(ctx):
    ctx = addcustom_link(args[0], args[1])
    return ctx

  @case("get")
  def caseGet(ctx):
    ctx = get_link(args[0])
    return ctx
  
  @case("getall")
  def caseGetAll(ctx):
    ret = ""
    for key in linkdb.keys():
      _ret = " -> ".join([key, linkdb[key]])
      ret += _ret
      ret += '<br>'
    ctx = ret
    return ctx
  
  @case("remove")
  def caseRemove(ctx):
    ctx = remove_link(args[0])
    return ctx

  @case("login")
  def caseLogin(ctx):
    print("Login requested")
    ctx = "Successfully logged in to https://jurl.jelka33.repl.co/con"
    return ctx
  
  @case("__default__")
  def __default__(ctx):
    print("Error command not found")
    return ctx


@app.route('/')
def root():
  return "<h1>Jelka URL Shortener</h1> \
          <p>jurl.rf.gd</p>"

@app.route('/get-link', methods=['GET', 'POST'])
def get_link_page():
  data = request.args
  return get_link(data['code'])

@app.route('/add-link', methods=['GET', 'POST'])
def add_link_page():
  data = request.args
  return add_link(data['url'])

@app.route('/add-custom-link', methods=['GET', 'POST'])
def add_custom_link_page():
  data = request.args
  return addcustom_link(data['url'], data['code'])

@app.route('/con', methods=['GET', 'POST'])
def con_page():
  data = request.form
  if con_login(data['username'], data['password']):
    global args
    args = data['args'].split(',')

    t = enable(conSwitch, data['cmd'])
    args.clear()
    
    return {'msg': (t if t != None else 'Command not found') + '<br>', 'login': 'success'}

  return {'msg': 'Failed to login: wrong username or password<br>', 'login': 'fail'}

app.run(host='0.0.0.0', port=8080)