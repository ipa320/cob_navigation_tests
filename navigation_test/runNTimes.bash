#!/bin/bash
echo "Run $1 times"
for ((i=1;i<=$1;i++)); do
    echo "Run #$i"
    python navigation_test.py
done
