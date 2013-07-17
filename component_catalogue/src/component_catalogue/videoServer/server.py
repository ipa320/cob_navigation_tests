#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading, os, sys, urlparse, json, cgi

class MissingParameterException( Exception ):
    def __init__( self, field ):
        Exception.__init__( self, 'The following required parameter was missing: %s' % field )

class Handler( BaseHTTPRequestHandler ):

    def do_POST(self):
        try:
            parsedUrl  = urlparse.urlparse( self.path )
            path   = parsedUrl.path
            params = urlparse.parse_qs( parsedUrl.query )

            if path == '/videosExist':
                data = self.getPostVars()
                self.sendJson( data )
                #if not 'files' in self.params:
                    #raise MissingArgumentError( 'files' )
                #files = 

            elif 'play' in params:
                size = os.path.getsize( 'sample_iPod.m4v' )
                self.send_response( 200 )
                self.send_header( 'Content-Type', 'video/x-m4v' )
                self.send_header( 'Connection', 'close' )
                self.send_header( 'Content-Length', size )
                self.send_header( 'Cache-Control', 'max-age=31536000' )
                self.end_headers()
                with open( 'videoServer/sample_iPod.m4v', 'rb' ) as f:
                    self.wfile.write( f.read() )

            else:
                self.send_response( 404 )
                self.end_headers()

        except MissingParameterException, e:
            self.send_response( 400 )
            self.send_header( 'Content-Type', 'text/plain' )
            self.end_headers()
            self.wfile.write( str( e ))

    def getPostVars( self ):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def sendJson( self, data ):
        self.send_response( 200 )
        self.send_header( 'Content-Type', 'application/json' )
        self.end_headers()
        self.wfile.write( json.dumps( data ))

class ThreadedHTTPServer( HTTPServer ):#ThreadingMixIn, HTTPServer ):
    """Handle requests in a separate thread."""
    def finish_request( self, *args ):
        try:
            return HTTPServer.finish_request( self, *args )
        except IOError,e:
            if e.errno == errno.EPIPE: pass
            else: raise e

if __name__ == '__main__':
    server = ThreadedHTTPServer(( 'localhost', 8000 ), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
