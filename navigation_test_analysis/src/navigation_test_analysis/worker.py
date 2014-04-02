#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy, os, re, subprocess, sys, time, datetime, traceback
import navigation_test_helper.msg
import subprocess, threading
from navigation_test_helper.metricsObserverTF import MetricsObserverTF
from navigation_test_helper.tfDiffObserver    import TFDiffObserver
from navigation_test_helper.tfPointsObserver  import TFPointsObserver
from navigation_test_helper.jsonFileHandler   import JsonFileHandler
from navigation_test_helper.git               import Git
from navigation_test_helper.bagInfo           import BagInfo
from rosbagPatcher.rosbagPatcher              import BagFilePatcher
from std_srvs.srv                             import Empty
import rospy.service


class Worker( object ):
    def __init__( self, bagInfo ):
        self.bagInfo = bagInfo
        self._analyzer = None

    def start( self, speed=1 ):
        filename = self.bagInfo.filename
        self._analyzer = BagAnalyzer( filename )
        self._analyzer.start()
        player   = BagReplayer( self.bagInfo.filepath )
        try:
            player.play( speed )
            self._analyzer.stop()
            print '"%s" analyzed' % self.bagInfo.filepath
            data = self._analyzer.serialize()
            self.saveResults( data )
            self.bagInfo.setAnalyzed()
            self._stopScreenRecorder()

        except BagAnalyzer.NoStatusReceivedError:
            print "except BagAnalyzer.NoStatusReceivedError"
            self._terminateScreenRecorderAndMetricsObserver()
            self._errorOccured( 'No status topic received.' )
        except BagAnalyzer.NoFinishedStatusReceivedError:
            print "except BagAnalyzer.NoFinishedStatusReceivedError"
            self._terminateScreenRecorderAndMetricsObserver()
            self._errorOccured( 'No finished status topic received.' )

        except BagAnalyzer.NoRepositoryNameReceivedError:
            print "except BagAnalyzer.NoRepositoryNameReceivedError"
            self._terminateScreenRecorderAndMetricsObserver()
            self._errorOccured( 'No Repository name received.' )

        except BagReplayer.TCPROSHeaderError:
            print "except BagReplayer.TCPROSHeaderError"
            self._terminateScreenRecorderAndMetricsObserver()
            if not self.bagInfo.isFixed():
                self._fixBagFileTCPROSHeader()
            else:
                self._errorOccured( 'Bag-File corrupted: TCPROS-Header-Error' )

        except BagReplayer.INDEX_DATA_Expected:
            print "except BagReplayer.INDEX_DATA_Expected"
            self._terminateScreenRecorderAndMetricsObserver()
            if not self.bagInfo.isFixed():
                self._reindexBagFile()
            else:
                self._errorOccured( 'Bag-File corrupted: Bagfile index. \n' + \
                        'Running rosbag reindex might fix the problem' )

        except Exception,e:
            self._terminateScreenRecorderAndMetricsObserver()
            self._errorOccured( 'Unexpected error occured: %s' % e )


    def _terminateScreenRecorderAndMetricsObserver( self ):
        if not self._analyzer: return
        try:
            self._analyzer.stop()
        except Exception,e:
            traceback.print_stack()
            print 'Could not stop the analyzer, an unexpected error occured:'
            print e


        try:
            print 'Terminating video converter'
            s = rospy.ServiceProxy( 'screenRecorder/terminate', Empty )
            s()
        except rospy.service.ServiceException, e:
            print 'Terminate Service could not be called: %s' % str( e )


    def _stopScreenRecorder( self ):
        try:
            print 'Stopping video converter'
            s = rospy.ServiceProxy( 'screenRecorder/stop', Empty )
            s()
        except rospy.service.ServiceException, e:
            print 'Stop Service could not be called: %s' % str( e )

    def _fixBagFileTCPROSHeader( self ):
        print
        print 'BAG-FILE TCPROS-HEADER-ERROR OCCURED. TRYING TO RECOVER'
        print '-------------------------------------------------------'
        patcher = BagFilePatcher( self.bagInfo.filepath )
        patcher.patch()
        self.bagInfo.setFixed()
        
    def _reindexBagFile( self ):
        print
        print 'BAG-FILE INDEX-DATA-ERROR OCCURED. TRYING TO RECOVER'
        print '----------------------------------------------------'
        args = [ 'rosbag', 'reindex', self.bagInfo.filepath ]
        print 'Running %s.\nThis could take a minute\n\n' % args
        try:
            subprocess.call( args )
            self.bagInfo.setFixed()
        except Exception, e:
            print 'Could not reindex bag file'
            set.bagInfo.setErroneous()

    def _errorOccured( self, msg ):
        self.bagInfo.setErroneous()
        print 'ERROR: %s' % msg
        print 'Bag-File: %s' % self.bagInfo.filepath

    def saveResults( self, data ):
        filename       = self.bagInfo.rawFilename
        repositoryName = self._getRepositoryNameFromData( data )
        subdirectories = ( data[ 'navigation' ], data[ 'robot' ], data[ 'scenario' ] )

        with Git( repositoryName )  as r:
            path = r.mkdir( subdirectories )
            filepath = '%s/result_%s.json' % ( path, filename )
            resultWriter = JsonFileHandler( filepath )
            resultWriter.write( data )

            r.commitAllChanges( 'Date: %s, Bag File %s' % (
                data[ 'localtimeFormatted' ], filename ))
            r.pullAndPush()

    def _getRepositoryNameFromData( self, data ):
        repositoryName = data[ 'repository' ]
        if not repositoryName:
            raise BagAnalyzer.NoRepositoryNameReceivedError( 
                    'Repository is not valid: %s' % data )
        return repositoryName


class BagReplayer( object ):
    class TCPROSHeaderError( Exception ): pass
    class INDEX_DATA_Expected( Exception ): pass

    def __init__( self, filepath ):
        self._filepath = filepath

    def play( self, speed=1 ):
        self._assertFileExists()
        print 'Playing %s' % self._filepath
        pipe = subprocess.PIPE
        args = [ 'rosbag', 'play', self._filepath, '-r', str( speed )]
        p    = subprocess.Popen( args, stderr=pipe )
        stdout, stderr = p.communicate()
        print stderr

        if stderr.find( 'invalid TCPROS header' ) >= 0:
            raise BagReplayer.TCPROSHeaderError()

        if stderr.find( 'Expected INDEX_DATA record' ) >= 0:
            raise BagReplayer.INDEX_DATA_Expected()

    def _assertFileExists( self ):
        if not os.path.isfile( self._filepath ):
            raise IOError( 'File %s does not exist' % self._filepath )



class BagAnalyzer( object ):
    class NoStatusReceivedError( Exception ): pass
    class NoRepositoryNameReceivedError( Exception ): pass
    class NoFinishedStatusReceivedError( Exception ): pass

    def __init__( self, filename ):
        print 'Initializing Analyzer'
        self._filename                = filename
        self._metricsObserver         = MetricsObserverTF()
        self._tfDiffObserver          = TFDiffObserver(
                '/gazebo_gt', '/base_link' )
        self._tfObserver          = TFDiffObserver(
                '/gazebo_gt', '/base_link' )
        self._tfPointsObserver        = TFPointsObserver(
                [ '/gazebo_gt', '/base_link' ], dt=2 )
        self._metricsObserver.dT      = 0
        self._duration                = 'N/A'
        self._active                  = False
        self._setting                 = {}
        self._expectedNextWaypointId  = 0
        self._finishedStatusReceived  = False
        self._error                   = ''
        self._subscribers             = []
        self._collisions              = 0
        self._collisionsTopic         = None
        self._startedCameras          = {}
        self.setupStatusListener()

    def setupStatusListener( self ):
        print 'Listening to /navigation_test/status'
        self._subscribers.append( rospy.Subscriber(
                'status', 
                navigation_test_helper.msg.Status,
                self._statusCallback ))

    def _setupCollisionsListener( self ):
        topic = self._setting[ 'collisionsTopic' ]
        if not topic or topic  == self._collisionsTopic:
            return

        print 'Listening to collisions on "%s"' % topic
        self._subscribers.append( rospy.Subscriber( topic,
            navigation_test_helper.msg.Collision,
            self._collisionCallback ))
        self._collisionsTopic = topic


    def start( self ):
        print 'Starting Analyzer'
        self._active = True
        self._metricsObserver.start()
        self._tfDiffObserver.start()
        self._startTime = None
        self._localtime = None

    def stop( self ):
        print 'Stopping MetricsObserver'
        if self._active:
            self._active = False
            self._unregisterSubscribers()
            self._metricsObserver.stop()
            self._tfDiffObserver.stop()

    def _unregisterSubscribers( self ):
        for subscriber in self._subscribers:
            subscriber.unregister()

    def serialize( self ):
        self._assertNoUnrecoverableErrorOccured()
        data = self._metricsObserver.serialize()
        data[ 'error'              ] = self._error
        data[ 'duration'           ] = self._duration
        data[ 'filename'           ] = self._filename
        data[ 'localtime'          ] = self._localtime
        data[ 'collisions'         ] = self._collisions
        data[ 'localtimeFormatted' ] = self._localtimeFormatted()
        data[ 'deltas'             ] = self._tfDiffObserver.serialize()
        data = dict( data.items() + self._setting.items() )
        return data

    def _assertNoUnrecoverableErrorOccured( self ):
        if not self._startTime:
            raise BagAnalyzer.NoStatusReceivedError()
        if not self._finishedStatusReceived:
            raise BagAnalyzer.NoFinishedStatusReceivedError()

    def _localtimeFormatted( self ):
        print 'Localtime: %s' % self._localtime
        d = datetime.datetime.fromtimestamp( self._localtime )
        return d.strftime( '%Y-%m-%d' )

    def _collisionCallback( self, msg ):
        self._collisions += 1

    def _statusCallback( self, msg ):
        if not self._active: return

        self._startTime                    = msg.starttime
        self._localtime                    = msg.localtime
        self._setting[ 'robot' ]           = msg.setting.robot
        self._setting[ 'navigation' ]      = msg.setting.navigation
        self._setting[ 'scenario' ]        = msg.setting.scenario
        self._setting[ 'repository' ]      = msg.setting.repository
        self._setting[ 'collisionsTopic' ] = msg.setting.collisionsTopic

        self._setupCollisionsListener()
    
        # first error wins
        if msg.error and not self._error:
            self._error = msg.error

        if msg.info == 'finished':
            self._finishedStatusReceived = True
            self._duration = ( msg.header.stamp - self._startTime ).to_sec()
            self.stop()
            return

        elif msg.info == 'running':
            if not msg.waypointId == self._expectedNextWaypointId:
                print( 'Expected next waypoint id to be %s but was %s' % (
                    self._expectedNextWaypointId, msg.waypointId ))
            self._expectedNextWaypointId = msg.waypointId + 1
            self._logNextWaypoint( msg )



    def _logNextWaypoint( self, msg ):
        sys.stdout.write( 'Going to Waypoint #%s, X: %s, Y: %s, Theta: %s\n' % 
            ( msg.waypointId, msg.waypointX, msg.waypointY, msg.waypointTheta ))
        sys.stdout.write( 'Robot: %s, Navigation: %s, Scenario: %s\n' % ( self._setting[ 'robot' ],
                self._setting[ 'navigation' ], self._setting[ 'scenario' ]))
        sys.stdout.flush()



if __name__ == '__main__':
    rospy.init_node( 'analyse_worker', anonymous=True )
    filepath = rospy.get_param( '~filepath' )
    speed    = rospy.get_param( '~speed' )
    worker = Worker( BagInfo( filepath ))
    worker.start( speed=speed )
    print 'Worker finished, all threads closed'
    print threading._active
