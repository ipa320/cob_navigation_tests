import navigation_test.msg
import rospy

class NavigationStatusPublisher( object ):
    def __init__( self, topic ):
        self._waypointNo = -1
        self._nextWaypoint = None
        self._start = None
        self._publisher = rospy.Publisher( topic, navigation_test.msg.Status )

    def nextWaypoint( self, waypoint):
        self._waypointNo += 1
        if not self._start:
            self._start = rospy.Time.now()
        self._nextWaypoint = waypoint
        msg = self._createMsg()
        self._publisher.publish( msg )

    def finished( self ):
        msg = self._createMsg( 'finished' )
        self._publisher.publish( msg )

    def _createMsg( self, info='' ):
        waypoint = self._nextWaypoint
        msg = navigation_test.msg.Status()
        msg.header.stamp = rospy.Time.now()
        msg.info = info
        msg.start = self._start
        msg.waypointId = self._waypointNo
        if waypoint:
            msg.waypointX = waypoint[ 0 ]
            msg.waypointY = waypoint[ 1 ]
            msg.waypointTheta = waypoint[ 2 ]
        return msg
