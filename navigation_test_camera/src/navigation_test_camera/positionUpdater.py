#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_camera' )

import rospy
import tf
import time, threading, math
import gazebo_msgs.msg
from navigation_test_helper.positionResolver import PositionResolver
from navigation_test_helper.gazeboHelper import ModelStateSetter

class CameraUpdater( threading.Thread ):
    def __init__( self, updateRate, zOffset ):
        threading.Thread.__init__( self )
        self._alive      = True
        self._updateRate = updateRate
        self._zOffset    = zOffset

    def run( self ):
        positionResolver = PositionResolver()
        while self.isAlive() and not positionResolver.isInitialized():
            positionResolver.initialize( 5 )

        modelStateSetter = ModelStateSetter( 'camera_model' )
        while self.isAlive():
            position = positionResolver.getPosition()
            position.theta = 0
            modelStateSetter.set( position, z=self._zOffset, P=math.pi/2 )
            time.sleep( self._updateRate )

    def isAlive( self ):
        return self._alive and not rospy.is_shutdown()

    def stop( self ):
        self._alive = False

if __name__ == '__main__':
    rospy.init_node( 'camera_position_updater' )
    zOffset    = rospy.get_param( '~zOffset' )
    updateRate = float( rospy.get_param( '~updateRate' ))
    updater    = CameraUpdater( updateRate, zOffset )

    updater.start()
    rospy.spin()
    updater.stop()
