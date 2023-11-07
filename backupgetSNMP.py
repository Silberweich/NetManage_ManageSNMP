import argparse
import ipaddress
import asyncio 
from pysnmp import hlapi 
from pysnmp.entity.rfc3413.oneliner import cmdgen
import re

# Source: https://stackoverflow.com/questions/8643047/how-to-make-a-single-getnext-query-in-pysnmp
def getNextSNMPStackOverflow(ip, port, oid, community):
    print("Current OID", oid)
    oidTuple = tuple(map(int, oid.split('.')))
    print("OID Tuple", oidTuple)
    cmdGen  = cmdgen.AsynCommandGenerator()
    #print("Type:", type((1,3,6,1,2,1,7,4,0)))

    cmdGen.nextCmd(
    cmdgen.CommunityData(community.replace('"', '').replace("'", "")),
    cmdgen.UdpTransportTarget((ip, port)),
        (oidTuple,),
        (cbFun, None))

    cmdGen.snmpEngine.transportDispatcher.runDispatcher()

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
        return 1
    if errorStatus:
        print(errorStatus.prettyPrint())
        return 1
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            print('%s = %s' % (oid.prettyPrint(),
                               val and val.prettyPrint() or '?'))
            
def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBindTable, cbCtx):
    if errorIndication:
        print(errorIndication)
        return 1
    if errorStatus:
        print(errorStatus.prettyPrint())
        return 1
    for varBindRow in varBindTable:
        for oid, val in varBindRow:
            print('%s = %s' % (oid.prettyPrint(),
                               val and val.prettyPrint() or '?'))

def getNextSNMP(ip, port, oid, community):
    print("entry")
    cmd = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmd.bulkCmd(  
                cmdgen.CommunityData('test-agent', 'management'),  
                cmdgen.UdpTransportTarget((ip, 161)),  
                0, 
                25, 
                (1,3,6,1,2,1,4,21,1), # ipRouteTable
            )

    if errorIndication:
        print (errorIndication)
    else:
        if errorStatus:
            print (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                )
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    print (name.prettyPrint(), val.prettyPrint())
    print("exit")

    def __getNextSNMP(self, oid) -> tuple:
        # TODO: implement an SNMP getNext function as a base, get next until the end of the table
        # Unused, switch to getBulkRequest
        pass

# 1.3.6.1.2.1.1.5.0 "management"
def getSNMP(ip, port, oid, community):
#     >>> from 

#  g = nextCmd(snmpDispatcher(),
#              CommunityData('public'),
#              UdpTransportTarget(('demo.snmplabs.com', 161)),
#              ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')))
    auth = cmdgen.CommunityData(community.replace('"', '').replace("'", ""))

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((ip, port)),
    cmdgen.MibVariable(oid),
    lookupMib=False,
    )

    # if errorIndication:
    #     print(errorStatus, errorIndication, errorIndex, "error")
    #     exit()
    
    for i in varBinds:
        
        oid, val = i
        #print(i)
        print("Error Status:", errorStatus,type(i), "::", oid, "::", val, str(val), type(val))

def getIPRouteTable(self) -> {}:
        # Get Everything from  
        # IPRoutetable 1.3.6.1.2.1.4.21 Down to 1.3.6.1.2.1.4.21.1.10
        IP_RTABLE_OID = "test"
        varBindTable = self.__getBulkSNMP(IP_RTABLE_OID)
        
        pattern = re.compile(r".*2\.4\.21\.1\.[1789].*")

        matched = []

        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print("Name", name.prettyPrint(), "Value", val.prettyPrint())
                print("Test string", str(name))
                match = pattern.search(str(name))
                print(match)
                if match:
                    matched_string = match.group(0)
                    print("Match found:", matched_string)
                else:
                    continue
        print("All data printed, exiting the function...")
        
        return matched