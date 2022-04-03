#!/bin/bash

cd /Volumes/HDD/Data/ztd/test

echo "" > out.txt

for file in obs_files/*.mom; do
    site=${file:0-8:4}
    analyse_timeseries.py $site WN
    if [ $? -ne 0 ]; then
        echo "Error in analyse_timeseries.py"
        exit 1
    fi
    cat estimatetrend.json | jq ".BIC" >> out.txt
done