#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import subprocess, threading, os, tempfile, os.path
from subprocess             import PIPE
from navigation_test_helper import copyHandlers
from navigation_test_helper import gtkHelper
from videoEncoder           import RecorderSettings
from std_srvs.srv           import Empty
import videoEncoder

class ScreenRecorder( threading.Thread ):
    def __init__( self, settings ):
        threading.Thread.__init__( self )
        self._settings       = settings
        self._p              = None
        self.tmpPath         = tempfile.mkdtemp()

        bagFilename = os.path.basename( settings.bagFilepath )
        self.mkvAbsolutePath = '%s/%s.mkv' % ( self.tmpPath, bagFilename )
        self.mp4AbsolutePath = '%s/%s.mp4' % ( self.tmpPath, bagFilename )

        self._setupCopyHandler()

    def run( self ):
        cmd     = self._startCmd()
        self._p = subprocess.Popen( cmd )
        self._p.wait()

    def stop( self ):
        if not self._p: return
        print 'Terminating video process'
        self._p.terminate()
        print 'Converting video to mp4'
        self._convert()
        print 'Copying files'
        self._copyFiles()
        self._remove()
        print 'Finished converting video'

    def _convert( self ):
        cmd = self._convertCmd()
        p   = subprocess.Popen( cmd )
        p.wait()
        #os.remove( '%s.mkv' % self._settings.absolutePath )

    def _startCmd( self ): 
        cmd = videoEncoder.recordToMkvFileCommand( self.mkvAbsolutePath, 
                self._settings )
        print 'Recording to %s' % self.mkvAbsolutePath
        print 'Command %s' % cmd
        return cmd.split( ' ' )

    def _convertCmd( self ):
        cmd = videoEncoder.encodeToMp4Command( self.mkvAbsolutePath,
                self.mp4AbsolutePath )
        return cmd.split( ' ' )

    def _setupCopyHandler( self ):
        uri = self._settings.targetUri
        self._copyHandler = copyHandlers.getByUri( uri )
        self._copyHandler.assertWritable()

    def _copyFiles( self ):
        self._copyHandler.copyFile( self.mp4AbsolutePath )

    def _remove( self ):
        os.unlink( self.mkvAbsolutePath )
        os.unlink( self.mp4AbsolutePath )
        os.rmdir( self.tmpPath )

def getParam( key, default=None ):
    try:
        return rospy.get_param( key )
    except KeyError, e:
        if not default: raise e
        return default

if __name__=='__main__':
    videoEncoder.assertInstalled()

    rospy.init_node( 'screen_recorder' )
    settings  = RecorderSettings()
    settings.bagFilepath = getParam( '~bagFilepath' )
    settings.size        = getParam( '~size', gtkHelper.getFullscreenSize() )
    settings.frequency   = getParam( '~frequency' )
    settings.offset      = getParam( '~offset' )
    settings.targetUri   = getParam( '~videoPath' )
    settings.display     = getParam( '~display', os.environ[ 'DISPLAY' ])

    screenRecorder = ScreenRecorder( settings )
    screenRecorder.start()
    stopCallback = lambda *args: screenRecorder.stop()
    rospy.Service( 'screenRecorder/stop', Empty, stopCallback )
    rospy.spin()
