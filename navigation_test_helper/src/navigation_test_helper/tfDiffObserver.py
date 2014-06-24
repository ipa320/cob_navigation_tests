import roslib
roslib.load_manifest( 'navigation_test_helper' )

import rospy, tf
from threading import Thread, RLock
import time

import numpy, math

class TFDiffObserver( Thread ):
    def __init__( self, topicNameA, topicNameB, numPoints=300 ):
        Thread.__init__( self )
        self._topicNameA = topicNameA
        self._topicNameB = topicNameB
        self._tfListener = None
        self._initialized = None
        self._lock = RLock()
        self._active = True
        self._dT = 0.01
        self._deltas = []
        self._numPoints = numPoints

    def initialize( self, timeout=None ):
        if not timeout:
            while self.isActive() and not self.isInitialized():
                self._initializeOnce( 5 )
        else:
            self._initializeOnce( timeout )


    def isInitialized( self ):
        with self._lock:
            return self._initialized

    def _initializeOnce( self, timeout=5.0 ):
        with self._lock:
            if self.isInitialized(): return True
            if not self._tfListener:
                self._tfListener = tf.TransformListener() # <- TF listenter is initialized here
            try:
                self._tfListener.waitForTransform( self._topicNameA,
                        self._topicNameB, rospy.Time( 0 ),
                        rospy.Duration( timeout )) # <- TF listenter waits here
                self._initialized = True
                return True
            except tf.Exception,e:
                print 'TFDiffObserver: Could not get transformation from %s to %s within timeout %s' % (
                        self._topicNameA, self._topicNameB, timeout )
                return False
            except Exception,e:
                print 'TFDiffObserver: Exception occured: %s' % e
                return False

    def run( self ):
        self.initialize()
        while self.isActive():
            timestamp = rospy.Time.now().to_sec()
            dPos, dQuat = self._tfListener.lookupTransform(
                self._topicNameA, self._topicNameB, rospy.Time( 0 )) # <- TF listenter is setup here
            self._storeDelta( timestamp, dPos, dQuat )
            time.sleep( self._dT )
        self._thinPoints()

    def _thinPoints( self ):
        factor = int( len( self._deltas ) / self._numPoints )
        self._deltas = self._deltas[ ::factor ]

    def _storeDelta( self, timestamp, dPos, dQuat ):
        dEuler = tf.transformations.euler_from_quaternion( dQuat )
        self._deltas.append( ( timestamp, dPos[ 0 ], dPos[ 1 ], dEuler[ 2 ]))


    def isActive( self ):
        with self._lock:
            return not rospy.is_shutdown() and self._active

    def stop( self ):
        with self._lock:
            self._active = False

    def serialize( self ):
        return self._deltas[:]
