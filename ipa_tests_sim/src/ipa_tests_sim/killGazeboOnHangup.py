#!/usr/bin/env python
import roslib
roslib.load_manifest( 'ipa_tests_sim' )

import rospy
from gazebo_msgs.msg import ModelStates
import time, subprocess, os.path

stateReceived = False
def callback( msg ):
    global stateReceived
    stateReceived = True

def killAllRosAndGazebo():
    path = os.path.dirname( os.path.abspath( __file__ ))
    cmd = '%s/killAllRosAndGazebo.bash' % path
    subprocess.call([ cmd ])


if __name__ == '__main__':
    rospy.init_node( 'killGazeboOnHangup' )
    subscriber = rospy.Subscriber( '/gazebo/model_states', ModelStates, callback )
    time.sleep( 30 )
    if not stateReceived:
        killAllRosAndGazebo()
