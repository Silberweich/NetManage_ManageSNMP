from pysnmp.entity.rfc3413.oneliner import cmdgen
import time

SYSTEM_OID = ".1.3.6.1.2.1.1.1.0"
IP_RTABLE_OID = ""
UDP_IN_OID = "1.3.6.1.2.1.7.1.0"
UDP_OUT_OID = "1.3.6.1.2.1.7.4.0"

class SNMPConnection:
    def __init__(self, ip, port, community) -> None:
        self.ip = ip
        self.port = port
        # self.oid = None
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
        # TODO: implement an SNMP getNext function as a base
        pass

    def getSystemDesc(self) -> str:
        global SYSTEM_OID
        err, errStatus, errIndex, var = self.__getSNMP(SYSTEM_OID)
        oid, value = var[0]
        return value

    def getUDPInNow(self) -> tuple[float, int]:
        global UDP_IN_OID
        err, errStatus, errIndex, var = self.__getSNMP(UDP_IN_OID)
        oid, value = var[0]
        return time.time(), value

    def getUDPOutNow(self) -> tuple[float, int]:
        global UDP_OUT_OID
        err, errStatus, errIndex, var = self.__getSNMP(UDP_OUT_OID)
        oid, value = var[0]
        return time.time(), value

    def getIPRouteTable(self) -> []:
        # TODO: do the shit
        pass    
        
# 1.3.6.1.2.1.1.5.0 "management"
def getSNMP(ip, port, oid, community):
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
    

if __name__ == "__main__":
    getSNMP("10.99.1.2", "161", UDP_IN_OID, "management")

    instance = SNMPConnection("10.99.1.2", "161", "management")
    # print(instance.getSystemDesc())
    print(instance.getUDPInNow())
    # print(instance.getUDPOutNow())