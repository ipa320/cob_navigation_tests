#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import threading, subprocess, sys
import navigation_test_helper.msg

def importImageView():
    from multiImageView import ImageViewApp

class CameraDisplayManager( object ):
    def __init__( self ):
        self._startedCameraDisplays = {}
        self._app = None

    def start( self ):
        self._statusSubscriber = rospy.Subscriber( 'status', 
            navigation_test_helper.msg.Status, self._statusCallback )

    def _statusCallback( self, msg ):
        if msg.setting.cameraTopics:
            print 'Starting MultiImageView on topics: %s' % msg.setting.cameraTopics
            self._app = ImageViewApp( msg.setting.cameraTopics )
            self._app.start()
            self._statusSubscriber.unregister()

    def stop( self ):
        sys.exit( 0 )


if __name__ == '__main__':
    try:
        importImageView()
        rospy.init_node( 'display_cameras' )
        manager = CameraDisplayManager()
        manager.start()
        rospy.spin()
        manager.stop()
    except ImportError,e:
        print 'Could not launch MultiImageView'
        print e
