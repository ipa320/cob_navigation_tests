import actionlib
import rospy
import geometry_msgs.msg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

class Navigator( object ):
    def __init__( self, action_name ):
        self.action_name = action_name
        self.move_client = actionlib.SimpleActionClient( self.action_name, 
                MoveBaseAction)
        self.move_client.wait_for_server()


    def goTo( self, goal ):
        posMsg = self._createGoalMessage( goal )
        self.pub_goal =  MoveBaseGoal( posMsg ) 
        self.move_client.send_goal( self.pub_goal )
    
    def waitForResult( self, timeout=30.0 ):
        self.move_client.wait_for_result(rospy.Duration( timeout ))

    def _createGoalMessage( self, goal ):
        msg = geometry_msgs.msg.PoseStamped()
        msg.header.frame_id = '/map'
        msg.header.stamp = rospy.get_rostime()
        msg.pose.position.x = goal.x
        msg.pose.position.y = goal.y
        quat = quaternion_from_euler( 0, 0, goal.theta )
        msg.pose.orientation.x = quat [0]
        msg.pose.orientation.y = quat [1]
        msg.pose.orientation.z = quat [2]
        msg.pose.orientation.w = quat [3]
        return msg

    def _createStateMessage( self, position ):
        req = SetModelStateRequest()
        state = req.model_state
        position, orientation = state.pose.position, state.pose.orientation

        state.model_name = 'robot'
        position.x, position.y, position.z = position.x, position.y, 0.01

        quat = quaternion_from_euler( 0, 0, goal.theta )
        orientation.x = quat [0]
        orientation.y = quat [1]
        orientation.z = quat [2]
        orientation.w = quat [3]
