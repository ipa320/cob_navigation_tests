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
import rospy

import rosbag
from std_msgs.msg import Int32, String

import tf
from tf.msg import *
from tf.transformations import euler_from_quaternion

from simple_script_server import *
sss = simple_script_server()

from kinematics_msgs.srv import *
from std_msgs.msg import *
from sensor_msgs.msg import *
from move_base_msgs.msg import *
from visualization_msgs.msg import *

import global_lock
import rostopic, record_topic
import math, uuid, re, tempfile, time, os, sys, subprocess, itertools, shutil

class CopyException( Exception ):
    def __init__( self, source, target, err ):
        msg = 'Could not copy file %s to %s' % ( source, target )
        if err: msg += 'Err:\n%s' % err
        Exception.__init__( self, msg )

class SSHCopier():
    pattern = '([^@]+)@([^:]+):(.+)'

    @staticmethod
    def matcher( uri ):
        return re.match( SSHCopier.pattern, uri ) 

    @staticmethod
    def matches( uri ):
        return SSHCopier.matcher( uri ) != None

    def __init__( self, uri ):
        matcher       = SSHCopier.matcher( uri )
        self.username = matcher.group( 1 )
        self.host     = matcher.group( 2 )
        self.path     = matcher.group( 3 )

    def _wrapBySsh( self, cmd ):
        ssh = 'ssh -o ConnectTimeout=30s -o PasswordAuthentication=no %s@%s' % ( \
            self.username, self.host )
        sshArgs = ssh.split( ' ' )
        cmdArgs = cmd.split( ' ' )
        return sshArgs + cmdArgs

    def assertWritable( self ):
        args = self._wrapBySsh( 'touch %s/.connection_test' % self.path )
        success, stdout = self._execute( args )
        if not success:
            msg  = "Couldn't write to directory %s as %s on host %s," % ( \
                    self.path, self.username, self.host )
            msg += "\n\ncmd: %s" % args
            msg += "\n\nstdout+sterr: %s" % stdout
            raise Exception( msg )
        return True

    def copyFile( self, localFilepath ):
        args = self._scpCommandArgs( localFilepath )
        success, stdout = self._execute( args )
        if not success:
            target= "%s@%s:%s/" % ( self.username, self.host, self.path )
            raise CopyException( localFilepath, target )

    def _scpCommandArgs( self, localFilepath ):
        filename = os.path.basename( localFilepath )
        cmd = 'scp %s %s@%s:%s/%s' % ( localFilepath, self.username,
            self.host, self.path, filename )
        return cmd.split( ' ' )

    def _execute( self, args ):
        PIPE = subprocess.PIPE
        p    = subprocess.Popen( args, stdout=PIPE, stderr=PIPE )
        stdin, stdout = p.communicate()
        success       = p.returncode == 0
        return success, stdout


class LocalCopier():
    def __init__( self, path ):
        self.path = path

    def assertWritable( self ):
        if not os.access( self.path, os.W_OK ):
            raise Exception( 'Cannot write to local filesystem on %s' %
                self.path )
        return True

    def copyFile( self, localFilepath ):
        filename       = os.path.basename( localFilepath )
        targetFilepath = '%s/%s' % ( self.path, filename )
        try:
            shutil.copyfile( localFilepath, targetFilepath )
        except IOError,e:
            raise CopyException( localFilepath, targetFilepath )

class topics_bag():

    def __init__(self):
        self.loadParams()
        self.setupFileCopier()
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

    def setupFileCopier( self ):
        if SSHCopier.matches( self.bag_target_path ):
            self._fileCopier = SSHCopier( self.bag_target_path )
        else:
            self._fileCopier = LocalCopier( self.bag_target_path )
        self._fileCopier.assertWritable()

    def close( self ):
        self.bag.close()
        try:
            self._fileCopier.copyFile( self.bag_local_filepath )
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
        self.trigger_record_translation = self.requiredParam('~trigger_record_translation')
        self.trigger_record_rotation    = self.requiredParam('~trigger_record_rotation')
        self.trigger_timestep           = self.requiredParam('~trigger_timestep')
        self.wanted_tfs                 = self.requiredParam('~wanted_tfs')
        self.trigger_topics             = self.requiredParam("~trigger_topics")
        self.continuous_topics          = self.requiredParam("~continuous_topics")
        self.bag_target_path            = self.requiredParam("~bag_path")
        self.bag_local_path             = tempfile.gettempdir()
        self.bag_filename               = '%s.bag' % uuid.uuid4()
        self.bag_local_filepath         = self.bag_local_path + '/' + self.bag_filename

    def requiredParam( self, key ):
        value = rospy.get_param( key )
        if value is None:
            raise Exception( 'Could not load paramter %s' % key )
        return value

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
    rospy.Service('/logger/shutdown', Trigger, shutdownReceived )
    rospy.loginfo("Published shutdown" )
    global shutdown
    while not shutdown:
        print 'Waiting for shutdown.'
        time.sleep( 1 )

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
    time_step = rospy.Duration.from_sec(bagR.trigger_timestep)
    start_time = rospy.Time.now()

    with bagR.bag as bagfile:
        rate = rospy.Rate(10) #Hz
        topics_t = []
        topics_c = []	
        for tfs in bagR.trigger_topics:
            topic_r = record_topic.record_topic(tfs, bagfile)
            topics_t.append(topic_r)
        for tfc in bagR.continuous_topics:
            topic_r = record_topic.record_topic(tfc, bagfile, continuous=True)
            topics_c.append(topic_r)
        rospy.sleep(2)
        sleep_interrupted = False
        wasActive = False
        while ( not wasActive or bagR.active()) and not rospy.is_shutdown() and not sleep_interrupted:
            if bagR.active()==1:
                if not wasActive:
                    bagR.init_stop_service()
                wasActive = True
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

