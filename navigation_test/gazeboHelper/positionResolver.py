import tf
import rospy
from tf.transformations import euler_from_quaternion
from position import Position

class PositionResolver( object ):
    def __init__( self ):
        self.transformListener = tf.TransformListener()
        self.transformListener.waitForTransform( '/map', '/base_link', rospy.Time( 0 ), 
            rospy.Duration( 300.0 ) )

    def getPosition( self ):
        #self.transformListener.waitForTransform( '/map', '/base_link', rospy.Time( 0 ), 
            #rospy.Duration( 3.0 ) )
        pos, rot = self.transformListener.lookupTransform(
            '/map', '/base_link', rospy.Time( 0 ))
        return self._rawToPositionObject( pos, rot )

    def _rawToPositionObject( self, pos, rot ):
        x,y,z = pos
        angles = euler_from_quaternion( rot )
        theta = angles[ 2 ]
        return Position( x, y, theta )

    def inPosition( self, target, tolerance ):
        position = self.getPosition()
        absDiff = ( position - target ).abs()
        return absDiff.x < tolerance.xy and absDiff.y < tolerance.xy and \
                absDiff.theta < tolerance.theta
