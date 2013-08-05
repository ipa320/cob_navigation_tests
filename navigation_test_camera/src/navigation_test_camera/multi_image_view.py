#!/usr/bin/env python

import roslib
roslib.load_manifest( 'navigation_test_camera' )
import rospy
from sensor_msgs.msg import Image
from proportional_splitter import ProportionalSplitter
from navigation_test_helper import gtkHelper
 
import wx, sys, threading
 
class ImageViewApp( wx.App ):
    def __init__( self, topics ):
        wx.App.__init__( self )
        self.topics      = topics
        self.subscribers = []

    def OnInit( self ):
        wx.App.__init__( self )
        size = gtkHelper.getFullscreenSize()
        self.frame = CloseFrame( title = "ROS Image View", size=size )
        self.frame.addCloseCallback( self.onClose )
        self.split1 = ProportionalSplitter( self.frame, proportion=0.5, size=size )
        self.panel1 = ImageViewPanel( self.split1 )
        self.panel2 = ImageViewPanel( self.split1 )
        self.split1.SplitVertically( self.panel1, self.panel2 )
        self.frame.Show(True)
        return True

    def onClose( self ):
        for subscriber in self.subscribers:
            subscriber.unregister()
        sys.exit( 1 )

    def start( self ):
        panels = [ self.panel1, self.panel2 ]
        for i in xrange( len( self.topics )):
            topic      = self.topics[ i ]
            panel      = panels[ i ]
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

 
#def handle_image(image):
    ## make sure we update in the UI thread
    #wx.CallAfter(wx.GetApp().panel.update, image)
    ## http://wiki.wxpython.org/LongRunningTasks
 
def main(argv):
    def handle_image( image ):
        wx.CallAfter( app.panel.update, image )

    rospy.init_node('ImageView')
    topics = [ '/stereo/right/image_raw', '/stereo/left/image_raw' ]
    app = ImageViewApp( topics )
    app.start()
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv))
