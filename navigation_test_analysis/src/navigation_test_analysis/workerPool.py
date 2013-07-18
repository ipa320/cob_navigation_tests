#!/usr/bin/env python
import roslib
PKG = 'navigation_test_analysis'
roslib.load_manifest( PKG )
import rospy
import os, re, subprocess, socket, time, threading
from navigation_test_helper.git              import Git
from navigation_test_helper.jsonFileHandler  import JsonFileHandler
from navigation_test_helper.resultRepository import ResultRepository
from navigation_test_helper.bagInfo          import BagInfo
from worker import Worker


class BagDirectoryReader( object ):
    def __init__( self, directory ):
        self._directory     = directory
        self._filesAnalyzed = []

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
    def __init__( self, bagPath, videoConfig ):
        threading.Thread.__init__( self )
        self._bagPath = bagPath
        self._active  = True
        self._additionalRosArguments = {
            'videoConfig':  videoConfig
        }

    def stop( self ):
        self._active = False

    def run( self ):
        print 'Starting analysis daemon on: %s' % self._bagPath
        directoryReader = BagDirectoryReader( bagPath )
        pool = WorkerPool()
        while self._active:
            if directoryReader.hasUnanalyzedBagFilenames():
                bagInfo = directoryReader.nextUnanalyzedBagFilename()
                printInfoMessage( bagInfo )
                pool.newInstance( bagInfo, self._additionalRosArguments )

            time.sleep( 3 )

if __name__ == '__main__':
    rospy.init_node( 'analyze_remaining_bag_files' )
    bagPath     = os.path.expanduser( rospy.get_param( '~bagPath' ))
    videoConfig = rospy.get_param( '~videoConfig' )
    daemon  = AnalyserDaemon( bagPath, videoConfig )
    daemon.start()
    rospy.spin()
    daemon.stop()
    print 'Stopping daemon, please wait'
