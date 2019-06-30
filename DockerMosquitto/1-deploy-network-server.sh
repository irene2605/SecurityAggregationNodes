#!/bin/bash

echo "----- Create 'mosquitto' network -----------------------"
# create network "mosquitto" with subnet 172.20.0.0/16 and gateway 172.20.0.1 (this is your host's IP)
docker network create --driver bridge --subnet 172.20.0.0/16 --gateway 172.20.0.1 mosquitto
echo

echo "----- Create 'mosquitto-server' container ---------------"
docker run -d --name mosquitto-server --network mosquitto --ip 172.20.0.2 eclipse-mosquitto
echo
