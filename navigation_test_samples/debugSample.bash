#!/bin/bash
dir=$( cd $(dirname $0) ; pwd -P )
launch=$1
if [ -z "$launch" ]; then
    ls $dir/launch
    exit 1
fi
if [ ! -f "$launch" ]; then
    filename=`find $dir/launch -iname "*$launch*" | head -n 1`
    launch=`basename "$filename"`
fi
if [ -z "$launch" ]; then
    echo "No launch file found"
    exit 2
fi

export ROS_MASTER_URI=http://localhost:22422
rxconsole &
rosrun rviz rviz &
rostest navigation_test_samples $launch
killall rviz
