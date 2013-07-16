#!/usr/bin/env python
import SimpleHTTPServer, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os, json, sys

os.chdir( os.path.dirname( os.path.realpath( __file__ )))

class MyServer( SocketServer.TCPServer ):
    allow_reuse_address = True
    def __init__( self, port, resultsData ):
        self._resultsData = resultsData
        SocketServer.TCPServer.__init__( self, ( "", port ), MyHandler )

    def concatedResults( self ):
        return self._resultsData

class MyHandler( SimpleHTTPRequestHandler ):
    def do_GET( self ):
        if self.path == '/':
            self.send_response( 301 )
            self.send_header( 'Location', '/ui/' )
            self.end_headers()

        elif self.path == '/data':
            self.send_response( 200 )
            self.end_headers()
            data = self.server.concatedResults()
            self.wfile.write( json.dumps( data ))
        else:
            SimpleHTTPRequestHandler.do_GET( self )

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
    server.serve_forever()
