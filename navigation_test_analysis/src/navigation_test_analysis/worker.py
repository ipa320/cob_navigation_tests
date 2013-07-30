#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy, os, re, subprocess, sys, time, datetime
import navigation_test_helper.msg
import subprocess, threading
from navigation_test_helper.metricsObserverTF import MetricsObserverTF
from navigation_test_helper.jsonFileHandler   import JsonFileHandler
from navigation_test_helper.git               import Git
from navigation_test_helper.bagInfo           import BagInfo
from rosbagPatcher.rosbagPatcher import BagFilePatcher


class Worker( object ):
    def __init__( self, bagInfo ):
        self.bagInfo = bagInfo

    def start( self ):
        filename = self.bagInfo.filename
        analyzer = BagAnalyzer( filename )
        analyzer.start()
        player = BagReplayer( self.bagInfo.filepath )
        try:
            player.play()
            analyzer.stop()
            print '"%s" analyzed' % self.bagInfo.filepath
            data = analyzer.serialize()
            self.saveResults( data )
            self.bagInfo.setAnalyzed()


        except BagAnalyzer.NoStatusReceivedError:
            self._errorOccured( 'No status topic received.' )

        except BagAnalyzer.NoFinishedStatusReceivedError:
            self._errorOccured( 'No finished status topic received.' )

        except BagAnalyzer.NoRepositoryNameReceivedError:
            self._errorOccured( 'No Repository name received.' )

        except subprocess.CalledProcessError,e:
            if not self.bagInfo.isFixed():
                self._fixBagFile()
            else:
                self._errorOccured( 'Bag-File corrupted' )

        finally:
            analyzer.stop()

    def _fixBagFile( self ):
        print
        print 'BAG-FILE ERROR OCCURED. TRYING TO RECOVER'
        print '-----------------------------------------'
        patcher = BagFilePatcher( self.bagInfo.filepath )
        patcher.patch()
        self.bagInfo.setFixed()
        

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
    def __init__( self, filepath ):
        self._filepath = filepath

    def play( self ):
        self._assertFileExists()
        print 'Playing %s' % self._filepath
        p = subprocess.check_call([ 'rosbag', 'play', self._filepath ])

    def _assertFileExists( self ):
        if not os.path.isfile( self._filepath ):
            raise IOError( 'File %s does not exist' % self._filepath )


class CameraDisplayer( threading.Thread ):
    def __init__( self, topic ):
        threading.Thread.__init__( self )
        self._topic = topic

    def start( self ):
        cmd  = 'rosrun image_view image_view image:=%s/image_raw' % self._topic
        print 'Running: %s' % cmd
        args = cmd.split( ' ' )
        p = subprocess.Popen( args )

class BagAnalyzer( object ):
    class NoStatusReceivedError( Exception ): pass
    class NoRepositoryNameReceivedError( Exception ): pass
    class NoFinishedStatusReceivedError( Exception ): pass

    def __init__( self, filename ):
        print 'Initializing Analyzer'
        self._filename                = filename
        self._metricsObserver         = MetricsObserverTF()
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
                '/status', 
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


    def _displayCameraTopics( self ):
        for cameraTopic in self._setting[ 'cameraTopics' ]:
            if cameraTopic in self._startedCameras: continue
            print 'Starting Camera "%s"' % cameraTopic
            display = CameraDisplayer( cameraTopic )
            display.start()
            self._startedCameras[ cameraTopic ] = display



    def start( self ):
        print 'Starting Analyzer'
        self._active = True
        self._metricsObserver.start()
        self._startTime = None
        self._localtime = None

    def stop( self ):
        print 'Stopping MetricsObserver'
        if self._active:
            self._active = False
            self._unregisterSubscribers()
            self._metricsObserver.stop()

    def _unregisterSubscribers( self ):
        for subscriber in self._subscribers:
            subscriber.unregister()

    def serialize( self ):
        self._assertNoUnrecoverableErrorOccured()
        data = self._metricsObserver.serialize()
        data[ 'error'      ] = self._error
        data[ 'duration'   ] = self._duration
        data[ 'filename'   ] = self._filename
        data[ 'localtime'  ] = self._localtime
        data[ 'collisions' ] = self._collisions
        data[ 'localtimeFormatted' ] = self._localtimeFormatted()
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
        self._setting[ 'cameraTopics' ]    = msg.setting.cameraTopics

        self._setupCollisionsListener()
        self._displayCameraTopics()
    
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
                raise Exception( 'Expected next waypoint id to be %s but was %s' % (
                    self._expectedNextWaypointId, msg.waypointId ))
            self._expectedNextWaypointId += 1
            self._logNextWaypoint( msg )



    def _logNextWapoint( self, msg ):
        sys.stdout.write( 'Going to Waypoint #%s, X: %s, Y: %s, Theta: %s\n' % 
            ( msg.waypointId, msg.waypointX, msg.waypointY, msg.waypointTheta ))
        sys.stdout.write( 'Robot: %s, Navigation: %s, Scenario: %s\n' % ( self._setting[ 'robot' ],
                self._setting[ 'navigation' ], self._setting[ 'scenario' ]))
        sys.stdout.flush()



if __name__ == '__main__':
    rospy.init_node( 'analyse_worker', anonymous=True )
    filepath = rospy.get_param( '~filepath' )
    worker = Worker( BagInfo( filepath ))
    worker.start()
