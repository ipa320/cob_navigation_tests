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
# This module records topics according to triggering events
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
from tf.msg             import *
from tf.transformations import euler_from_quaternion
import rostopic
import global_lock

class record_topic():

    def __init__(self, topic_info, bagfile, continuous=False):
        self.msg             = None
        self.topic_name      = topic_info[ 'topic' ]
        self.topic_type_info = topic_info[ 'type' ]
        self.continuous      = continuous
        self.bagfile         = bagfile

        self._setupSubscriber()
        global_lock.locked = False
        
    def _setupSubscriber( self ):
        parts       = self.topic_type_info.split( '/' )
        name        = parts.pop()
        module_name = '.'.join( parts ) + '.msg'

        # Import the topic type and setup the topic
        module  = __import__( module_name, fromlist=[ name ])
        self.topic_type   = getattr( module, name )
        rospy.Subscriber( self.topic_name, self.topic_type, self.callback )

        rospy.loginfo( 'Recording topic "%s"' % self.topic_name )
        
    def lock(self):
        global_lock.locked = True
        
    def unlock(self):
        global_lock.locked = False     
        
    def callback(self, msg):
        self.msg = msg
        if self.continuous:
            self.record()
    
    def record(self):
        if(self.msg!=None):
            if not global_lock.locked:
                try:
                    if(global_lock.active_bag):
                        self.lock()
                        self.bagfile.write(self.topic_name, self.msg)
                        self.unlock()
                except KeyError, e:
                    rospy.loginfo(self.msg)
