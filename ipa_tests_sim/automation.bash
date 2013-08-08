#!/bin/bash
mkdir -p /share/uhr-se/bagrecord
export ROBOT_ENV=ipa-apartment
export ROS_MASTER_URI=http://localhost:22422
function killAllRosAndGazebo(){
    pids=`ps ax | grep 'ros\|gazebo' | grep -v "analysis" | sed -rn "s/\s*([0-9]+).*/\1/p"`
    for pid in $pids; do kill -9 $pid; done
}

while true; do
    mkdir -p /share/uhr-se/bagrecord

    for route in "room" "ipa-apartment"; do
        for robot in "desire" "cob3-3"; do
            for nav in "2dnav_ipa_extloc_diff" "2dnav_ipa_extloc" "2dnav_ros_dwa" "2dnav_ros_tr"; do
                if ( [ $nav == "2dnav_ipa_extloc_diff" ] || [ $nav == "2dnav_ipa_extloc" ] ) && [ $robot == "desire" ]; then
                    continue;
                fi

                echo "Starting $robot on $route with $nav"
                sleep 2
                export ROBOT=$robot
                killAllRosAndGazebo; sleep 2; killAllRosAndGazebo; sleep 10
                timeout -s 9 1200 rostest ipa_tests_sim $route.launch robot:=$robot navigation:=$nav
                sleep 20
            done
        done
    done
done
