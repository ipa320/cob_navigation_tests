import tf
import rospy
from tf.transformations import euler_from_quaternion
from position import Position

class PositionMissedException( Exception ):
    def __init__( self, position, target, tolerance ):
        msg = 'Position %s does not match goal position %s ( tolerance: %s )' % \
                ( position, target, tolerance )
        Exception.__init__( self, msg )

class PositionResolver( object ):
    def __init__( self ):
        self.transformListener = tf.TransformListener()
        self.transformListener.waitForTransform( '/map', '/base_link', rospy.Time( 0 ), 
            rospy.Duration( 300.0 ) )

    def getPosition( self ):
        pos, rot = self.transformListener.lookupTransform(
            '/map', '/base_link', rospy.Time( 0 ))
        return self._rawToPositionObject( pos, rot )

    def _rawToPositionObject( self, pos, rot ):
        x,y,z = pos
        angles = euler_from_quaternion( rot )
        theta = angles[ 2 ]
        return Position( x, y, theta )

    def assertInPosition( self, targetPosition, tolerance ):
        position = self.getPosition()
        if not self.inPosition( targetPosition, tolerance ):
            raise PositionMissedException( position, targetPosition, tolerance )

    def inPosition( self, target, tolerance ):
        position = self.getPosition()
        absDiff = ( position - target ).abs()
        return absDiff.x < tolerance.xy and absDiff.y < tolerance.xy and \
                absDiff.theta < tolerance.theta
