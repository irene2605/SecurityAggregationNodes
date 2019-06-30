#!/bin/bash

NUM_PUBLISHERS=20 # max 250
NUM_PUBLISHERS_COMP=1 # max 250
NUM_MESSAGES=10
INTER_MESSAGE_DELAY=1 #seconds
INTER_MESSAGE_DELAY_COMP=1 #seconds
TOPIC='house/bulb'
MESSAGE='on'
MESSAGE_COMP='compromised'

echo "----- Create 'mosquitto-pub' containers  ---------------"
for ((i=1;i<=$NUM_PUBLISHERS;i++));
do
	HOSTID=$((i + 3))
	docker run -d --rm --name mosquitto-pub-$i --network mosquitto --ip 172.20.0.$HOSTID eclipse-mosquitto mosquitto_pub -h 172.20.0.2 -t $TOPIC -m $MESSAGE-$i --repeat $NUM_MESSAGES --repeat-delay $INTER_MESSAGE_DELAY
done

echo "----- Create 'mosquitto-pub' containers comp ---------------"
for ((i=1;i<=$NUM_PUBLISHERS_COMP;i++));
do
	HOSTID=$((i + 3))
	docker run -d --rm --name mosquitto-comp-$i --network mosquitto --ip 172.20.1.$HOSTID eclipse-mosquitto mosquitto_pub -h 172.20.0.2 -t $TOPIC -m $MESSAGE_COMP-$i --repeat $NUM_MESSAGES --repeat-delay $INTER_MESSAGE_DELAY_COMP
done
