from src.handledb import HandleInfluxDB
from src.handlesnmp import SNMPConnection
import time
import threading

deviceList = {
    "C2800R": "192.168.100.1",
    "C1800R": "192.168.100.2",
    "C3560SW": "192.168.200.2",
    "C2960SW": "10.99.1.2"
}

listSNMPConn = {}
listDBConn = {}
listThreads = []

# this part initialize classes for each device
for device in deviceList:
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

    # db.storeDataToDB(udp_in, "type:in")
    # db.storeDataToDB(udp_out, "type:out")

def storeDataIntervalWrapper(interval: int, snmp:SNMPConnection, db:HandleInfluxDB) -> None:
    while True:
        storeData(snmp, db)
        time.sleep(interval)

if __name__ == "__main__":
    for device in deviceList:
        # print(device, listSNMPConn[device])
        listThreads.append(threading.Thread(target=storeDataIntervalWrapper, args=(60, listSNMPConn[device], listDBConn[device],)).start())
    print("do what ever rn")