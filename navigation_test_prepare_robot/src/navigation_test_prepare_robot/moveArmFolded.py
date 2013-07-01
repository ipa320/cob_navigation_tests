#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_prepare_robot' )
import rospy, time
from simple_script_server import simple_script_server
import std_msgs

if __name__=='__main__':
    publisher = rospy.Publisher( '/navigation_test/robot_ready', 
            std_msgs.msg.String )
    rospy.init_node( 'moveArmFolded' )
    rospy.loginfo( 'Moving robot arm to home position' )
    scriptServer = simple_script_server()
    scriptServer.move( 'arm', 'folded', True )
    
    i = 0
    while not rospy.is_shutdown():
        publisher.publish( 'robot ready, #%d' % i )
        time.sleep( 1 )
        i += 1
