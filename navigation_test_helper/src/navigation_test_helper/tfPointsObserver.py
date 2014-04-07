import roslib
roslib.load_manifest( 'navigation_test_helper' )

import rospy, tf
from threading import Thread, RLock
import time, copy

class TFPointsObserver( Thread ):
    def __init__( self, topicNames, baseTopic='/map', dT=2 ):
        Thread.__init__( self )
        self._topicNames  = topicNames
        self._baseTopic   = baseTopic
        self._tfListener  = None
        self._initialized = False
        self._lock        = RLock()
        self._active      = True
        self._dT          = dT
        self._values      = {}

    def initialize( self, timeout=None ):
        if not timeout:
            while not rospy.is_shutdown() and not self.isInitialized():
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
                self._tfListener = tf.TransformListener()
                for topicName in self._topicNames:
                    self._tfListener.waitForTransform( self._baseTopic,
                            topicName, rospy.Time( 0 ),
                            rospy.Duration( timeout ))
                self._initialized = True
                return True
            except tf.Exception,e:
                print 'Could not get transformation from %s to %s within timeout %s' % ( self._baseTopic, topicName, timeout )
                return False

    def run( self ):
        self.initialize()
        while not rospy.is_shutdown() and self.isActive():
            for topicName in self._topicNames:
                timestamp   = rospy.Time.now().to_sec()
                dPos, dQuat = self._tfListener.lookupTransform(
                    self._baseTopic, topicName, rospy.Time( 0 ))
                self._storeValue( topicName, timestamp, dPos, dQuat )
                time.sleep( self._dT )

    def _storeValue( self, topicName, timestamp, dPos, dQuat ):
        dEuler = tf.transformations.euler_from_quaternion( dQuat )
        if not topicName in self._values:
            self._values[ topicName ] = []
        self._values[ topicName ].append( ( timestamp, dPos[ 0 ], dPos[ 1 ],
            dEuler[ 2 ]))

    def isActive( self ):
        with self._lock:
            return self._active

    def stop( self ):
        with self._lock:
            self._active = False

    def serialize( self ):
        return copy.copy( self._values )
