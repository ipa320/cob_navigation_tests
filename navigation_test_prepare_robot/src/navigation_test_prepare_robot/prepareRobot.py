#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_prepare_robot' )
import rospy, time, yaml
from simple_script_server       import simple_script_server
from navigation_test_helper.srv import SetupRobotService

def setupRobotService( serviceName, robotConfig ):
    rospy.loginfo( 'Creating setup service %s' % serviceName )
    serviceCallback = createSetupRobotCallback( robotConfig )
    rospy.Service( serviceName, SetupRobotService, serviceCallback )

def createSetupRobotCallback( robotConfig ):
    return lambda( req ): setupRobot( robotConfig, req )

def setupRobot( robotConfig, req ):
    rospy.loginfo( 'Preparing robot for navigation scenario ...' )
    scriptServer = simple_script_server()
    #config = yaml.load( file( robotConfig, 'r' ))
    #if config:
    #    for key, value in config.items():
    #        rospy.loginfo( 'Moving %s to %s' % ( key, value ))
    #        scriptServer.move( key, value, blocking=True )
    for key, value in robotConfig.items():
        rospy.loginfo( 'Moving %s to %s' % ( key, value ))
        scriptServer.move( key, value, blocking=True )
    return True, ''

if __name__=='__main__':
    rospy.init_node( 'cob_prepare_robot' )
    serviceName = rospy.get_param( 'setupRobotService' )
    robotConfig = rospy.get_param( 'robotConfig' )
    setupRobotService( serviceName, robotConfig )
    rospy.spin()
