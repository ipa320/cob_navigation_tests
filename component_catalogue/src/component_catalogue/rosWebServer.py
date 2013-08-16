#!/usr/bin/env python
import roslib
roslib.load_manifest( 'component_catalogue' )
import rospy
from webServer import WebServer
from navigation_test_helper.git import Git

if __name__ == '__main__':
    rospy.init_node( 'server' )
    port = int( rospy.get_param( '~port' ))
    repositoryName = rospy.get_param( '~repository' )
    videoServer = rospy.get_param( '~videoServer' )
    git = Git( repositoryName )
    with git as repository:
        server = WebServer( port, repository, videoServer )
        server.serve_forever()
