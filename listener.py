#!/usr/bin/env python3

from flask import Flask, request
import json
import pprint
import plex_notify as plex

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=2)


# https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks
# As stated above, the payload is sent in JSON format inside a multipart
# HTTP POST request. For the media.play and media.rate events, a second part of
# the POST request contains a JPEG thumbnail for the media.

@app.route('/', methods=['POST'])
def foo():
    data = json.loads(request.form['payload'])
    pp.pprint(data)
    plex.process_event(data)
    return "OK"


if __name__ == '__main__':
    app.run()
