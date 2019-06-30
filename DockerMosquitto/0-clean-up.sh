#!/bin/bash

echo "----- Remove 'mosquitto' containers --------------------"
docker ps -a | grep "mosquitto" | awk '{print $1}' | xargs -r docker rm -f
echo

echo "----- Remove 'mosquitto' network -----------------------"
docker network ls | grep "mosquitto" | awk '{print $1}' | xargs -r docker network rm
echo
