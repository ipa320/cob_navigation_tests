#!/usr/bin/env python
import roslib
roslib.load_manifest( 'component_catalogue' )
import rospy

import SimpleHTTPServer, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from navigation_test_helper.git import Git
from navigation_test_helper.resultRepository import ResultRepository
import os, json

os.chdir( os.path.dirname( os.path.realpath( __file__ )))

class MyServer( SocketServer.TCPServer ):
    allow_reuse_address = True
    def __init__( self, port, repository ):
        self._repository = repository
        SocketServer.TCPServer.__init__( self, ( "", port ), MyHandler )

    def updateRepository( self ):
        self._repository.pull()

    def concatedResults( self ):
        rep = ResultRepository( self._repository )
        return rep.concated()

class MyHandler( SimpleHTTPRequestHandler ):
    def do_GET( self ):
        if self.path == '/':
            self.send_response( 301 )
            self.send_header( 'Location', '/ui/' )
            self.end_headers()

        elif self.path == '/data':
            self.send_response( 200 )
            self.end_headers()
            self.server.updateRepository()
            data = self.server.concatedResults()
            self.wfile.write( json.dumps( data ))
        else:
            SimpleHTTPRequestHandler.do_GET( self )

if __name__ == '__main__':
    rospy.init_node( 'server' )
    port = int( rospy.get_param( '~port' ))
    repositoryName = rospy.get_param( '~repository' )
    git = Git( repositoryName )
    with git as repository:
        server = MyServer( port, repository )
        server.serve_forever()
