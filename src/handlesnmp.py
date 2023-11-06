from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget,\
                         ContextData, ObjectType, ObjectIdentity, nextCmd
import time


SYSTEM_OID = ".1.3.6.1.2.1.1.1.0"
UDP_IN_OID = "1.3.6.1.2.1.7.1.0"       # The total number of UDP datagrams delivered to UDP users.
UDP_OUT_OID = "1.3.6.1.2.1.7.4.0"      # The total number of UDP datagrams sent from this entity.
IP_RTABLE_OID = "1.3.6.1.2.1.4.21"     # This entity's IP Routing table.
IP_ROUTE_DEST_OID = "1.3.6.1.2.1.4.21.1.1"
IP_ROUTE_NEXT_HOP_OID = "1.3.6.1.2.1.4.21.1.7"
IP_ROUTE_TYPE_OID = "1.3.6.1.2.1.4.21.1.8
IP_ROUTE_PROTO_OID = "1.3.6.1.2.1.4.21.1.9"
IP_ROUTE_AGE_OID = "1.3.6.1.2.1.4.21.1.10"

class SNMPConnection:
    def __init__(self, name, ip, port, community) -> None:
        self.ip = ip
        self.port = port
        self.name = name
        self.community = community

    # Internal method
    # grab SNMP data and return it.
    def __getSNMP(self, oid) -> tuple:
        auth = cmdgen.CommunityData(self.community.replace('"', '').replace("'", ""))

        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        auth,
        cmdgen.UdpTransportTarget((self.ip, self.port)),
        cmdgen.MibVariable(oid),
        lookupMib=False,
        )

        return errorIndication, errorStatus, errorIndex, varBinds
    
    def __getNextSNMP(self, oid) -> tuple:
        # TODO: implement an SNMP getNext function as a base, get next until the end of the table
        # Unused, switch to getBulkRequest
        pass

    def __getBulkSNMP(self, oid):
        print("Current OID", oid)
        oidTuple = tuple(map(int, oid.split('.')))
        print("OID Tuple", oidTuple)

        print("entry")
        cmd = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmd.bulkCmd(  
                    cmdgen.CommunityData('test-agent', self.community.replace('"', '').replace("'", "")),  
                    cmdgen.UdpTransportTarget((self.ip, self.port)),  
                    0, 
                    25, 
                    oidTuple, # ipRouteTable (1,3,6,1,2,1,4,21,1)
                )

        if errorIndication:
            print (errorIndication)
        else:
            if errorStatus:
                print (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
            else: #Everything is print in this format
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        print (name.prettyPrint(), val.prettyPrint())
                print("All data printed, exiting the function...")
                
        return varBindTable

        

    def getSystemDesc(self) -> str:
        global SYSTEM_OID
        err, errStatus, errIndex, var = self.__getSNMP(SYSTEM_OID)
        oid, value = var[0]
        return value

    def getUDPInNow(self) -> int:
        global UDP_IN_OID
        err, errStatus, errIndex, var = self.__getSNMP(UDP_IN_OID)
        oid, value = var[0]
        return value

    def getUDPOutNow(self) -> int:
        global UDP_OUT_OID
        err, errStatus, errIndex, var = self.__getSNMP(UDP_OUT_OID)
        oid, value = var[0]
        return value

    def getIPRouteTable(self) -> {}:
        result = self.__getBulkSNMP(IP_RTABLE_OID)
        return result

    def getName(self)-> str:
        return self.name   
        
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


if __name__ == "__main__":
    getNextSNMP("10.99.1.2", "161", IP_RTABLE_OID, "management")

    #instance = SNMPConnection("10.99.1.2", "161", "management")
    # print(instance.getSystemDesc())
    #print(instance.getUDPInNow())
    # print(instance.getUDPOutNow())
