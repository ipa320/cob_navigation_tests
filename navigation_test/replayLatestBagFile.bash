#!/bin/bash
latestFile=`find /share/uhr-se/bag_record -printf '%T+ %p\n' | sort -r | head -n 1| sed -r 's/[^\s]+\s(.*)/\1/'`
echo $latestFile
rosbag play $latestFile
