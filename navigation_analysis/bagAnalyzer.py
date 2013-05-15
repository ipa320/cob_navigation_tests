import roslib
roslib.load_manifest( 'navigation_test' )
import rospy, os, re, subprocess, sys
import navigation_test.msg
from threading import Thread
from gazeboHelper.metricsObserverTF import MetricsObserverTF
from jsonFileHandler import JsonFileHandler

class BagDirectoryReader( object ):
    def __init__( self, directory ):
        self._directory = directory

    def getBagFiles( self ):
        bagFiles = []
        for dirname, dirnames, filenames in os.walk( self._directory ):
            for filename in filenames:
                if re.match( '.*\.bag$', filename ):
                    bagFiles.append( filename )
        return bagFiles


class BagReplayer( object ):
    def __init__( self, filepath ):
        self._filepath = filepath

    def play( self ):
        print 'Playing %s' % self._filepath
        p = subprocess.call([ 'rosbag', 'play', self._filepath ])

class BagAnalyzer( object ):
    def __init__( self, resultWriter, filename ):
        print 'Initializing Analyzer'
        self._filename = filename
        self._metricsObserver = MetricsObserverTF()
        self._metricsObserver.dT = 0
        self._duration = 'N/A'
        self._resultWriter = resultWriter
        self._active = False
        self.setupStatusListener()

    def setupStatusListener( self ):
        print 'Listening to /navigation_test/status'
        rospy.Subscriber( '/navigation_test/status', navigation_test.msg.Status,
                self._callback )

    def start( self ):
        print 'Starting Analyzer'
        self._active = True
        self._metricsObserver.start()
        self._startTime = None

    def stop( self ):
        print 'Stopping MetricsObserver'
        self._active = False
        self._metricsObserver.stop()
        self._saveMetricsData()

    def _saveMetricsData( self ):
        data = self._metricsObserver.serialize()
        data[ 'duration' ] = self._duration
        data[ 'filename' ] = self._filename
        self._resultWriter.write( data )

    def shutdown( self ):
        self.stop()
        rospy.signal_shutdown( 'finished' )

    def _callback( self, msg ):
        if not self._active: return
        self._startTime = msg.start

        if msg.info == 'finished':
            self._duration = ( msg.header.stamp - self._startTime ).to_sec()
            self.shutdown()
            return

        sys.stdout.write( 'Going to Waypoint #%s, X: %s, Y: %s, Theta: %s\n' % 
            ( msg.waypointId, msg.waypointX, msg.waypointY, msg.waypointTheta ))
        sys.stdout.flush()


rospy.init_node( 'navigation_test_analyzer' )
path = os.path.dirname(os.path.abspath(__file__))
testResultHandler = JsonFileHandler( path + '/analyzedMetrics.json' )

bagDir = '/share/uhr-se/bag_record'
filesAnalyzed = map( lambda f: f[ 'filename' ], testResultHandler.read() )

print 'Reading %s' % bagDir
directoryReader = BagDirectoryReader( bagDir )
for bagFile in directoryReader.getBagFiles():
    if bagFile in filesAnalyzed: continue
    analyzer = BagAnalyzer( testResultHandler, bagFile )
    analyzer.start()
    player = BagReplayer( bagDir + '/' + bagFile )
    player.play()

print 'All files analyzed'
