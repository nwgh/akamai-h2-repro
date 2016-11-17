#!/usr/bin/env python

# https://h[12].test-drive.me.uk/experiments/<type>/<filename>.php?n=<number>
# <type> images <filename> imgfiles
# <type> js <filename> jsfiles
# <type> css <filename> cssfiles
# number = 1-1000

import os

from flask import Flask, make_response, render_template, request

app = Flask('akamai_h2')

@app.route('/')
def index():
    return '<!DOCTYPE html><html><head><title>WAT</title></head><body>WAT</body></html>'

@app.route('/jstest')
def jstest():
    return make_css_js(js=True)

@app.route('/csstest')
def csstest():
    return make_css_js(css=True)

def get_http_version():
    if os.getenv('HTTP2'):
        return 2
    return 1

def make_css_js(js=False, css=False):
    n = int(request.args.get('n', 1))
    data = render_template('css_js.html', http_version=get_http_version(), n=n, css=css, js=js)
    response = make_response(data, 200)
    response.headers['content-type'] = 'text/html'
    # XXX - maybe set x-powered-by, date

    return response

@app.route('/js_<int:per_part>_<int:part>.js')
def serve_js(per_part, part):
    first_div = (per_part * (part - 1)) + 1
    last_div = per_part * part
    output = ''
    for div_num in range(first_div, last_div + 1):
        output += "document.getElementById('div%d').style.backgroundColor = 'red'; " % (div_num,)

    response = make_response(output, 200)
    response.headers['content-type'] = 'application/javascript'
    # XXX - maybe set etag, content-length, date (now), expires (now + 1 week), last-modified, max-age (604800) depending on what apache gives

    return response

@app.route('/css_<int:per_part>_<int:part>.css')
def serve_css(per_part, part):
    first_div = (per_part * (part - 1)) + 1
    last_div = per_part * part
    output = ''
    for div_num in range(first_div, last_div + 1):
        output += '#div%d {width:20px;height:20px;background-color:#000000;float:left;margin:1px;} ' % (div_num,)

    response = make_response(output, 200)
    response.headers['content-type'] = 'text/css'
    # XXX - maybe set etag, content-length, date (now), expires (now + 1 week), last-modified, max-age (604800) depending on what apache gives

    return response

@app.route('/imgtest')
def imgtest():
    n = int(request.args.get('n', 1))
    data = render_template('image.html', http_version=get_http_version(), n=n)
    response = make_response(data, 200)
    response.headers['content-type'] = 'text/html'
    # XXX - maybe set content-length, date, x-powered-by

    return response

@app.route('/image_<int:per_part>.jpg')
def serve_image(per_part):
    data = file('image.jpg').read()
    response = make_response(data, 200)
    response.headers['content-type'] = 'image/jpeg'
    # XXX - maybe set etag, content-length, date (now), expires (now + 1 week), last-modified, max-age (604800) depending on what apache gives

    return response