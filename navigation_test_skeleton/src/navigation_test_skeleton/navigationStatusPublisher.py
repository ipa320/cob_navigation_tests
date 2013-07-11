import navigation_test_helper.msg
import rospy, time

class NavigationStatusPublisher( object ):
    def __init__( self, topic, setting ):
        self._waypointNo   = -1
        self._nextWaypoint = None
        self._localtime    = time.time()
        self._publisher    = rospy.Publisher( topic, navigation_test_helper.msg.Status )
        self._setting      = setting

    def nextWaypoint( self, waypoint):
        self._waypointNo += 1
        self._nextWaypoint = waypoint
        msg = self._createMsg( info='running' )
        self._publisher.publish( msg )

    def failed( self, errorCode ):
        msg = self._createMsg( info='finished', error='failed:%s' % errorCode )
        self._publisher.publish( msg )

    def timedout( self ):
        msg = self._createMsg( info='finished', error='timedout' )
        self._publisher.publish( msg )

    def missed( self ):
        msg = self._createMsg( info='finished', error='missed' )
        self._publisher.publish( msg )

    def finished( self ):
        msg = self._createMsg( info='finished' )
        self._publisher.publish( msg )

    def _createMsg( self, info='', error='' ):
        waypoint          = self._nextWaypoint
        msg               = navigation_test_helper.msg.Status()
        msg.header.stamp  = rospy.Time.now()
        msg.info          = info
        msg.error         = error
        msg.localtime     = self._localtime
        msg.waypointId    = self._waypointNo
        msg.setting       = self._createSettingMsg()
        if waypoint:
            msg.waypointX = waypoint[ 0 ]
            msg.waypointY = waypoint[ 1 ]
            msg.waypointTheta = waypoint[ 2 ]
        return msg

    def _createSettingMsg( self ):
        msg = navigation_test_helper.msg.Setting()
        msg.robot      = self._setting[ 'robot' ]
        msg.scenario   = self._setting[ 'scenario' ]
        msg.navigation = self._setting[ 'navigation' ]
        msg.repository = self._setting[ 'repository' ]
        return msg
