# coding=utf-8
"""Tshark"""

import pyshark
import sys

class Capture(object):
    def __init__(self, interface, capFilter, element):
        self.__interface = interface #'lo'
        self.__capFilter = capFilter #'tcp'
        self.__element = element #queue

    def run(self):
        capture = pyshark.LiveCapture(self.__interface, self.__capFilter)
        for packet in capture.sniff_continuously():
            #IP        
            iplayer = getattr(packet, 'ip')
            ipsrc = None if(iplayer is None) else getattr(iplayer, 'src')
            ipdst = None if(iplayer is None) else getattr(iplayer, 'dst')
            #UDP
            srcport=None
            dstport=None
            protocol=None
            mqttmessagetype=None
            udplayer = getattr(packet, 'udp', None)
            if(udplayer is not None):
                srcport = int(getattr(udplayer, 'srcport'))
                dstport = int(getattr(udplayer, 'dstport'))
                protocol = 'UDP'
            #TCP
            tcplayer = getattr(packet, 'tcp', None)
            if(tcplayer is not None):
                srcport = int(getattr(tcplayer, 'srcport'))
                dstport = int(getattr(tcplayer, 'dstport'))
                protocol = 'TCP'
            #MQTT
            mqttlayer = getattr(packet, 'mqtt', None)
            if(mqttlayer is not None):
                mqttmessagetype = int(getattr(mqttlayer, 'msgtype'))

#Puerto 1883 puerto estandar para comunicaciones sin encriptar
#Puerto 8883 y 8884 usan SSL/TLS, 8884 requiere certificado (solo tcp)
            if(dstport==1883 and protocol=='TCP' and mqttmessagetype == 3):
                print('Calling Heavy Hitters')
                self.__element.put(ipsrc)
 
            #print('Packet:', (ipsrc, ipdst, srcport, dstport))
	
