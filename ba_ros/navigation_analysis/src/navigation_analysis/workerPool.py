#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_analysis' )
import rospy
import os, re, subprocess, socket
from navigation_helper.git              import Git
from navigation_helper.jsonFileHandler  import JsonFileHandler
from navigation_helper.resultRepository import ResultRepository
from navigation_helper.bagInfo          import BagInfo
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

    def newInstance( self, bagInfo ):
        newPort = self.findNextAvailablePort()
        env = os.environ.copy()
        env[ 'ROS_MASTER_URI' ] = 'http://localhost:%s' % newPort
        args = [
            'roslaunch',
            'navigation_analysis',
            'analyse_bag_file.launch',
            'filepath:=%s'      % bagInfo.filepath
        ]
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

if __name__ == '__main__':
    rospy.init_node( 'analyze_remaining_bag_files' )
    bagDir = rospy.get_param( '~bagDir' )

    print 'Reading %s' % bagDir
    path = os.path.dirname(os.path.abspath(__file__))

    pool = WorkerPool()

    directoryReader = BagDirectoryReader( bagDir )
    while directoryReader.hasUnanalyzedBagFilenames():
        bagInfo = directoryReader.nextUnanalyzedBagFilename()
        printInfoMessage( bagInfo )
        pool.newInstance( bagInfo )

    print 'All files analyzed, Saving.'
