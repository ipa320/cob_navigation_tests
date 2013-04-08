import roslib
roslib.load_manifest( 'navigation_test' )
import rospy
import std_srvs.srv

reset_service = rospy.ServiceProxy( '/gazebo/reset_world', std_srvs.srv.Empty )
reset_service()
