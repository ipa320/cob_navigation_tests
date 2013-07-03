#!/usr/bin/env python
import roslib
roslib.load_manifest( 'navigation_test_collision_detection' )
import rospy
import datetime, sys
from gazebo_msgs.msg            import ContactsState
from navigation_test_helper.msg import Collision

class CollisionDetector:
    def __init__( self, bumperTopicName, collisionsTopicName, collisionMinInterval ):
        self._bumperTopicName      = bumperTopicName
        self._collisionsTopicName  = collisionsTopicName
        self._collisionActive      = False
        self._collisionsNum        = 0
        self._timeLastCollision    = None
        self._collisionMinInterval = int( collisionMinInterval )
    
    def start( self ):
        rospy.loginfo( 'Starting collision detection' )
        self._setupBumperSubscriber()
        self._setupCollisionPublisher()

    def _setupBumperSubscriber( self ):
        self._subscriber = rospy.Subscriber( self._bumperTopicName,
                ContactsState, self._contactsStateCallback )

    def _setupCollisionPublisher( self ):
        self._publisher = rospy.Publisher( self._collisionsTopicName,
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
        if self._collisionWithinInterval():
            msg = 'Ignoring collision, last collision less than %ss ago' % \
                    self._collisionMinInterval
            rospy.loginfo( msg )
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

    def _collisionWithinInterval( self ):
        return self._secondsSinceLastCollision() < self._collisionMinInterval

    def _secondsSinceLastCollision( self ):
        if not self._timeLastCollision:
            return sys.maxint
        delta = datetime.datetime.now() - self._timeLastCollision
        return delta.seconds

if __name__ == '__main__':
    rospy.init_node( 'collision_detection' )
    bumperTopicName      = rospy.get_param( '~bumperTopic' )
    collisionMinInterval = rospy.get_param( '~collisionMinInterval' )
    collisionsTopicName  = rospy.get_param( '~collisionsTopic' )

    detector  = CollisionDetector( bumperTopicName, collisionsTopicName,
            collisionMinInterval )
    detector.start()
    rospy.spin()
