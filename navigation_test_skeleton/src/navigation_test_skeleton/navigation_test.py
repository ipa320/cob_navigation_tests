#!/usr/bin/env python
import roslib, math
roslib.load_manifest( 'navigation_test_skeleton' )
import rospy, rostopic
import os, logging, sys
import cob_srvs.srv, time
import unittest, rostest
import std_srvs, std_srvs.srv, std_msgs, threading
from navigationStatusPublisher                import NavigationStatusPublisher
from navigation_test_helper.positionResolver  import PositionResolver
from navigation_test_helper.metricsObserverTF import MetricsObserverTF
from navigation_test_helper.tolerance         import Tolerance
from navigation_test_helper.position          import Position
from navigation_test_helper.navigator         import Navigator


class TestNavigation( unittest.TestCase ):
    def setUp( self ):
        rospy.loginfo( 'Setting navigator' )
        self.navigator = Navigator( '/move_base' )
        self._metricsObserver = MetricsObserverTF()

        setting = self._getSetting()
        self._navigationStatusPublisher = NavigationStatusPublisher( 
                '/navigation_test/status', setting )

        self.tolerance = Tolerance( xy=0.2, theta=.3 )
        self.positionResolver = PositionResolver()

        rospy.loginfo( 'Waiting for robot to be ready' )
        robotReadyLock = self._waitForRobotToBeReady()
        robotReadyLock.acquire()

        rospy.loginfo( 'Waiting for Bag Recorder' )
        self._stopBagRecording = self._waitForBagRecorder()


    def _getSetting( self ):
        return {
            'scenario':   rospy.get_param( '~name' ),
            'robot':      rospy.get_param( '~robot' ),
            'navigation': rospy.get_param( '~navigation' ),
            'repository': rospy.get_param( '~repository' )
        }

    def _waitForRobotToBeReady( self ):
        self._robotReadyLock = threading.Lock()
        subscriber = rospy.Subscriber( '/navigation_test/robot_ready', 
                std_msgs.msg.String, self._callbackRobotReady )
        self._robotReadyLock.acquire()
        return self._robotReadyLock

    def _callbackRobotReady( self, msg ):
        rospy.loginfo( 'Robot ready. Releasing lock' )
        self._robotReadyLock.release()

    def _waitForBagRecorder( self ):
        rospy.wait_for_service( '/logger/stop' )

        stopBagRecordingService  = rospy.ServiceProxy( '/logger/stop',  
                cob_srvs.srv.Trigger )
        rospy.loginfo( 'Logger ready' )
        return stopBagRecordingService


    def testNavigate( self ):
        goals = rospy.get_param( '~goals' )
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
        
        self._stopBagRecording()
        self._waitForBagRecorderShutdown()

        rospy.signal_shutdown( 'finished' )
        time.sleep( 4 )

    def _waitForBagRecorderShutdown( self ):
        rospy.loginfo("waiting for logger to be able to shutdown")
        rospy.wait_for_service( '/logger/shutdown' )
        shutdownService = rospy.ServiceProxy( '/logger/shutdown',
                cob_srvs.srv.Trigger )
        shutdownService()
        rospy.loginfo("found.")



if __name__ == '__main__':
    rospy.init_node( 'navigation_test_schalal' )
    rostest.rosrun( 'navgation_test', 'test_navigation',
        TestNavigation, sys.argv)
