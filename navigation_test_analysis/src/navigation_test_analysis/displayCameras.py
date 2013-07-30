#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import threading, subprocess
import navigation_test_helper.msg

class CameraDisplay( threading.Thread ):
    def __init__( self, topic ):
        threading.Thread.__init__( self )
        self._topic = topic
        self._p     = None

    def start( self ):
        cmd  = 'rosrun image_view image_view image:=%s/image_raw' % self._topic
        print 'Starting Camera "%s" with:\n > %s' % ( self._topic, cmd )
        args = cmd.split( ' ' )
        self._p = subprocess.Popen( args )

    def stop( self ):
        if not self._p: return
        self._p.terminate()


class CameraDisplayManager( object ):
    def __init__( self ):
        self._startedCameraDisplays = {}

    def start( self ):
        self._statusSubscriber = rospy.Subscriber( 'status', 
            navigation_test_helper.msg.Status, self._statusCallback )

    def _statusCallback( self, msg ):
        for cameraTopic in msg.setting.cameraTopics:
            if cameraTopic in self._startedCameraDisplays: continue
            display = CameraDisplay( cameraTopic )
            display.start()
            self._startedCameraDisplays[ cameraTopic ] = display

    def stop( self ):
        for topic, display in self._startedCameraDisplays.items():
            display.stop()


if __name__ == '__main__':
    rospy.init_node( 'display_cameras' )
    manager = CameraDisplayManager()
    manager.start()
    rospy.spin()
    manager.stop()
