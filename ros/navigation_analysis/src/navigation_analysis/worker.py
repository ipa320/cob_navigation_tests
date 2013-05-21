#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_analysis' )
import rospy, os, re, subprocess, sys, time, datetime
import navigation_helper.gazeboHelper, navigation_helper.msg
from threading import Thread
from navigation_helper.metricsObserverTF import MetricsObserverTF
from navigation_helper.jsonFileHandler   import JsonFileHandler
from git import Git
import subprocess

class Worker( object ):
    def __init__( self, bagFilepath, repository ):
        self._repository  = repository
        self._bagFilepath = bagFilepath

    def start( self ):
        filename = os.path.basename( self._bagFilepath )
        analyzer = BagAnalyzer( filename )
        analyzer.start()
        player = BagReplayer( self._bagFilepath )
        player.play() 
        print '"%s" analyzed' % self._bagFilepath
        data = analyzer.serialize()

        self.saveResults( data )


    def saveResults( self, data ):
        filename = os.path.basename( self._bagFilepath )
        subdirectories = ( data[ 'navigation' ], data[ 'robot' ], data[ 'scenario' ] )
        path = self._repository.mkdir( subdirectories )

        filepath = '%s/result_%s.json' % ( path, filename )
        resultWriter = JsonFileHandler( filepath )
        resultWriter.write( data )

        self._repository.commitAllChanges( 'Date: %s, Bag File %s' % (
            data[ 'localtimeFormatted' ], filename ))
        self._repository.pullAndPush()

class BagReplayer( object ):
    def __init__( self, filepath ):
        self._filepath = filepath

    def play( self ):
        print 'Playing %s' % self._filepath
        p = subprocess.call([ 'rosbag', 'play', self._filepath ])

class BagAnalyzer( object ):
    def __init__( self, filename ):
        print 'Initializing Analyzer'
        self._filename               = filename
        self._metricsObserver        = MetricsObserverTF()
        self._metricsObserver.dT     = 0
        self._duration               = 'N/A'
        self._active                 = False
        self._setting                = {}
        self._expectedNextWaypointId = 0
        self.setupStatusListener()

    def setupStatusListener( self ):
        print 'Listening to /navigation_test/status'
        self._statusSubscriber = rospy.Subscriber( '/navigation_test/status', 
                navigation_helper.msg.Status, self._callback )
        print self._statusSubscriber

    def start( self ):
        print 'Starting Analyzer'
        self._active = True
        self._metricsObserver.start()
        self._startTime = None
        self._localtime = None

    def stop( self ):
        print 'Stopping MetricsObserver'
        self._active = False
        self._statusSubscriber.unregister()
        self._metricsObserver.stop()

    def serialize( self ):
        data = self._metricsObserver.serialize()
        data[ 'duration'  ] = self._duration
        data[ 'filename'  ] = self._filename
        data[ 'localtime' ] = self._localtime
        data[ 'localtimeFormatted' ] = self._localtimeFormatted()
        data = dict( data.items() + self._setting.items() )
        return data

    def _localtimeFormatted( self ):
        print 'Localtime: %s' % self._localtime
        d = datetime.datetime.fromtimestamp( self._localtime )
        return d.strftime( '%Y-%m-%d' )

    def _callback( self, msg ):
        if not self._active: return

        if not self._startTime:
            self._startTime               = msg.header.stamp
            self._localtime               = msg.localtime
            self._setting[ 'robot' ]      = msg.setting.robot
            self._setting[ 'navigation' ] = msg.setting.navigation
            self._setting[ 'scenario' ]   = msg.setting.scenario
        

        if msg.info == 'finished':
            self._duration = ( msg.header.stamp - self._startTime ).to_sec()
            self.stop()
            return

        elif not msg.waypointId == self._expectedNextWaypointId:
            raise Exception( 'Expected next waypoint id to be %s but was %s' % (
                self._expectedNextWaypointId, msg.waypointId ))
        self._expectedNextWaypointId += 1

        sys.stdout.write( 'Going to Waypoint #%s, X: %s, Y: %s, Theta: %s\n' % 
            ( msg.waypointId, msg.waypointX, msg.waypointY, msg.waypointTheta ))
        sys.stdout.write( 'Robot: %s, Navigation: %s, Scenario: %s\n' % ( self._setting[ 'robot' ],
                self._setting[ 'navigation' ], self._setting[ 'scenario' ]))
        sys.stdout.flush()



if __name__ == '__main__':
    rospy.init_node( 'analyse_worker', anonymous=True )
    filepath       = rospy.get_param( '~filepath' )
    repositoryName = rospy.get_param( '~repository' )

    git = Git( repositoryName )
    with git as repository:
        worker = Worker( filepath, repository )
        worker.start()
