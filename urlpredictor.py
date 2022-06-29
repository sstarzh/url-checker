#!/usr/bin/env python3

import argparse, os, random, sys
import numpy as np
#import pickle
import urllib.parse
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID";
os.environ["CUDA_VISIBLE_DEVICES"]="0";
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import json
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

load_my_model = 'distilbert'
def set_header():
    headers = {
        'Host': hostname
    }

    return headers
def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Proxy HTTP requests')
    parser.add_argument('--port', dest='port', type=int, default=8081,
                        help='serve HTTP requests on specified port (default: random)')
    parser.add_argument('--ip', dest='ip', type=str, default='127.0.0.1',
                        help='listen on IP (default: 127.0.0.1')
    parser.add_argument('--proto', dest='protocol', type=str, default='http',
                        help='protocol - either http or https (default: http')
    parser.add_argument('--model', dest='load_my_model', type=str, default='distilbert',
                        help='Predictor model to use (default: distilbert)')
    args = parser.parse_args(argv)
    return args
args = parse_args()
print(args)

def proc(req):
        path = urllib.parse.unquote(req)
        try:
            text = path.split('?')[1]
        except:
            text = path
        new_model = ml_model()
        result = new_model.predict(text)
        print(result)
        resp = result
        return resp

def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def do_POST(self, body=True):
        postvars = self.parse_POST()
        result = proc(postvars.URL)
        data = {}
        data['inference'] = result
        json_data = json.dumps(data)
        self.send_response(200, json_data)
        self.send_header("Content-Type", "application/json")
        self.send_header('Content-Length', len(json_data))
        self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""
def main(argv=sys.argv[1:]):
    global hostname
    global protocol
    args = parse_args(argv)
    hostname = args.hostname
    print('http server is starting on {} port {}...'.format(args.ip, args.port))
    server_address = (args.ip, args.port)
    protocol = args.protocol
    httpd = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
    httpd.serve_forever()
def ml_model():
    #predictor = ktrain.load_predictor(args.load_my_model)
    #new_model = ktrain.get_predictor(predictor.model, predictor.preproc)
    predictor = load_model(load_my_model)
    new_model = predictor
    return new_model
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass