# coding=utf-8
"""Rules"""

import iptc

class _Firewall(object):
    "" "Class Chain" ""
    
    def __init__(self, ipcall):
        self.__ipcall = ipcall
        
    def flushrules():
        "" "Method Chain" ""
        raise Exception ("To be implemented")
        
    def createrule():
        "" "Method Chain" ""
        raise Exception ("To be implemented")
        
    def addrule(self, ipcall):
        "" "Method Chain" ""
        raise Exception ("To be implemented")
        
    def deleterule(self, ipcall):
        "" "Method Chain" ""
        raise Exception ("To be implemented")
        
        
class IPTables(_Firewall):
    "" "Class Chain" ""
    
    def __init__(self, chainName='INPUT'):
        print ("Initializing iptables")

    def flushrules(self):
        "" "Method Flush Chain" ""
        print ('Flushing rules')
        table = iptc.Table('filter')
        table.autocommit = False
        chain = iptc.Chain(table, "INPUT")
        for rule in chain.rules:
            chain.delete_rule(rule)
        table.commit()
        table.autocommit = True


    def createrule():
        rule = iptc.Rule()
        rule.in_interface = "eth0"
        rule.src = "192.168.1.0/255.255.255.0"
        rule.protocol = "tcp"

    def addrule(self, ipcall):
        print ('Adding rule', ipcall)
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        # Create rule
        rule = iptc.Rule()
        # Any interface
        rule.src = ipcall
        # Target Rule
        target = iptc.Target(rule, "DROP")
        rule.target = target
        # Insert rule
        chain.insert_rule(rule)
        print ('Added Rule')

    def deleterule(self, ipcall):
        print ('Deleting rule', ipcall)
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        # Create rule
        rule = iptc.Rule()
        # Any interface
        rule.src = ipcall
        # Target Rule
        target = iptc.Target(rule, "DROP")
        rule.target = target
        # Insert rule
        chain.delete_rule(rule)   
        print ('Deleted Rule')

