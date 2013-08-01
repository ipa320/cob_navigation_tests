#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_prepare_robot' )
import rospy, time
from simple_script_server       import simple_script_server
from navigation_test_helper.srv import SetupRobotService

def setupRobotService( serviceName ):
    rospy.loginfo( 'Creating setup service %s' % serviceName )
    rospy.Service( serviceName, SetupRobotService, setupRobot )

def setupRobot( req ):
    rospy.loginfo( 'Moving robot arm to home position' )
    scriptServer = simple_script_server()
    scriptServer.move( 'arm', 'folded', blocking=True )
    scriptServer.move( 'tray', 'down', blocking=True )
    return True, ''

if __name__=='__main__':
    rospy.init_node( 'cob_prepare_robot' )
    serviceName = rospy.get_param( 'setupRobotService' )
    setupRobotService( serviceName )
    rospy.spin()
