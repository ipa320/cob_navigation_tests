#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import subprocess, threading, os, gtk, tempfile
from subprocess import PIPE
from navigation_test_helper import copyHandlers

class RecorderSettings( object ):
    def __init__( self ):
        self.targetUri = ''
        self.display   = ':0'
        self.offset    = [ 0, 0 ]
        self.size      = [ 0, 0 ]
        self.frequency = 0

    def sizeToString( self ):
        return '%s:%s' % tuple( self.size )

    def offsetToString( self ):
        return '%s,%s' % tuple( self.offset )

class ScreenRecorder( threading.Thread ):
    def __init__( self, settings ):
        threading.Thread.__init__( self )
        self._settings       = settings
        self._p              = None
        self.tmpPath         = tempfile.mkdtemp()
        self.mkvAbsolutePath = self.tmpPath + '/video.mkv'
        self.mp4AbsolutePath = self.tmpPath + '/video.m4v'
        self._setupCopyHandler()

    def run( self ):
        cmd     = self._startCmd()
        self._p = subprocess.Popen( cmd, stdout=PIPE, stderr=PIPE )

    def stop( self ):
        if not self._p: return
        self._p.terminate()
        self._convert()
        self._copyFiles()
        self._remove()

    def _convert( self ):
        cmd = self._convertCmd()
        p   = subprocess.Popen( cmd )
        p.wait()
        #os.remove( '%s.mkv' % self._settings.absolutePath )

    def _startCmd( self ): 
        cmd  = 'avconv -f x11grab -s %s -r %s -i %s+%s %s' % (
                self._settings.sizeToString(),
                self._settings.frequency,
                self._settings.display,
                self._settings.offsetToString(),
                self.mkvAbsolutePath )
        print 'Recording to %s' % self.mkvAbsolutePath
        print 'Command %s' % cmd
        return cmd.split( ' ' )

    def _convertCmd( self ):
        cmd = 'avconv -i grab.mkv -c:v libx264 %s' % ( self.mkvAbsolutePath,
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

def getFullscreenSize():
    window = gtk.Window()
    screen = window.get_screen()
    return [ screen.get_width(), screen.get_height() ]


def getParam( key, default=None ):
    try:
        return rospy.get_param( key )
    except KeyError, e:
        if not default: raise e
        return default

def assertAvconvInstalled():
    try:
        args   = 'avconv --help'.split( ' ' )
        p      = subprocess.Popen( args, stdout=subprocess.PIPE )
        result = p.wait()
    except OSError, e:
        raise Exception( 'Avconv is not installed on your system' )

def assertCodecInstalled():
    args = 'avconv -codecs'.split(  ' ' )
    p    = subprocess.Popen( args, stdout=subprocess.PIPE )
    stdout, stderr = p.communicate()
    if not stdout.find( 'lix264' ):
        raise Exception( 'Codec libx264 not installed. You can try to install package "libavcodec-extra-53"' )


if __name__=='__main__':
    assertAvconvInstalled()
    assertCodecInstalled()

    rospy.init_node( 'screen_recorder' )
    settings  = RecorderSettings()
    settings.size      = getParam( '~size', getFullscreenSize() )
    settings.frequency = getParam( '~frequency' )
    settings.offset    = getParam( '~offset' )
    settings.targetUri = getParam( '~videoPath' )
    settings.display   = getParam( '~display', os.environ[ 'DISPLAY' ])

    screenRecorder = ScreenRecorder( settings )
    screenRecorder.start()
    rospy.spin()
    screenRecorder.stop()
