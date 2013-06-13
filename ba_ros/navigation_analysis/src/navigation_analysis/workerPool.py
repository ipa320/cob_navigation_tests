#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_analysis' )
import rospy
import os, re, subprocess, socket
from navigation_helper.git import Git
from navigation_helper.jsonFileHandler import JsonFileHandler
from navigation_helper.resultRepository import ResultRepository
from worker import Worker

class BagDirectoryReader( object ):
    def __init__( self, directory, repository ):
        self._directory     = directory
        self._repository    = repository
        self._usedFilenames = []

    def getBagFilenames( self ):
        bagFiles = []
        for dirname, dirnames, filenames in os.walk( self._directory ):
            for filename in filenames:
                if re.match( '.*\.bag$', filename ):
                    yield filename

    def hasUnanalyzedBagFilenames( self ):
        return self._nextUnanalyedBagFilename( silent=True ) != None

    def nextUnanalyzedBagFilename( self ):
        return self._nextUnanalyedBagFilename( silent=False )

    def _nextUnanalyedBagFilename( self, silent ):
        for bagFilename in self.getBagFilenames():
            fileUsed     = bagFilename in self._usedFilenames
            fileAnalyzed = bagFilename in self.getAllBagFilenamesAnalyzed()
            if fileUsed or fileAnalyzed:
                continue
            
            if not silent:
                self._usedFilenames.append( bagFilename )

            return bagFilename
        return None


    def getAllBagFilenamesAnalyzed( self ):
        resultRepository = ResultRepository( self._repository )
        return resultRepository.allFilenamesAnalyzed()





class WorkerPool( object ):
    def __init__( self, repositoryName, deleteOnError ):
        self._s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._lastPort       = 11310
        self._repositoryName = repositoryName
        self._deleteOnError  = deleteOnError

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
        env = os.environ.copy()
        env[ 'ROS_MASTER_URI' ] = 'http://localhost:%s' % newPort
        args = [
            'roslaunch',
            'navigation_analysis',
            'analyse_bag_file.launch',
            'filepath:=%s'      % filepath,
            'repository:=%s'    % self._repositoryName,
            'deleteOnError:=%s' % self._deleteOnError
        ]
        print args
        p = subprocess.Popen( args, env=env )
        p.wait()



if __name__ == '__main__':
    rospy.init_node( 'analyze_remaining_bag_files' )
    bagDir         = rospy.get_param( '~bagDir' )
    repositoryName = rospy.get_param( '~repository' )
    deleteOnError  = rospy.get_param( '~deleteOnError' )

    print 'Reading %s' % bagDir
    path = os.path.dirname(os.path.abspath(__file__))

    git = Git( repositoryName )
    pool = WorkerPool( repositoryName, deleteOnError )

    with git as repository:
        directoryReader = BagDirectoryReader( bagDir, repository )
        while directoryReader.hasUnanalyzedBagFilenames():
            bagFilename = directoryReader.nextUnanalyzedBagFilename()
            bagFilepath = bagDir + '/' + bagFilename
            if os.path.isfile( bagFilepath + Worker.FIX_SUFFIX ):
                print 'Skipping %s since a fix exists' % bagFilename
                continue
            print 'Analyzing %s' % bagFilename
            pool.newInstance( bagFilepath )

    print 'All files analyzed, Saving.'
