#!/usr/bin/env python
''' Generic Interface for MDPs to MDPVis; 
    output format supported = json '''
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from urlparse import urlparse, parse_qs

#
# Return data
#
def get_initialize(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_initialize'}

def get_rollouts(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_rollouts'}

def get_state(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_state'}

def get_optimize(query):
    # Hailey todo: return an object following the spec Sean Provides
    return {'todo':'get_optimize'}

# Request Handlers
class Handler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):
        parsedQuery = urlparse(self.path)
        path = parsedQuery[2]
        print("processing get request:" + path)
        queryString = parsedQuery[4]
        queryDict = parse_qs(queryString)# todo, send this to the get_rollouts function
        
        if path == "/initialize":
            ret = json.dumps(get_initialize(queryDict))
            self.request.sendall(ret)
        elif path == "/rollouts":
            ret = json.dumps(get_rollouts(queryDict))
            self.request.sendall(ret)
        elif path == "/state":
            ret = json.dumps(get_state(queryDict))
            self.request.sendall(ret)
        elif path == "/optimize":
            ret = json.dumps(get_optimize(queryDict))
            self.request.sendall(ret)
        else:
            # Serve the visualization's files
            try:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        return

# Starting Server
#note that this potentially makes every file on your computer readable by the internet
def run(port=8000):

    print('http server is starting...')
    print('note that this could potentially make all your files readable over the internet')
    server_address = ('127.0.0.1', port) #ip and port of server
    httpd = HTTPServer(server_address, Handler)
    print('http server is running...listening on port %s' %port)
    httpd.serve_forever()

if __name__ == '__main__':
    from optparse import OptionParser
    op = OptionParser(__doc__)
    op.add_option("-p", default=8000, type="int", dest="port", 
                  help="port #")
    opts, args = op.parse_args(sys.argv)
    run(opts.port)