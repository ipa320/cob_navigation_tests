#!/usr/bin/env python
import roslib
roslib.load_manifest( 'gazebo_gt_tf_publisher' )

import time
import rospy, rostopic, tf
from gazebo_msgs.msg import ModelStates


class TfPublisher:
    def __init__( self, modelName, topicName ):
        self._modelName = modelName
        self._topicName = topicName
        self._registerSubscriber()
        self._initBroadcaster()

    def _registerSubscriber( self ):
        self._subscriber = rospy.Subscriber( '/gazebo/model_states',
                ModelStates, self._callback )

    def _initBroadcaster( self ):
        self._broadcaster = tf.TransformBroadcaster()

    def shutdown( self ):
        self._subscriber.unregister()

    def _broadcast( self, x, y, theta ):
        try:
            self._broadcaster.sendTransform( (x, y, 0 ),
                    tf.transformations.quaternion_from_euler( 0, 0, theta ),
                    rospy.Time.now(), self._topicName, 'map' )
        except rospy.exceptions.ROSException, e:
            rospy.logwarn( 'Could not send transformation: %s' % e )


    def _callback( self, data ):
        if not self._modelName in data.name:
            return
        index    = data.name.index( self._modelName )
        pose     = data.pose[ index ]
        position = pose.position
        orient   = pose.orientation
        euler    = tf.transformations.euler_from_quaternion(
                ( orient.x, orient.y, orient.z, orient.w ))
        self._broadcast( position.x, position.y, euler[ 2 ])

if __name__ == '__main__':
    rospy.init_node( 'gazebo_gt_tf_publisher' )
    modelName = rospy.get_param( '~modelName' )
    topicName = rospy.get_param( '~topicName' )

    tfPublisher = TfPublisher( modelName, topicName )
    rospy.loginfo( 'Gazebo-TF: ModelName: %s, TopicName: %s' % 
            ( modelName, topicName ))

    rospy.spin()
    rospy.loginfo( 'Shutting down gazebo_gt_tf_publisher' )
    tfPublisher.shutdown()
