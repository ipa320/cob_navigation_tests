#!/usr/bin/env python
import roslib
PKG = 'navigation_test_analysis'
roslib.load_manifest( PKG )
import rospy
import os, re, subprocess, socket, time, threading, os.path
from navigation_test_helper.git              import Git
from navigation_test_helper.jsonFileHandler  import JsonFileHandler
from navigation_test_helper.resultRepository import ResultRepository
from navigation_test_helper.bagInfo          import BagInfo
from worker import Worker
import videoEncoder


class BagDirectoryReader( object ):
    def __init__( self, directory ):
        self._directory     = directory
        self._filesAnalyzed = []

    def waitUntilBagfileSizeStable( self, bagInfo ):
        filepath = bagInfo.filepath
        filesize1, filesize2 = 0,1
        while filesize1 != filesize2:
            filesize1 = os.path.getsize( filepath )
            time.sleep( 2 )
            filesize2 = os.path.getsize( filepath )

    def getBagInfos( self ):
        bagFiles = []
        for dirname, dirnames, filenames in os.walk( self._directory ):
            for filename in filenames:
                if BagInfo.isBagFile( filename ):
                    filepath = "%s/%s" % ( self._directory, filename )
                    yield BagInfo( filepath )

    def hasUnanalyzedBagFilenames( self ):
        return self._nextUnanalyedBagFilename( silent=True ) != None

    def nextUnanalyzedBagFilename( self ):
        return self._nextUnanalyedBagFilename( silent=False )

    def _nextUnanalyedBagFilename( self, silent ):
        for bagInfo in self.getBagInfos():
            analyzedAlready = bagInfo.filepath in self._filesAnalyzed
            if analyzedAlready or bagInfo.isProcessed():
                continue

            try:
                self.waitUntilBagfileSizeStable( bagInfo )
            except OSError, e:
                self._filesAnalyzed.append( bagInfo.filepath )
                continue

            if not silent:
                self._filesAnalyzed.append( bagInfo.filepath )

            return bagInfo
        return None


    def getAllBagFilenamesAnalyzed( self ):
        resultRepository = ResultRepository( self._repository )
        return resultRepository.allFilenamesAnalyzed()





class WorkerPool( object ):
    def __init__( self ):
        self._s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._lastPort       = 11310

    def findNextAvailablePort( self ):
        try:
            while True:
                self._lastPort += 1
                self._s.connect(( '127.0.0.1', self._lastPort ))
                self._s.close()
        except socket.error as e:
            pass

        return self._lastPort

    def newInstance( self, bagInfo, additionalRosArguments ):
        newPort = self.findNextAvailablePort()
        env = os.environ.copy()
        env[ 'ROS_MASTER_URI' ] = 'http://localhost:%s' % newPort
        args = [
            'roslaunch',
            PKG, 'analyse_bag_file.launch',
            'filepath:=%s' % bagInfo.filepath
        ]
        for key, value in additionalRosArguments.items():
            args.append( '%s:=%s' % ( key, value ))

        print args
        p = subprocess.Popen( args, env=env )
        p.wait()



def printInfoMessage( bagInfo ):
    title = 'Analyzing next bag file'
    lineLength = max( len( bagInfo.filepath ), len( title )) + 2
    print ''
    print '-' * lineLength
    print ''
    print " %s" % title
    print " %s" % bagInfo.filepath
    print ''
    print '-' * lineLength
    print ''


class AnalyserDaemon( threading.Thread ):
    def __init__( self, bagPath, videoConfig, speed ):
        threading.Thread.__init__( self )
        self._bagPath = bagPath
        self._active  = True
        self._directoryReader = BagDirectoryReader( self._bagPath )
        self._additionalRosArguments = {
            'videoConfig':  videoConfig,
            'speed':        speed
        }

    def stop( self ):
        self._active = False

    def runUntilNoBagfileLeft( self ):
        self.start()
        print 'bagpath: %s' % self._bagPath
        while self._active:
            time.sleep( 5 )
            self._active = self._directoryReader.hasUnanalyzedBagFilenames()

    def run( self ):
        print 'Starting analysis daemon on: %s' % self._bagPath
        pool = WorkerPool()
        while self._active:
            if self._directoryReader.hasUnanalyzedBagFilenames():
                bagInfo = self._directoryReader.nextUnanalyzedBagFilename()
                printInfoMessage( bagInfo )
                pool.newInstance( bagInfo, self._additionalRosArguments )

            time.sleep( 3 )

if __name__ == '__main__':
    videoEncoder.assertInstalled()

    rospy.init_node( 'analyze_remaining_bag_files' )
    bagPath     = os.path.expanduser( rospy.get_param( '~bagPath' ))
    videoConfig = rospy.get_param( '~videoConfig' )
    speed       = rospy.get_param( '~speed' )
    keepalive   = rospy.get_param( '~keepalive' ) == 'true'
    daemon  = AnalyserDaemon( bagPath, videoConfig, speed )
    if keepalive:
        daemon.start()
        rospy.spin()
        daemon.stop()
    else:
        daemon.runUntilNoBagfileLeft()

    print 'Stopping daemon, please wait'
