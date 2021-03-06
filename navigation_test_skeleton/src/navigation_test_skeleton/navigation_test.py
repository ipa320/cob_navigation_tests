#!/usr/bin/env python
import roslib, math
roslib.load_manifest( 'navigation_test_skeleton' )
import rospy, rostopic
import os, logging, sys
import cob_srvs.srv, time
import unittest, rostest
import std_srvs, std_srvs.srv, std_msgs
from watchDog                                 import WatchDog, TimeoutException
from navigationStatusPublisher                import NavigationStatusPublisher
from navigation_test_helper.positionResolver  import PositionResolver
from navigation_test_helper.positionResolver  import PositionMissedException
from navigation_test_helper.metricsObserverTF import MetricsObserverTF
from navigation_test_helper.tolerance         import Tolerance
from navigation_test_helper.position          import Position
from navigation_test_helper.navigator         import Navigator
from navigation_test_helper.navigator         import NavigationFailedException
from navigation_test_helper.srv               import SetupRobotService


class TestNavigation( unittest.TestCase ):
    def _initialize( self ):
        rospy.loginfo( 'Setting navigator' )

        moveBaseAction = rospy.get_param( 'moveBaseAction' )
        self.navigator = Navigator( moveBaseAction )
        self._metricsObserver = MetricsObserverTF()

        setting = self._getSetting()
        self._navigationStatusPublisher = NavigationStatusPublisher( 
                'status', setting )

        rospy.loginfo( 'Initializing Position Resolver' )
        self.tolerance = Tolerance( xy=0.3, theta=.3 )
        self.positionResolver = PositionResolver()
        self.positionResolver.initialize()

        rospy.loginfo( 'Waiting for Bag Recorder' )
        self._stopBagRecording = self._waitForBagRecorder()
        self._navigationStatusPublisher.starting()

        rospy.loginfo( 'Waiting for robot to be ready' )
        self._setupRobotWhenReady()

        rospy.loginfo( 'Starting actual test' )
        self._setupWatchdog()



    def _getSetting( self ):
        return {
            'scenario':        rospy.get_param( '~scenarioName' ),
            'robot':           rospy.get_param( '~robot' ),
            'navigation':      rospy.get_param( '~navigation' ),
            'repository':      rospy.get_param( 'repository' ),
            'cameraTopics':    rospy.get_param( 'cameraTopics' ),
            'collisionsTopic': rospy.get_param( 'collisionsTopic' )
        }

    def getParamOptional( self, key, default=None ):
        try:
            return rospy.get_param( key )
        except KeyError, e:
            return default

    def _setupWatchdog( self ):
        timeoutInS     = rospy.get_param( 'timeoutInS' )
        self._watchDog = WatchDog( timeoutInS )

    def _setupRobotWhenReady( self ):
        setupRobotServiceName = self.getParamOptional( 'setupRobotService' )
        if not setupRobotServiceName:
            rospy.loginfo( 'No setup robot service set. Assuming it\'s ready' )
            return

        rospy.loginfo( 'Waiting on setup service %s' % setupRobotServiceName )
        rospy.wait_for_service( setupRobotServiceName, timeout=120 )
        setupRobotService = rospy.ServiceProxy( setupRobotServiceName,
                SetupRobotService )
        result = setupRobotService()
        if not result.success:
            raise Exception( 'Setup Robot Service failed: %s' % result.msg )


    def _waitForBagRecorder( self ):
        rospy.wait_for_service( 'logger/stop', timeout=120 )

        stopBagRecordingService  = rospy.ServiceProxy( 'logger/stop',  
                cob_srvs.srv.Trigger )
        rospy.loginfo( 'Logger ready' )
        return stopBagRecordingService


    def testNavigate( self ):
        self._initialize()
        self._metricsObserver.start()

        goals            = rospy.get_param( 'route' )
        positionResolver = self.positionResolver
        tolerance        = self.tolerance
        failureMsg       = ''

        try:
            i = 0
            for goal in goals:
                rospy.loginfo( "Moving to %s" % goal )
                self._navigationStatusPublisher.nextWaypoint( goal )
                targetPosition = Position( *goal )

                resultWaiter = self.navigator.goTo( targetPosition ) 
                while not resultWaiter.hasFinished():
                    self._watchDog.assertExecutionTimeLeft()
                    time.sleep( 1 )

                resultWaiter.assertSucceeded()
                positionResolver.assertInPosition( targetPosition, tolerance )

                rospy.loginfo( "The current goal was reached" )
                i += 1
        
        except PositionMissedException, e:
            failureMsg = "The navigation missed the target. Exiting."
            self._navigationStatusPublisher.missed()

        except NavigationFailedException, e:
            errorCode = e.errorCode
            failureMsg = "The navigation failed with errorCode: %s. Exiting." % errorCode
            self._navigationStatusPublisher.failed( errorCode )

        except TimeoutException, e:
            timeout = self._watchDog.timeoutInS
            failureMsg = "The test timed out after %ss" % timeout
            self._navigationStatusPublisher.timedout()

        finally:
            self._terminate()

        if failureMsg:
            self.fail( failureMsg )

    def _terminate( self ):
        self._navigationStatusPublisher.finished()
        self._metricsObserver.stop()
        
        self._stopBagRecording()
        self._waitForBagRecorderShutdown()

        rospy.signal_shutdown( 'finished' )
        time.sleep( 4 )

    def _waitForBagRecorderShutdown( self ):
        rospy.loginfo("waiting for logger to be able to shutdown")
        rospy.wait_for_service( 'logger/shutdown' )
        shutdownService = rospy.ServiceProxy( 'logger/shutdown',
                cob_srvs.srv.Trigger )
        shutdownService()
        rospy.loginfo("found.")



if __name__ == '__main__':
    rospy.init_node( 'navigation_test_schalal' )
    rostest.rosrun( 'navgation_test', 'test_navigation',
        TestNavigation, sys.argv)
