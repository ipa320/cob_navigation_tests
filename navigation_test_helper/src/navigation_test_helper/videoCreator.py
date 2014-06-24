#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import navigation_test_helper.msg
from sensor_msgs.msg import Image

import commands

    
class VideoCreator( object ):
    def __init__( self, videofilepath ):
        print '>> videoCreator: init' 
        self._videofilepath = videofilepath
        print '>> videoCreator: path: ' + self._videofilepath
        self.r = rospy.Rate(1) #Hz
        self.timeout = 10 #s     
        self.waittime = self.timeout  
        
    def createVideo( self, filename ):
        #filename = 'dateiname'
        print '>> videoCreator: CREATING'
        command = 'cd %s; avconv -r 1 -i frame%%06d.jpg -r 20 %s.mp4' % (self._videofilepath, filename)
        try:
            s=commands.getstatusoutput(command)
        except:
            print ">> videoCreator: Unexpected error: ", sys.exc_info()[0]
        print s[1]   
        print s[0]   

    def hasFrameFiles( self ):
        s=commands.getstatusoutput('cd %s; ls | grep "frame"' % self._videofilepath)
        if s[1] == '':
            print '>> videoCreator: videofolder empty (no frames*.jpg files)'
            return 0
        else:
            return 1
            
    def deleteFrameFiles( self ):
        s=commands.getstatusoutput('cd %s; rm frame*.jpg' % self._videofilepath)
        print '>> videoCreator: deleting frames'
        return s[0]
