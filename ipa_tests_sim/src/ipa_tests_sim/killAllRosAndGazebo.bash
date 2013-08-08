#!/bin/bash
pids=`ps ax | grep 'ros\|gazebo' | grep -v 'analysis' | sed -rn "s/\s*([0-9]+).*/\1/p"`
for pid in $pids; do kill -9 $pid; done
