import argparse
import ipaddress
import asyncio 
from pysnmp import hlapi 
from pysnmp.entity.rfc3413.oneliner import cmdgen

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