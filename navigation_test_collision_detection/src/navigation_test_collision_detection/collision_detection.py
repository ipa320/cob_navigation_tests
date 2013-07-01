#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_collision_detection' )
import rospy
import datetime, sys
from gazebo_msgs.msg            import ContactsState
from navigation_test_helper.msg import Collision

class CollisionDetector:
    def __init__( self, bumperTopicName, publisherTopicName ):
        self._bumperTopicName    = bumperTopicName
        self._publisherTopicName = publisherTopicName
        self._collisionActive    = False
        self._collisionsNum      = 0
        self._timeLastCollision  = None
    
    def start( self ):
        rospy.loginfo( 'Starting collision detection' )
        self._setupBumperSubscriber()
        self._setupCollisionPublisher()

    def _setupBumperSubscriber( self ):
        self._subscriber = rospy.Subscriber( self._bumperTopicName,
                ContactsState, self._contactsStateCallback )

    def _setupCollisionPublisher( self ):
        self._publisher = rospy.Publisher( self._publisherTopicName,
                Collision )

    def _contactsStateCallback( self, msg ):
        hasCollision = self._msgContainsCollision( msg )
        if hasCollision and not self._collisionActive:
            self._possibleCollisionDetected()
        if not hasCollision and self._collisionActive:
            self._collisionResolved()

    def _msgContainsCollision( self, msg ):
        return len( msg.states ) > 0

    def _possibleCollisionDetected( self ):
        self._collisionActive   = True
        if self._lastCollisionLessThan1sAgo():
            rospy.loginfo( 'Ignoring collision, last collision less than 1s ago' )
        else:
            self._realCollisionDetected()

        self._timeLastCollision = datetime.datetime.now()

    def _realCollisionDetected( self ):
        rospy.loginfo( 'New collision detected' )
        self._collisionsNum += 1
        self._publishCollision()

    def _publishCollision( self ):
        self._publisher.publish( self._collisionsNum )

    def _collisionResolved( self ):
        rospy.loginfo( 'Object resolved collision' )
        self._collisionActive = False

    def _lastCollisionLessThan1sAgo( self ):
        return self._secondsSinceLastCollision() < 1

    def _secondsSinceLastCollision( self ):
        if not self._timeLastCollision:
            return sys.maxint
        delta = datetime.datetime.now() - self._timeLastCollision
        return delta.seconds

if __name__ == '__main__':
    rospy.init_node( 'collision_detection' )
    bumperTopicName    = rospy.get_param( '~bumperTopic' )
    collisionTopicName = rospy.get_param( '~collisionPublisherTopic' )

    detector  = CollisionDetector( bumperTopicName, collisionTopicName )
    detector.start()
    rospy.spin()
