import roslib
roslib.load_manifest( 'navigation_test_helper' )

import rospy, tf
from threading import Thread, RLock
import time, copy

class TFPointsObserver( Thread ):
    def __init__( self, topicNames, baseTopic='/map', numPoints=100 ):
        Thread.__init__( self )
        self._topicNames  = topicNames
        self._baseTopic   = baseTopic
        self._tfListener  = None
        self._initialized = False
        self._lock        = RLock()
        self._active      = True
        self._dT          = 0.1
        self._values      = {}
        self._numPoints   = numPoints

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
            topicName = 'n/a'
            try:
                self._tfListeners = []
                if not self._tfListener:
                    self._tfListener = tf.TransformListener()
                for topicName in self._topicNames:
                    self._tfListener.waitForTransform( self._baseTopic,
                            topicName, rospy.Time( 0 ),
                            rospy.Duration( timeout ))
                self._initialized = True
                return True
            except tf.Exception,e:
                print 'TFPointsObserver: Could not get transformation from %s to %s within timeout %s' % ( self._baseTopic, topicName, timeout )
                return False
            except Exception,e:
                print 'TFPointsObserver: Exception occured: %s' % e
                return False

    def run( self ):
        self.initialize()
        while self.isActive():
            for topicName in self._topicNames:
                timestamp   = rospy.Time.now().to_sec()
                dPos, dQuat = self._tfListener.lookupTransform(
                    self._baseTopic, topicName, rospy.Time( 0 ))
                self._storeValue( topicName, timestamp, dPos, dQuat )
                time.sleep( self._dT )
        self._thinPoints()

    def _storeValue( self, topicName, timestamp, dPos, dQuat ):
        dEuler = tf.transformations.euler_from_quaternion( dQuat )
        if not topicName in self._values:
            self._values[ topicName ] = []
        self._values[ topicName ].append( ( timestamp, dPos[ 0 ], dPos[ 1 ],
            dEuler[ 2 ]))

    def _thinPoints( self ):
        for topicName, points in self._values.items():
            factor = int( len( points ) / self._numPoints )
            self._values[ topicName ] = points[ ::factor ]

    def isActive( self ):
        with self._lock:
            return not rospy.is_shutdown() and self._active

    def stop( self ):
        with self._lock:
            self._active = False

    def serialize( self ):
        return copy.copy( self._values )
