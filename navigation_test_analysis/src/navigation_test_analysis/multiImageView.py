#!/usr/bin/env python

import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy
from sensor_msgs.msg import Image
from navigation_test_helper import gtkHelper
 
import wx, sys, threading, math, yaml
import cv_bridge, cv, cv2
 
class ImageViewApp( wx.App ):
    def __init__( self, topics ):
        self.topics      = topics
        self.panels      = []
        self.subscribers = []
        wx.App.__init__( self )

    def OnInit( self ):
        wx.App.__init__( self )
        self.size = gtkHelper.getFullscreenSize()
        self.frame = CloseFrame( title = "ROS Image View", size=self.size )
        self.frame.addCloseCallback( self.onClose )
        self.createPanels()
        self.frame.Show(True)
        return True

    def createPanels( self ):
        topicsCount = len( self.topics )
        if topicsCount == 1:
            return self.createSinglePanel()
        if topicsCount == 2:
            return self.createTwoPanels()

        size = int( math.ceil( math.sqrt( topicsCount )))
        return self.createMultiplePanels( size, size )
    
    def createSinglePanel( self ):
        self.panels = [ ImageViewPanel( self.frame )]

    def createTwoPanels( self ):
        return self.createMultiplePanels( 1, 2 )

    def createMultiplePanels( self, rows, cols ):
        widthPerPanel  = self.size[ 0 ] / cols
        heightPerPanel = self.size[ 1 ] / rows
        size           = [ widthPerPanel, heightPerPanel ]
        for y in xrange( rows ):
            for x in xrange( cols ):
                pos   = [ x*widthPerPanel, y*heightPerPanel ]
                panel = ImageViewPanel( self.frame, pos=pos, size=size )
                self.panels.append( panel )

    def onClose( self ):
        for subscriber in self.subscribers:
            subscriber.unregister()
        sys.exit( 1 )

    def start( self ):
        for i in xrange( len( self.topics )):
            topic      = self.topics[ i ]
            panel      = self.panels[ i ]
            cb         = self.make_handle_image_cb( panel )
            subscriber = rospy.Subscriber( topic, Image, cb )
            self.subscribers.append( subscriber )
        self.MainLoop()


    def make_handle_image_cb( self, panel ):
        return lambda image: self.handle_image( panel, image )

    def handle_image( self, panel, image ):
        # make sure we update in the UI thread
        wx.CallAfter( panel.update, image )
        # http://wiki.wxpython.org/LongRunningTasks


class CloseFrame( wx.Frame ):
    def __init__( self, title, size ):
        wx.Frame.__init__( self, None, title=title, size=size )
        self._callbacks = []
        self.initUI()

    def addCloseCallback( self, cb ):
        self._callbacks.append( cb )

    def initUI( self ):
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

    def onCloseWindow( self, event ):
        for cb in self._callbacks:
            cb()
        self.Destroy()
 
class ImageViewPanel(wx.Panel):
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        self.bridge      = cv_bridge.CvBridge()


    """ class ImageViewPanel creates a panel with an image on it, inherits wx.Panel """
    def update(self, image):
        # http://www.ros.org/doc/api/sensor_msgs/html/msg/Image.html
        if not hasattr(self, 'staticbmp'):
            self.staticbmp = wx.StaticBitmap(self)
            frame = self.GetParent()
            frame.SetSize((image.width, image.height))
        if image.encoding == 'rgba8':
            bmp = wx.BitmapFromBufferRGBA(image.width, image.height, image.data)
            self.staticbmp.SetBitmap(bmp)
        elif image.encoding == 'rgb8':
            bmp = wx.BitmapFromBuffer(image.width, image.height, image.data)
            self.staticbmp.SetBitmap(bmp)
        elif image.encoding == 'bgr8':
            cvImage = self.bridge.imgmsg_to_cv( image, 'rgb8' )
            bmp = wx.BitmapFromBuffer(image.width, image.height, cvImage.tostring() )
            self.staticbmp.SetBitmap(bmp)

 
#def handle_image(image):
    ## make sure we update in the UI thread
    #wx.CallAfter(wx.GetApp().panel.update, image)
    ## http://wiki.wxpython.org/LongRunningTasks
 
def main(argv):
    rospy.init_node('ImageView')
    topics = yaml.load( rospy.get_param( '~cameraTopics' ))
    app    = ImageViewApp( topics )
    app.start()
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv))
