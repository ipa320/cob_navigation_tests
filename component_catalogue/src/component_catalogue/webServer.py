#!/usr/bin/env python
import roslib
roslib.load_manifest( 'component_catalogue' )
import rospy

import SimpleHTTPServer, SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from navigation_test_helper.git import Git
from navigation_test_helper.resultRepository import ResultRepository
import os, json, urllib, urllib2

os.chdir( os.path.dirname( os.path.realpath( __file__ )))

class WebServer( ThreadingMixIn, HTTPServer ):
    daemon_threads = True

    def __init__( self, port, repository, videoServer ):
        self._repository  = repository
        self._videoServer = videoServer
        HTTPServer.__init__( self, ( '', port ), Handler )

    def updateRepository( self ):
        self._repository.pull()

    def concatedResults( self ):
        rep  = ResultRepository( self._repository )
        data = rep.concated()
        self.insertVideoUrl( data )
        return data

    def insertVideoUrl( self, tests ):
        filenames  = map( lambda x: x[ 'filename' ], tests )
        postfields = { 'filenames': json.dumps( filenames )}
        req = urllib2.Request( url  = '%s/videosExist' % self._videoServer,
                data = urllib.urlencode( postfields ))
        try:
            f = urllib2.urlopen( req )
            videoUrls = json.loads( f.read())
            for i in xrange( len( videoUrls )):
                test     = tests[ i ]
                videoUrl = videoUrls[ i ]
                if videoUrl:
                    test[ 'video' ] = self._videoServer + videoUrl
                else:
                    test[ 'video' ] = 'No video available'

        except urllib2.HTTPError,e:
            for test in tests:
                test[ 'video' ] = 'Video Server Error'
        except urllib2.URLError,e:
            for test in tests:
                test[ 'video' ] = 'Could not connect to server'

class Handler( SimpleHTTPRequestHandler ):
    def do_GET( self ):
        if self.path == '/':
            self.send_response( 301 )
            self.send_header( 'Location', '/ui/' )
            self.end_headers()

        elif self.path == '/data':
            self.server.updateRepository()
            data = self.server.concatedResults()
            self.sendJson( data )
        else:
            SimpleHTTPRequestHandler.do_GET( self )

    def sendJson( self, data ):
        self.send_response( 200 )
        self.send_header( 'Content-Type', 'application/json' )
        self.end_headers()
        self.wfile.write( json.dumps( data ))

if __name__ == '__main__':
    rospy.init_node( 'server' )
    port = int( rospy.get_param( '~port' ))
    repositoryName = rospy.get_param( '~repository' )
    videoServer = rospy.get_param( '~videoServer' )
    git = Git( repositoryName )
    with git as repository:
        server = WebServer( port, repository, videoServer )
        server.serve_forever()
