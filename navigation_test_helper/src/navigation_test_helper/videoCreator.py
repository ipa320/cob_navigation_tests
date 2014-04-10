#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
import navigation_test_helper.msg
from sensor_msgs.msg import Image

import os

    
class VideoCreator( object ):
    def __init__( self ):
        print '>> videoCreator init'
        rospy.Subscriber("/topCamera/image_raw", Image, self.callback)  
        self.r = rospy.Rate(1) #Hz
        self.timeout = 10 #s     
        self.waittime = self.timeout  
        
    def waitForPlayback( self ):
        print '>> videoCreator waiting for playback to end'
        while self.waittime > 0:
            print '>> videoCreator waiting ' + str(self.waittime)
            self.r.sleep()
            self.waittime = self.waittime - 1
            
    def createVideo( self, videopath ):
        print '>> videoCreator CREATING'
        os.system("cd /home/aub-ch/Public/; touch heLLo")
        #avconv -r 1 -i frame%06d.jpg -r 5 out_avconv.mp4     
            
    def waitForEnd( self ):
        print '>> videoCreator heLLo'
        
    def callback( self, data):
        self.waittime = self.timeout
    
#if __name__ == '__main__':
#    rospy.init_node( 'videoCreator', anonymous=True )
#    videofilepath = rospy.get_param( '~videofilepath' )
#    filepath = rospy.get_param( '~filepath' )
 #   speed    = rospy.get_param( '~speed' ) 
 #   
 #   vc = videoCreator() 
 ##   vc.waitForPlayback()
 #   vc.createVideo( videofilepath )
 #   vc.waitForEnd()
 #   print '>> videoCreator finished'
