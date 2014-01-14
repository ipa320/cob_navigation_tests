import tf
import rospy
from tf.transformations import euler_from_quaternion
from position import Position
from threading import RLock

class PositionMissedException( Exception ):
    def __init__( self, position, target, tolerance ):
        msg = 'Position %s does not match goal position %s ( tolerance: %s )' % \
                ( position, target, tolerance )
        Exception.__init__( self, msg )

class PositionResolver( object ):
    _tfListener = None

    def __init__( self ):
        self._lock = RLock()

    def initialize( self, timeout=None ):
        if not timeout:
            while not rospy.is_shutdown() and not self.isInitialized():
                self._initializeOnce( 5 )
        else:
            self._initializeOnce( timeout )

    def _initializeOnce( self, timeout=5.0 ):
        with self._lock:
            if self.isInitialized(): return True
            try:
                tfListener = tf.TransformListener()
                tfListener.waitForTransform( '/map', '/base_link',
                        rospy.Time( 0 ), rospy.Duration( timeout ))
                PositionResolver._tfListener = tfListener
                return True
            except tf.Exception,e:
                print 'Could not get transformation from /map to /base_link within timeout'
                return False

    def isInitialized( self ):
        with self._lock:
            return PositionResolver._tfListener != None

    def getPosition( self ):
        pos, rot = PositionResolver._tfListener.lookupTransform(
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
