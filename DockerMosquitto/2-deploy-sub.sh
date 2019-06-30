#!/bin/bash

echo "----- Create 'mosquitto-sub' container ---------------"
docker run -it --rm --name mosquitto-sub --network mosquitto --ip 172.20.0.3 eclipse-mosquitto mosquitto_sub -h 172.20.0.2 -t '#' -v
