# coding=utf-8
"""HeavyHitters"""
import time, sys
from InterfazRules import IPTables
from threading import Thread, RLock

class HeavyHitters(object):
    "" "Class Chain" ""

    def __init__(self, numbuckets, threshold, callbacks, blocktime):
        self.__numbuckets = numbuckets
        self.__threshold = threshold
        self.__callbacks = callbacks
        self.__dictionary = {}
        self.__rules = []  #Orden de las ips
        self.__times = {}  #Mapeo del instante de tiempo de cada ip
        self.__lock = RLock()
        self.__blocktime = blocktime    

    def unblock(self, direcip):
        iptables = IPTables()
        with self.__lock:
            element, delay = self.getElementToUnblock()
            if direcip != element: return
            if delay>0: return
            self.__rules.remove(element)
            del self.__times[element]
            del self.__dictionary[element]
            iptables.deleterule(direcip)

    def getElementToUnblock(self):
        with self.__lock:
            if len(self.__rules) == 0: return None, None 
            element = self.__rules[0]
            t=time.time()
            delay=self.__times[element]+self.__blocktime-t       
            return element, delay

    def addelement(self, element):
        "" "Method Chain" ""
        # Check IP in the dictionary
        contador = self.__dictionary.get(element)
        if contador is not None:
            contador += 1
            self.__dictionary.update({element: contador})
            if contador >= self.__threshold:
                #if callback is not none, call callback
                if self.__callbacks is not None:
                    if element not in self.__times:
                        self.__rules.append(element)
                        self.__times[element]=time.time()
                        self.__rules = sorted(self.__rules, key = lambda ip: self.__times[ip])
                        # Add rule calling Callback
                        print('Calling Callback from HH with', element)
                        self.__callbacks(element)
                    #Si la regla ya esta añadida meterlos en una lista e ir comprobando con los tiempos para sacarlo de la restriccion
               
        else:
            if len(self.__dictionary) >= self.__numbuckets:
                remips = set()
                for element_, contador_ in self.__dictionary.items():
                    self.__dictionary.update({element_: contador_-1})
                    if self.__dictionary.get(element_) == 0:
                        remips.add(element_)
                for remip in remips:
                    del self.__dictionary[remip]
            self.__dictionary[element] = 1

    def getelements(self):
        "" "Method Chain" ""
        result = self.__dictionary
        return result

