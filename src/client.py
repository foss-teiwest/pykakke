from sys import argv
from tornado.httpclient import HTTPError, HTTPClient as Client
from tornado.escape import json_decode as decode
client = Client()

try:
    url = argv[1]
except IndexError:
    print('Connecting to localhost')
    url = 'http://localhost:8888/'

pos = 0
timeout = 20

while True:
    try:
        resp = client.fetch(url + str(pos), request_timeout=timeout)
        d = decode(resp.body)
        pos = d['pointer']
        line = d['text']
        print(line.rstrip('\n'))
    except HTTPError as e:
        #print(e)
        if not 'imeout' in str(e):
            print(e)
            break
    except KeyboardInterrupt:
        print('Closed by user')
        break

