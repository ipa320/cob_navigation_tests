from metricsContainer import MetricsContainer
from threading import Thread, Lock
from positionResolver import PositionResolver
import rospy, tf, time

class MetricsObserverTF( Thread ): 
    def __init__( self ):
        Thread.__init__( self )
        self.dT = 0.005
        self._alive = True

        self._lock = Lock()
        self._metricsContainer = MetricsContainer()

    def start( self ):
        self._metricsContainer.start()
        Thread.start( self )

    def stop( self ):
        print 'Trying to stop MetricsObserverTf...'
        self._metricsContainer.stop()
        with self._lock:
            print '...Alive set to false'
            self._alive = False

    def isAlive( self ):
        with self._lock:
            return self._alive

    def run( self ):
        positionResolver = PositionResolver()
        while self.isAlive() and not rospy.is_shutdown():
            # initialize the position resolver but be careful to abort this
            # procedure if the user is requesting to stop the thread
            while self.isAlive() and not positionResolver.isInitialized():
                positionResolver.initialize( 5 )

            try: 
                position = positionResolver.getPosition()
                self._metricsContainer.update( position )
                time.sleep( self.dT )
            except tf.Exception, e:
                print 'Could not get position'
                print e
                if not rospy.is_shutdown():
                    rospy.sleep( self.dT/2 )
            except rospy.exceptions.ROSInterruptException:
                self._alive = False
                break
        print 'MetricsObserverTF finished.'

    def serialize( self ):
        return self._metricsContainer.serialize()

    def __str__( self ):
        return '<MetricsObserverTF %s>' % self._metricsContainer
