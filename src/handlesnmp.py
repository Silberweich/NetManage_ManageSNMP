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
IP_ROUTE_TYPE_OID = "1.3.6.1.2.1.4.21.1.8"
IP_ROUTE_PROTO_OID = "1.3.6.1.2.1.4.21.1.9"
IP_ROUTE_AGE_OID = "1.3.6.1.2.1.4.21.1.10"

IP_ROUTE_TABLE_ENT = [
"1.3.6.1.2.1.4.21.1.1",
"1.3.6.1.2.1.4.21.1.7",
"1.3.6.1.2.1.4.21.1.8",
"1.3.6.1.2.1.4.21.1.9",
"1.3.6.1.2.1.4.21.1.10"]

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


    def __getBulkSNMP(self, oid):
        #print("Current OID", oid)
        oidTuple = tuple(map(int, oid.split('.')))
        #print("OID Tuple", oidTuple)

        #print("entry")
        cmd = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmd.bulkCmd(  
                    cmdgen.CommunityData('test-agent', self.community.replace('"', '').replace("'", "")),  
                    cmdgen.UdpTransportTarget((self.ip, self.port)),  
                    0, # From 0th record
                    100, # to 100th record, unless the table is longer than that, this will end as is
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
                """
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        print("Name", name.prettyPrint(), "Value", val.prettyPrint())
                print("All data printed, exiting the function...")
                """    
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
    
    def getIPRouteDest(self):
        global IP_ROUTE_TABLE_ENT

        varBindTable = self.__getBulkSNMP(IP_ROUTE_DEST_OID)

        oid_name_table = ["IP ROUTE DESTINATION", "IP ROUTE NEXT HOP", "IP ROUTE TYPE", "IP ROUTE PROTO", "IP ROUTE AGE"]

        all_table = []

        i = 0

        for oid in IP_ROUTE_TABLE_ENT:
            var = self.__getBulkSNMP(oid)
            temp_list = []
            temp_list.append(oid_name_table[i])
            for varBindTableRow in var:
                for name, val in varBindTableRow:
                    temp_list.append(val.prettyPrint())
                    #dest_table[i].append(val)

                    #print(val.prettyPrint())
            all_table.append(temp_list)
            i += 1

        return all_table

    def getName(self)-> str:
        return self.name   


if __name__ == "__main__":
    pass