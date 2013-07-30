import datetime
import rospy

class TimeoutException( Exception ):
    def __init__( self, timeoutInS ):
        msg = 'Timeout %ss exceeded' % timeoutInS
        Exception.__init__( self, msg )

class WatchDog( object ):
    def __init__( self, timeoutInS ):
        self.timeoutInS = timeoutInS
        self._starttime = rospy.Time.now()

    def assertExecutionTimeLeft( self ):
        now    = rospy.Time.now()
        deltaS = now.secs - self._starttime.secs
        if deltaS > self.timeoutInS:
            raise TimeoutException( self.timeoutInS )
