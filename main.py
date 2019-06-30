# coding=utf-8
"""Main"""

import sys
import callback
import random
import netaddr
import threading
import time
import queue

from HeavyHitters import HeavyHitters
from InterfazRules import IPTables
from tshark import Capture
#from threading import Lock

# Generate random IPs
def generateRandomIP():
    "" "Method Chain" ""
    intip = random.randint(823284281, 823284291)
    return str(netaddr.IPAddress(intip))

def funct_queue(element, function):
    while True:
        item=element.get()
        if item is None:
            break
        #function = HeavyHitters(numbuckets, threshold, hh)
        print ('Received IP:', item)
        print ('HeavyHitters elements before:', function.getelements())
        function.addelement(item)
        print ('HeavyHitters elements after:', function.getelements())        
        element.task_done()   

def funct_unblock(hh):
    while True:
        element , delay = hh.getElementToUnblock()
        if element is None:
            time.sleep(0.5)
            continue
        if delay>0: time.sleep(delay)
        hh.unblock(element)
        
def main():
    "" "Main Chain" ""
    iptables = IPTables()
    numbuckets = 10
    hhCallback = callback.mycallback(iptables)
    threshold = 5 
    blocktime = 10
    hh=HeavyHitters(numbuckets, threshold, hhCallback.execute, blocktime)

    element = queue.Queue()
    th2=threading.Thread(target=funct_queue, args=(element, hh))
    th2.start()

    th3=threading.Thread(target=funct_unblock, args=(hh,))
    th3.start()

    capture = Capture('any', 'tcp port 1883', element)
    capture.run()

if __name__ == '__main__':
    sys.exit(main())
        
