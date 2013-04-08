#!/usr/bin/env python
import roslib, math
roslib.load_manifest( 'navigation_test' )
import rospy, rostopic
import os, logging, sys
import cob_srvs.srv, time
import unittest, rostest
from navigationStatusPublisher import NavigationStatusPublisher
from gazeboHelper.positionResolver import PositionResolver
from gazeboHelper.metricsObserverTF import MetricsObserverTF
from gazeboHelper.tolerance import Tolerance
from gazeboHelper.position import Position
from gazeboHelper.navigator import Navigator
from jsonFileWriter import JsonFileWriter

class TestNavigation( unittest.TestCase ):
    def setUp( self ):
        self.navigator = Navigator( '/move_base' )
        self._metricsObserver = MetricsObserverTF()
        self._navigationStatusPublisher = NavigationStatusPublisher( '~status' )
        self.tolerance = Tolerance( xy=0.2, theta=.3 )
        self.positionResolver = PositionResolver()
        path = os.path.dirname(os.path.abspath(__file__))
        self.testResultWriter = JsonFileWriter( path + '/metrics.json' )

        self._startBagRecording, self._stopBagRecording = \
            self._waitForBagRecorder()
        self._startBagRecording()
        time.sleep( 4 )

    def _waitForBagRecorder( self ):
        rospy.wait_for_service( '/logger/start' )
        rospy.wait_for_service( '/logger/stop' )

        startBagRecordingService = rospy.ServiceProxy( '/logger/start', 
                cob_srvs.srv.Trigger )
        stopBagRecordingService  = rospy.ServiceProxy( '/logger/stop',  
                cob_srvs.srv.Trigger )
        print 'Logger ready'
        return ( startBagRecordingService, stopBagRecordingService )


    def testNavigate( self ):
        goals = rospy.get_param( '/navigation_test/goals' )
        self._metricsObserver.start()

        i = 0
        for goal in goals:
            self._navigationStatusPublisher.nextWaypoint( goal )
            targetPosition = Position( *goal )

            self.navigator.goTo( targetPosition ) 
            self.navigator.waitForResult( timeout=300.0 )

            errorMsg = 'Position: %s does not match goal %s' % ( 
                    self.positionResolver.getPosition(), goal )
            self.assertTrue( self.positionResolver.inPosition( targetPosition, 
                    self.tolerance ), errorMsg )

            i += 1

        self._navigationStatusPublisher.finished()
        self._metricsObserver.stop()
        self.testResultWriter.write( self._metricsObserver.serialize() )
        
        self._stopBagRecording()
        time.sleep( 4 )

if __name__ == '__main__':
    rospy.init_node( 'navigation_test', anonymous=True)
    rostest.rosrun( 'navgation_test', 'test_navigation',
        TestNavigation, sys.argv)
