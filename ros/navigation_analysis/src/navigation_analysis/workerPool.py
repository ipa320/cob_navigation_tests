#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_analysis' )
import rospy
import os, re, subprocess, socket
from git import Git
from navigation_helper.jsonFileHandler import JsonFileHandler

class BagDirectoryReader( object ):
    def __init__( self, directory, repository ):
        self._directory  = directory
        self._repository = repository

    def getBagFilenames( self ):
        bagFiles = []
        for dirname, dirnames, filenames in os.walk( self._directory ):
            for filename in filenames:
                if re.match( '.*\.bag$', filename ):
                    bagFiles.append( filename )
        return bagFiles

    def getUnanalyzedBagFilenames( self ):
        bagFilenames = self.getBagFilenames()
        bagFilenamesAnalyzed = self.getAllBagFilenamesAnalyzed()
        for bagFilename in bagFilenames:
            if not bagFilename in bagFilenamesAnalyzed:
                yield bagFilename

    def getAllBagFilenamesAnalyzed( self ):
        allFilenamesAnalyzed = []
        for dirname, filename in self._repository.walk():
            if not filename.startswith( 'result' ) or not filename.endswith( '.json' ):
                continue
            testResultHandler = JsonFileHandler( dirname + '/' + filename )
            nextFilename = map( lambda f: f[ 'filename' ], testResultHandler.read() )
            allFilenamesAnalyzed += nextFilename
        return allFilenamesAnalyzed





class WorkerPool( object ):
    def __init__( self, repositoryName ):
        self._s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._lastPort       = 11310
        self._repositoryName = repositoryName

    def findNextAvailablePort( self ):
        try:
            while True:
                self._lastPort += 1
                self._s.connect(( '127.0.0.1', self._lastPort ))
                self._s.close()
        except socket.error as e:
            pass

        return self._lastPort

    def newInstance( self, filepath ):
        newPort = self.findNextAvailablePort()
        args = [
            'roslaunch',
            '-p', str( newPort ),
            'navigation_analysis',
            'analyse_bag_file.launch',
            'filepath:=%s'   % filepath,
            'repository:=%s' % self._repositoryName
        ]
        print args
        subprocess.call( args )



if __name__ == '__main__':
    rospy.init_node( 'analyze_remaining_bag_files' )
    bagDir         = rospy.get_param( '~bagDir' )
    repositoryName = rospy.get_param( '~repository' )

    print 'Reading %s' % bagDir
    path = os.path.dirname(os.path.abspath(__file__))

    git = Git( repositoryName )
    pool = WorkerPool( repositoryName )

    with git as repository:
        directoryReader = BagDirectoryReader( bagDir, repository )
        for bagFilename in directoryReader.getUnanalyzedBagFilenames():
            print 'now analyzing %s' % bagFilename
            bagFilepath = bagDir + '/' + bagFilename
            pool.newInstance( bagFilepath )


        #repository.push()


    print 'All files analyzed, Saving.'
