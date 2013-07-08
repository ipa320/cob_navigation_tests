#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_camera' )

import rospy
import tf
import time, threading
import gazebo_msgs.msg
from navigation_test_helper.positionResolver import PositionResolver
from navigation_test_helper.gazeboHelper import ModelStateSetter

class CameraUpdater( threading.Thread ):
    def __init__( self, updateRate, zOffset ):
        threading.Thread.__init__( self )
        self._active     = True
        self._updateRate = updateRate
        self._zOffset    = zOffset

    def run( self ):
        positionResolver = PositionResolver()
        modelStateSetter = ModelStateSetter()
        while self._active and not rospy.is_shutdown():
            position = positionResolver.getPosition()
            modelStateSetter.set( 'camera_model', position, z=self._zOffset )
            time.sleep( self._updateRate )

    def stop( self ):
        self._active = False

if __name__ == '__main__':
    rospy.init_node( 'camera_position_updater' )
    zOffset    = rospy.get_param( '~zOffset' )
    updateRate = float( rospy.get_param( '~updateRate' ))
    updater    = CameraUpdater( updateRate, zOffset )

    updater.start()
    rospy.spin()
    updater.stop()
