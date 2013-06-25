import math
import rospy

class MetricsContainer( object ):
    def __init__( self ):
        self._dist, self._distX, self._distY = 0.0, 0.0, 0.0
        self._rotation = 0.0
        self._duration, self._startTime = 'N/A', None
        self._lastPosition = None

    def update( self, position ):
        if not self._startTime and position and self._lastPosition and position != self._lastPosition:
            self._startTime = rospy.Time.now()
        if self._lastPosition is None:
            self._lastPosition = position

        dAbs = ( self._lastPosition - position ).abs()
        dD = math.sqrt( dAbs.x**2 + dAbs.y**2 )

        self._distX += dAbs.x
        self._distY += dAbs.y
        self._dist  += dD
        self._rotation += dAbs.theta * 180 / math.pi
        if self._startTime:
            self._duration = ( rospy.Time.now() - self._startTime ).to_sec()

        self._lastPosition = position

    def start( self ):
        pass

    def stop( self ):
        pass

    def serialize( self ):
        return {
            'distance': self._dist,
            'rotation': self._rotation,
            'duration': self._duration
        }

    def __str__( self ):
        return '<MetricsContainer distance: %s, rotation: %s, duration: %s' %  \
            ( self._dist, self._rotation, self._duration )
