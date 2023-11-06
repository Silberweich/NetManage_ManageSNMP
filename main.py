from src.handledb import HandleInfluxDB
from src.handlesnmp import SNMPConnection
import time
import threading

class DataProcessing:
    def __init__(self, devName:str, conn:SNMPConnection, db:HandleInfluxDB) -> None:
        self.devName = devName
        self.conn = conn
        self.db = db

    def getPPNToDB(self, interval:int) -> None:
        while True:
            self.db.storeDataToDB(self.conn.getUDPInNow, "type:in")
            self.db.storeDataToDB(self.conn.getUDPOutNow, "type:out")
            time.sleep(interval)
    
deviceList = {
    "C2800R": "192.168.100.1",
    "C1800R": "192.168.100.2",
    "C3560SW": "192.168.200.2",
    "C2960SW": "10.99.1.2",
    "pc": "127.0.0.1"
}

listSNMPConn = {}
listDBConn = {}
listThreads = []

# this part initialize classes for each device
for device in deviceList:
    if device == "pc":
        listSNMPConn[device] = (SNMPConnection(device, deviceList[device], "161", "public"))
    else:
        listSNMPConn[device] = (SNMPConnection(device, deviceList[device], "161", "management"))
    # TODO: See this shit? implement a way to keep multiple database connection like this
    listDBConn[device] = (HandleInfluxDB(device, deviceList[device], "thisatest", "whatever",))

def initSysDescr(snmp:SNMPConnection) -> None:
    # TODO: Get system description for such device, and send to somewhere (NodeRed)
    pass

def updateRoutingTable(snmp: SNMPConnection) -> None:
    # TODO: Get IP Routing Table for such device (that has routing table), and send to somewhere (NodeRed)
    pass

def storeData(snmp:SNMPConnection, db:HandleInfluxDB) -> None:
    
    udp_in = snmp.getUDPInNow
    udp_out = snmp.getUDPOutNow
    devicename = "dog" #devicename from devicelist should be string
    db.sendToDB()
    # db.storeDataToDB(udp_in, "type:in")
    # db.storeDataToDB(udp_out, "type:out")

def storeDataIntervalWrapper(interval: int, snmp:SNMPConnection, db:HandleInfluxDB) -> None:
    while True:
        storeData(snmp, db)
        time.sleep(interval)

## Run all kind of
if __name__ == "__main__":
    # for device in deviceList:
    #     # print(device, listSNMPConn[device])
    #     listThreads.append(threading.Thread(target=storeDataIntervalWrapper, args=(60, listSNMPConn[device], listDBConn[device],)).start())

    for i in range(100):
        for device in deviceList:
            #print(device, listSNMPConn[device])
            print(f"{i} device {device} in: {listSNMPConn[device].getUDPInNow()} | out: {listSNMPConn[device].getUDPOutNow()}")

    # Testing SNMP
    testGetNext = SNMPConnection("getNext", "10.99.2.1", 161, "management")
    print(testGetNext.getSystemDesc)
    