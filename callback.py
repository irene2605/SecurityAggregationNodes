# coding=utf-8
"""Callback"""

class mycallback(object):

    def __init__(self, iptables):
        self.iptables = iptables

    def execute(self,element):
        self.iptables.addrule(element)
        print('Callback called')
