#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading, os, sys, urlparse, json, cgi

class MissingParameterException( Exception ):
    def __init__( self, field ):
        Exception.__init__( self, 'The following required parameter was missing: %s' % field )

class Handler( BaseHTTPRequestHandler ):

    def do_POST( self ):
        path, params = self.parseUrl()
        if path == '/videosExist':
            data     = self.getPostVar( 'filenames' )
            jsonData = json.loads( data )
            result   = map( self.getVideoRemotePathForBagfile, jsonData )
            self.sendJson( result )
        else:
            self.send_response( 404 )
            self.end_headers()


    def do_GET( self ):
        path, params = self.parseUrl()
        bagFilename  = path.lstrip( '/' )
        absPath      = self.getVideoLocalPathForBagfile( bagFilename )
        if absPath == False:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( 'File not found\n' )
        else:
            self.sendVideo( absPath )


    def sendVideo( self, absPath ):
        size = os.path.getsize( absPath )
        self.send_response( 200 )
        self.send_header( 'Content-Type',   'video/x-m4v' )
        self.send_header( 'Connection',     'close' )
        self.send_header( 'Content-Length', size )
        self.send_header( 'Cache-Control',  'max-age=31536000' )
        self.end_headers()
        with open( absPath, 'rb' ) as f:
            self.wfile.write( f.read() )

    def parseUrl( self ):
        parsedUrl  = urlparse.urlparse( self.path )
        path   = parsedUrl.path
        params = urlparse.parse_qs( parsedUrl.query )
        return path, params


    def getVideoRemotePathForBagfile( self, filename ):
        absPath = self.getVideoLocalPathForBagfile( filename )
        if absPath:
            return '/%s' % filename
        return False

    def getVideoLocalPathForBagfile( self, filename ):
        filename   = filename + '.m4v'
        videoPath  = self.server.videoPath
        absPath    = '%s/%s' % ( videoPath, filename )
        if os.path.isfile( absPath ):
            return absPath
        return False


    def getPostVar( self, fieldname ):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        return postvars[ fieldname ][ 0 ] if fieldname in postvars else None


    def sendJson( self, data ):
        self.send_response( 200 )
        self.send_header( 'Content-Type', 'application/json' )
        self.end_headers()
        self.wfile.write( json.dumps( data ))


class ThreadedHTTPServer( HTTPServer ):#ThreadingMixIn, HTTPServer ):
    def __init__( self, *args ):
        self.videoPath = os.path.dirname( os.path.abspath( __file__ ))
        HTTPServer.__init__( self, *args )

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
