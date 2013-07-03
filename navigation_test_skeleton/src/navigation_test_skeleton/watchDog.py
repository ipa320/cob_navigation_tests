import datetime

class TimeoutException( Exception ):
    def __init__( self, timeoutInS ):
        msg = 'Timeout %ss exceeded' % timeoutInS
        Exception.__init__( self, msg )

class WatchDog( object ):
    def __init__( self, timeoutInS ):
        self.timeoutInS = timeoutInS
        self._starttime  = datetime.datetime.now()

    def assertExecutionTimeLeft( self ):
        now   = datetime.datetime.now()
        delta = now - self._starttime
        if delta.seconds > self.timeoutInS:
            raise TimeoutException( self.timeoutInS )
