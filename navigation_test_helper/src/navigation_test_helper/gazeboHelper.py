import sys, threading, signal
import rospy, rospy.exceptions

import std_srvs
import std_msgs
import geometry_msgs.msg
import gazebo_msgs.msg
import gazebo_msgs.srv
from tf.transformations import quaternion_from_euler


std = sys.stdout

def resetTime():
    pub = rospy.Publisher('/reset_time', std_msgs.msg.Empty )
    print "Resetting time"
    time.sleep(1)
    pub.publish( std_msgs.msg.Empty() )


def resetWorld():
    service = rospy.ServiceProxy( '/gazebo/reset_world', std_srvs.srv.Empty )
    service()
    
def resetSimulation():
    service = rospy.ServiceProxy( '/gazebo/reset_simulation', std_srvs.srv.Empty )
    service()


class ModelStateSetter( object ):
    def __init__( self, modelName ):
        self._modelName = modelName

    def set( self, position, z=0, R=0, P=0 ):
        service = self._getServiceProxy()

        modelState = gazebo_msgs.srv.SetModelState()

        start_pose = geometry_msgs.msg.Pose()
        start_pose.position.x = position.x
        start_pose.position.y = position.y
        start_pose.position.z = z

        quaternion = quaternion_from_euler( R, P, position.theta )
        start_pose.orientation.x = quaternion[ 0 ]
        start_pose.orientation.y = quaternion[ 1 ]
        start_pose.orientation.z = quaternion[ 2 ]
        start_pose.orientation.w = quaternion[ 3 ]

        start_twist = geometry_msgs.msg.Twist()
        start_twist.linear.x  = 0.0
        start_twist.linear.y  = 0.0
        start_twist.linear.z  = 0.0
        start_twist.angular.x = 0.0
        start_twist.angular.y = 0.0
        start_twist.angular.z = 0.0

        modelstate = gazebo_msgs.msg.ModelState
        modelstate.model_name = self._modelName
        modelstate.reference_frame = "/map";
        modelstate.pose =  start_pose;
        modelstate.twist = start_twist;
        return service( modelstate )

    # Lazy loading, get service proxy only when required
    def _getServiceProxy( self ):
        if hasattr( self, '_serviceProxy' ):
            return self._serviceProxy
        rospy.wait_for_service( '/gazebo/set_model_state' )
        self._serviceProxy = rospy.ServiceProxy( '/gazebo/set_model_state', \
                gazebo_msgs.srv.SetModelState )
        return self._serviceProxy
