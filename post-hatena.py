# -*- coding: utf-8 -*-
import datetime
import random
import hashlib
import base64
import requests
import sys

username = 'username'
password = 'API key'
blogname = 'yourblogname.hatenablog.com'
 
def wsse(username, password):
    created = datetime.datetime.now().isoformat() + 'Z'
    nonce = hashlib.sha1(str(random.random())).digest()
    digest = hashlib.sha1(nonce + created + password).digest()
    
    return 'UsernameToken Username="{}", PasswordDigest="{}", Nonce="{}", Created="{}"'.format(username, base64.b64encode(digest), base64.b64encode(nonce), created)


def posthatena(data):
    headers = {'X-WSSE': wsse(username, password)}

    url = 'http://blog.hatena.ne.jp/{}/{}/atom/entry'.format(username, blogname)

    r = requests.post(url, data=data, headers=headers)
    print (r)

if __name__ == '__main__':

    param = sys.argv
    if (len(param) != 3):
        print ("Usage: $ python " + param[0] + " title.txt body.txt")
        quit()  

    f = open(param[1])
    title = f.read()
    f.close()

    f = open(param[2])
    body = f.read()
    f.close()

    data = """<?xml version="1.0" encoding="utf-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
           xmlns:app="http://www.w3.org/2007/app">
      <title>""" + title + """</title>
      <author><name>name</name></author>
      <content type="text/plain">
        """ + body + """
      </content>
      <category term="1日100記事" />
      <app:control>
        <app:draft>no</app:draft>
      </app:control>
    </entry>
    """

    posthatena(data)
