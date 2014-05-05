#!/usr/bin/env python

#################################################################
##\file
#
# \note
# Copyright (c) 2013 \n
# Fraunhofer Institute for Manufacturing Engineering
# and Automation (IPA) \n\n
#
#################################################################
#
# \note
# Project name: Care-O-bot Research
# \note
# ROS package name: 
#
# \author
# Author: Thiago de Freitas Oliveira Araujo, 
# email:thiago.de.freitas.oliveira.araujo@ipa.fhg.de
# \author
# Supervised by: Florian Weisshardt, email:florian.weisshardt@ipa.fhg.de
#
# \date Date of creation: January 2013
#
# \brief
# This module records bagfile according to triggering events
#
#################################################################
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. \n
# - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. \n
# - Neither the name of the Fraunhofer Institute for Manufacturing
# Engineering and Automation (IPA) nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. \n
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License LGPL as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License LGPL for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License LGPL along with this program.
# If not, see < http://www.gnu.org/licenses/>.
#
#################################################################

import roslib
PKG = "navigation_test_skeleton"
roslib.load_manifest(PKG)
import rospy, rosbag, rostopic

import tf
import global_lock, record_topic

from tf.transformations     import euler_from_quaternion
from simple_script_server   import Trigger, TriggerResponse
from navigation_test_helper import copyHandlers
from navigation_test_helper.copyHandlers import CopyException
import math, uuid, re, tempfile, time, os, sys, itertools, yaml

class topics_bag():

    def __init__(self):
        self.loadParams()
        self.setupBagfileCopyHandler()
        self.openBagfile()
        
        while(rospy.rostime.get_time() == 0.0):
			time.sleep(0.1)

        # necessary tf elements 
        self.tfL     = tf.TransformListener()
        
        rospy.sleep(2)
        # waits for a tf transform before starting. This is important to check if
        # the system is fully functional.
        
        self.tfL.waitForTransform(
                self.wanted_tfs[0]["reference_frame"],
                self.wanted_tfs[0]["target_frame"],
                rospy.Time(0),
                rospy.Duration(10))
        
        # dictionaries for storing current translation and rotation for the specific
        # frames
        self.current_translation = {}
        self.current_rotation = {}
        
        for frame in self.wanted_tfs:
            self.current_translation[frame["target_frame"]] = [0,0,0]
            self.current_rotation[frame["target_frame"]] = [0,0,0,0]
            

        global_lock.active_bag = True

    def setupBagfileCopyHandler( self ):
        uri = self.bag_target_path
        self._bagfileCopyHandler = copyHandlers.getByUri( uri )
        self._bagfileCopyHandler.assertWritable()

    def close( self ):
        self.bag.close()
        try:
            self._bagfileCopyHandler.copyFile( self.bag_local_filepath )
            os.remove( self.bag_local_filepath )
        except CopyException,e:
            sys.stderr.write( 'An exception occured copying the file. The \
                    original bagfile can still be found in %s' % \
                    self.bag_local_filepath )
            raise e


    def loadParams( self ):
        # this defines the variables according to the ones specified at the yaml
        # file. The triggers, the wanted tfs, the wanted topics and where they are going
        # to be written, more specifically at the file named as self.bag.
        self.trigger_record_translation = self.getRequiredParam('~trigger_record_translation')
        self.trigger_record_rotation    = self.getRequiredParam('~trigger_record_rotation')
        self.trigger_timestep           = self.getRequiredParam('~trigger_timestep')
        self.wanted_tfs                 = self.getRequiredParam('~wanted_tfs')
        self.trigger_topics             = self.getRequiredParam("~trigger_topics")
        self.continuous_topics          = self.getRequiredParam("~continuous_topics")
        self.bag_target_path            = self.getRequiredParam("bagPath")
        self.bag_local_path             = tempfile.gettempdir()
        print ":) logging bag files to: %s" % tempfile.gettempdir()
        self.bag_filename               = '%s.bag' % uuid.uuid4()
        self.bag_local_filepath         = self.bag_local_path + '/' + self.bag_filename
        self.addCameraTopics()
        self.addCollisionsTopic()

    def addCameraTopics( self ):
        cameraTopicNames = self.getOptionalParam( 'cameraTopics' )
        if not cameraTopicNames:
            return

        for cameraTopicName in cameraTopicNames:
            self.continuous_topics.append({
                'topic':  cameraTopicName,
                'type':  'sensor_msgs/Image'
            })

    def addCollisionsTopic( self ):
        collisionsTopic = self.getOptionalParam( 'collisionsTopic' )
        if not collisionsTopic:
            return
        self.continuous_topics.append({
            'topic': collisionsTopic,
            'type':  'navigation_test_helper/Collision'
        })

    def getRequiredParam( self, key ):
        value = rospy.get_param( key )
        if value is None:
            raise Exception( 'Could not load paramter %s' % key )
        return value

    def getOptionalParam( self, key, default=None ):
        try:
            return rospy.get_param( key )
        except KeyError,e:
            return default

    def openBagfile( self ):
        # this creates the bagfile
        rospy.loginfo( "Logging to " + self.bag_local_filepath )
        self.bag = rosbag.Bag( self.bag_local_filepath, 'w' )

    def init_stop_service( self ):
        rospy.loginfo( 'Setting up stop service' )
        rospy.Service( '~stop', Trigger, self.trigger_callback_stop )

    def active(self):
    
        return global_lock.active_bag		
		  
    def trigger_callback_stop(self, req):
        res = TriggerResponse()
        global_lock.active_bag = False
        res.success.data = True
        res.error_message.data = "Bagfile recording stopped"
        print res.error_message.data
        return res  
    def tf_trigger(self, reference_frame, target_frame, tfs):
        #  this function is responsible for setting up the triggers for recording
        # on the bagfile.
        
        # sequence for calculating distance and yaw rotation for defining if a 
        # recording trigger is set according to the trigger value on the yaml file
        
        self.tfL.waitForTransform(reference_frame, target_frame, rospy.Time(0), rospy.Duration(3.0))
        trans, rot = self.tfL.lookupTransform(reference_frame, target_frame, rospy.Time(0))
        
        x = trans[0] - self.current_translation[target_frame][0]
        y = trans[1] - self.current_translation[target_frame][1]
        
        distance_trans = math.sqrt(x*x + y*y)
        distance_rot = abs(euler_from_quaternion(rot)[2] - euler_from_quaternion(self.current_rotation[target_frame])[2])
        
        if("trigger_record_translation" in tfs and distance_trans >= tfs["trigger_record_translation"]):
            rospy.loginfo("triggered for translation, trans = " + str(distance_trans))
            self.current_translation[target_frame] = trans
            self.current_rotation[target_frame] = rot
            return "triggered"
            
        if("trigger_record_rotation" in tfs and distance_rot >= tfs["trigger_record_rotation"]):
            rospy.loginfo("triggered for rotation, rot = " + str(distance_rot))
            self.current_translation[target_frame] = trans
            self.current_rotation[target_frame] = rot
            return "triggered"
        
        return "not_triggered"
        
    def bag_processor(self, tfs=None):
        
        trigger_position = self.tf_trigger(tfs["reference_frame"], tfs["target_frame"], tfs)
        return trigger_position



shutdown = False
def waitForShutdown():
    rospy.Service('logger/shutdown', Trigger, shutdownReceived )
    rospy.loginfo("Published shutdown" )
    i = 0
    global shutdown
    while not shutdown and i < 5:
        print 'Waiting for shutdown.'
        time.sleep( 0.5 )
        i += 1

def shutdownReceived( req ):
    global shutdown
    shutdown = True
    res = TriggerResponse()
    res.success.data = True
    res.error_message.data = "Shutting down"
    print res.error_message.data
    return res

if __name__ == "__main__":
    rospy.init_node('topics_bag')
    bagR = topics_bag()
    rospy.sleep(2)
    time_step  = rospy.Duration.from_sec( bagR.trigger_timestep )
    start_time = rospy.Time.now()

    with bagR.bag as bagfile:
        rate = rospy.Rate(10) #Hz
        topics_t = []
        topics_c = []	
        for tfs in bagR.trigger_topics:
            topic_r = record_topic.record_topic( tfs, bagfile )
            topics_t.append(topic_r)
        for tfc in bagR.continuous_topics:
            topic_r = record_topic.record_topic( tfc, bagfile, continuous=True )
            topics_c.append(topic_r)
        rospy.sleep(2)
        sleep_interrupted = False

        if not rospy.is_shutdown():
            bagR.init_stop_service()
        while bagR.active() and not rospy.is_shutdown() and not sleep_interrupted:
            if bagR.active()==1:
                # listen to tf changes
                for tfs in bagR.wanted_tfs:
                    triggers = bagR.bag_processor(tfs)
                    if(triggers == "triggered"):
                        rospy.loginfo("triggered by tf")
                        start_time = rospy.Time.now()
                        #Records the triggered topics
                        for tops_c, tfm in itertools.izip(topics_t, bagR.trigger_topics):
                            tops_c.record()
                    else:
                        rospy.logdebug("not triggered")
                # listen to ellapsed time
                time_msg = "time passed:" + (str)((rospy.Time.now() - start_time).to_sec())
                rospy.logdebug(time_msg)
                
                if(rospy.Time.now() - start_time > time_step):
                    rospy.loginfo("triggered by time")
                    start_time = rospy.Time.now()
                    for tops_c, tfm in itertools.izip(topics_t, bagR.trigger_topics):
                        tops_c.record()
                # sleep until next check

            try:
                rate.sleep()
            except rospy.exceptions.ROSInterruptException,e:
                sleep_interrupted = True
			
	# closing bag file
    rospy.loginfo("Closing bag file")
    bagR.close()
    waitForShutdown()

