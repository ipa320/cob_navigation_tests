#!/usr/bin/env python
import SimpleHTTPServer, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os, json, sys, urlparse, urllib2

os.chdir( os.path.dirname( os.path.realpath( __file__ )))

class MyServer( SocketServer.TCPServer ):
    allow_reuse_address = True
    def __init__( self, port, resultsData ):
        self._resultsData = json.loads( resultsData )
        self.videoServer  = 'http://localhost:8000'
        #SocketServer.TCPServer.__init__( self, ( "", port ), MyHandler )
        self.concatedResults()

    def concatedResults( self ):
        data = self._resultsData
        self.insertVideoUrl( data )
        return data

    def insertVideoUrl( self, data ):
        filenames = map( lambda x: x[ 'filename' ], data )
        req = urllib2.Request( url  = '%s/videosExist' % self.videoServer,
                data = json.dumps( filenames ))
        try:
            f = urllib2.urlopen( req )
            print f.read()
        except urllib2.HTTPError,e:
            print 'server down'
        

class MyHandler( SimpleHTTPRequestHandler ):
    def do_GET( self ):
        parsedUrl  = urlparse.urlparse( self.path )
        path   = parsedUrl.path
        params = urlparse.parse_qs( parsedUrl.query )

        if path == '/':
            self.send_response( 301 )
            self.send_header( 'Location', '/ui/' )
            self.end_headers()

        elif path == '/data':
            data = {
                'testData':    self.server.concatedResults(),
                'videoServer': self.server.videoServer
            }
            self.sendJson( data )

        elif path == '/video':
            self.send_response( 302 )
            self.send_header( 'Location', 'http://localhost:8000%s' % self.path )
            self.end_headers()
            self.wfile.write( 'test' )

        else:
            SimpleHTTPRequestHandler.do_GET( self )


    def sendJson( self, data ):
        self.send_response( 200 )
        self.send_header( 'Content-Type', 'application/json' )
        self.end_headers()
        self.wfile.write( json.dumps( data ))


def printUsageAndExit():
    print 'Usage: [filename]'
    sys.exit( 1 )

def getFilenameFromArgs():
    if not len( sys.argv ) == 2:
        printUsageAndExit()
    return sys.argv[ 1 ]

def getFilecontentFromArgs():
    filename = getFilenameFromArgs()
    with open( filename, 'r' ) as f:
        return f.read()

if __name__=='__main__':
    port        = 9000
    resultsData = getFilecontentFromArgs()
    server      = MyServer( port, resultsData )
    #server.serve_forever()
