#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_analysis' )
import rospy, rosbag
from rosbag.bag    import ROSBagFormatException
from genpy.message import DeserializationError
import sys, os, tempfile, shutil


class Message( object ):
    def __init__( self, time, msg, topic ):
        self.time  = time
        self.msg   = msg
        self.topic = topic

class BagReader( object ):
    def __init__( self, bag, time=None ):
        self._bag = bag
        self._time = time

    def read( self ):
        for topic, msg, time in self._bag.read_messages( start_time=self._time ):
            self._time = time
            yield Message( time=time, msg=msg, topic=topic )

    def positionInSeconds( self ):
        return self._time.to_sec()

    def getTimeIncrementedByNSeconds( self, delta ):
        sec = self._time.to_sec()
        return rospy.Time.from_sec( sec+delta )

class BagFilePatcher( object ):
    def __init__( self, sourceFilepath, destFilepath=None ):
        self._sourceFilepath = sourceFilepath
        self._destFilepath   = destFilepath
        self._sameSourceAndDestination = destFilepath is None
        if self._sameSourceAndDestination:
            self._destFilepath = tempfile.mktemp()

    def patch( self ):
        with rosbag.Bag( self._destFilepath, 'w' ) as destBag:
            with rosbag.Bag( self._sourceFilepath, 'r' ) as sourceBag:
                self._sourceBag = sourceBag
                self._destBag   = destBag
                self._reader    = BagReader( sourceBag )
                self._patchSourceBagFileToDestination()
        if self._sameSourceAndDestination: #replace old bagfile with new one
            os.remove( self._sourceFilepath )
            shutil.move( self._destFilepath, self._sourceFilepath )

    def _patchSourceBagFileToDestination( self ):
        finished = False
        while not finished:
            try:
                for msg in self._reader.read():
                    self._writeMessage( msg )
                finished = True
            except ( ROSBagFormatException, DeserializationError ) as e:
                self._tryToFixError( e )

    def _tryToFixError( self, e ):
        readerTimestamp = self._reader.positionInSeconds()
        print 'Possible Header field error detected at %s' % readerTimestamp
        self._skipDeltaSecondsInPlayback( delta=0.001 )

    def _writeMessage( self, msg ):
        self._destBag.write( msg.topic, msg.msg, msg.time )

    def _skipDeltaSecondsInPlayback( self, delta ):
        newTime = self._reader.getTimeIncrementedByNSeconds( delta )
        self._reader = BagReader( self._sourceBag, newTime )

def printUsageAndExit():
    print 'Usage [souce] [dest]'
    sys.exit( 1 )

if __name__ == '__main__':
    if not len( sys.argv ) == 3:
        printUsageAndExit()
    sourceFilename = sys.argv[ 1 ]
    destFilename   = sys.argv[ 2 ]
    if not os.path.isfile( sourceFilename ):
        printUsageAndExit()

    patcher = BagFilePatcher( sourceFilename, destFilename )
    patcher.patch()
    print 'Finished.'
