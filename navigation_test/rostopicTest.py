import roslib
roslib.load_manifest( 'navigation_test' )
import rospy
from gazebo_msgs.msg import ModelStates
import sys

def callback( data ):
    index = data.name.index( 'robot' )
    pose = data.pose[ index ]
    print pose

def listener():
    rospy.init_node( 'Test', anonymous=True )
    rospy.Subscriber( '/gazebo/model_states', ModelStates, callback )
    rospy.spin()

listener()
