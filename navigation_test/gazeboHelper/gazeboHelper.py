import sys, threading, signal
import actionlib
import rostest
import rospy, rospy.exceptions
import tf

from math import *

import time,json

from tf.msg import tfMessage 
from tf.transformations import euler_from_quaternion

from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import *
from nav_msgs.srv import *

from gazebo.srv import *
from gazebo_msgs.srv import *
from gazebo_msgs.msg import *

from simple_script_server import *
import std_srvs.srv
import yaml

std = sys.stdout

def resetWorld():
    service = rospy.ServiceProxy( '/gazebo/reset_world', std_srvs.srv.Empty )
    service()
    
def resetSimulation():
    service = rospy.ServiceProxy( '/gazebo/reset_simulation', std_srvs.srv.Empty )
    service()






class SimpleFileWriter( object ):
    def __init__( self, filename ):
        self._filename = filename
        self._values = {}

    def write( self, key, value ):
        self._values[ key ] = value

    def flush( self ):
        if not self._values:
            return

        with open( self._filename, 'a+'  ) as f:
            for key, value in self._values.items():
                f.write( '%s: %s, ' % ( key, value ))
            f.write( '\n' )
        self._values = {}

