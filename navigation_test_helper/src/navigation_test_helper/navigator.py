import actionlib
import rospy
import geometry_msgs.msg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from tf.transformations import quaternion_from_euler
import threading

class NavigationFailedException( Exception ):
    def __init__( self, errorCode ):
        self.errorCode = errorCode
        msg = 'Navigation failed to navigate. ErrorCode: %s' % errorCode
        Exception.__init__( self, msg )

class GoalResultWaiter( threading.Thread ):
    def __init__( self, move_client, timeoutInS ):
        threading.Thread.__init__( self )
        self._move_client = move_client
        self._timeoutInS  = timeoutInS
        self._lock        = threading.Lock()
        self._success     = False
        self._errorCode   = ''
        self._started     = False
        self._finished    = False

    def run( self ):
        with self._lock:
            self._started = True

        timeoutDuration = rospy.Duration( self._timeoutInS )
        self._move_client.wait_for_result( timeoutDuration )
        state = self._move_client.get_state()

        errorCodes = {
                GoalStatus.SUCCEEDED: '',
                GoalStatus.ABORTED:   'aborted',
                'default':            'failed'
        }
        with self._lock:
            errorKey = state if state in errorCodes else 'default'
            self._success   = state == GoalStatus.SUCCEEDED
            self._errorCode = errorCodes[ errorKey ]
            self._finished = True

    def block( self ):
        self.join()
        return self.wasSuccessfull()

    def wasSuccessfull( self ):
        with self._lock:
            return self._success

    def assertSucceeded( self ):
        if not self.wasSuccessfull():
            raise NavigationFailedException( self._errorCode )

    def hasFinished( self ):
        with self._lock:
            return self._finished

    def hasStarted( self ):
        with self._lock:
            return self._started

class Navigator( object ):
    def __init__( self, action_name ):
        self.action_name = action_name
        self.move_client = actionlib.SimpleActionClient( self.action_name, 
                MoveBaseAction)
        self.move_client.wait_for_server()

    def goTo( self, goal, timeoutInS=0 ):
        goalMsg = self._createGoalMessage( goal )
        self.move_client.send_goal( goalMsg )
        return self._waitForResultNonBlocking( timeoutInS )
    
    def _waitForResultNonBlocking( self, timeoutInS=0 ):
        waiter = GoalResultWaiter( self.move_client, timeoutInS )
        waiter.start()
        return waiter

    def _createGoalMessage( self, goal ):
        poseMsg = self._createPoseMessage( goal )
        return  MoveBaseGoal( poseMsg ) 

    def _createPoseMessage( self, goal ):
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
