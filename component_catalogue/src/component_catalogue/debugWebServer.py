#!/usr/bin/env python
import SimpleHTTPServer, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os, json, sys, urlparse, urllib2, urllib

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

    def insertVideoUrl( self, tests ):
        filenames  = map( lambda x: x[ 'filename' ], tests )
        postfields = { 'filenames': json.dumps( filenames )}
        req = urllib2.Request( url  = '%s/videosExist' % self.videoServer,
                data = urllib.urlencode( postfields ))
        try:
            f = urllib2.urlopen( req )
            videoUrls = json.loads( f.read())
            for i in xrange( len( videoUrls )):
                test     = tests[ i ]
                videoUrl = videoUrls[ i ]
                if videoUrl:
                    test[ 'video' ] = self.videoServer + videoUrl
                else:
                    test[ 'video' ] = 'No video available'

        except urllib2.HTTPError,e:
            for test in tests:
                test[ 'video' ] = 'Video Server Error'
        except urllib2.URLError,e:
            for test in tests:
                test[ 'video' ] = 'Could not connect to server'
        

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
