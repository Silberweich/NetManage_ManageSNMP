from src.handledb import HandleInfluxDB
from src.handlesnmp import SNMPConnection
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import time
import threading 
bucket = "jeen"
org = "jeen"
token = "44KDRmqUmCSc6g5aRsL5nHXqxuVQGlmMQycnWkX4me3J6-QMbjXYaGMabYpSq5XvXxDPz_2gD7MCwS8WLfV3Hg=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)
class DataProcessing:
    def __init__(self, devName:str, conn:SNMPConnection, db:HandleInfluxDB) -> None:
        self.devName = devName
        self.conn = conn
        self.db = db
        thread = threading.Thread(target=self.getPPNToDB, args=(10,))
        thread.daemon = False                            # Daemonize thread
        thread.start() 

    def sendTableToDB() -> None:
        pass
    def sendSysDescToDB() -> None:
        pass

    def getPPNToDB(self, interval:int) -> None:
        now_in = None
        prev_in = None
        now_out = None
        prev_out = None

        print(f"{self.devName}: Starting interval data capture")

        while True:
            
            now_in = self.conn.getUDPInNow()
            now_out = self.conn.getUDPOutNow()

            if prev_in != None or prev_out != None:
                print(f"{self.devName}: IN: {now_in - prev_in} | OUT: {now_out - prev_out} # per {interval} sec")
                self.db.sendToDBudp(self.devName, int(now_in - prev_in), int(now_out - prev_out))

            prev_in = now_in
            prev_out = now_out

            time.sleep(interval)
    
deviceList = {
    "C2800R": "192.168.100.1",
    "C1800R": "192.168.100.2",
    "C3560SW": "192.168.200.2",
    "C2960SW": "10.99.1.2",
}

listSNMPConn = {}
listDBConn = {}
listThreads = []

# this part initialize classes for each device
for device in deviceList:
    listSNMPConn[device] = (SNMPConnection(device, deviceList[device], "161", "management"))
    # TODO: See this shit? implement a way to keep multiple database connection like this
    listDBConn[device] = (HandleInfluxDB(bucket, org, token, url))

# def initSysDescr(snmp:SNMPConnection) -> None:
#     # TODO: Get system description for such device, and send to somewhere (NodeRed)
#     pass

# def updateRoutingTable(snmp: SNMPConnection) -> None:
#     # TODO: Get IP Routing Table for such device (that has routing table), and send to somewhere (NodeRed)
#     pass

# def storeData(snmp:SNMPConnection, db:HandleInfluxDB) -> None:
#     udp_in = snmp.getUDPInNow
#     udp_out = snmp.getUDPOutNow

#     # db.storeDataToDB(udp_in, "type:in")
#     # db.storeDataToDB(udp_out, "type:out")

# def storeDataIntervalWrapper(interval: int, snmp:SNMPConnection, db:HandleInfluxDB) -> None:
#     while True:
#         storeData(snmp, db)
#         time.sleep(interval)

## Run all kind of
if __name__ == "__main__":
    print("doing your mom")
    for device in deviceList:
        listThreads.append(DataProcessing(device, listSNMPConn[device], listDBConn[device]))
    # for device in deviceList:
    #     # print(device, listSNMPConn[device])
    #     listThreads.append(threading.Thread(target=storeDataIntervalWrapper, args=(60, listSNMPConn[device], listDBConn[device],)).start())

    # for i in range(100):
    #     for device in deviceList:
    #         #print(device, listSNMPConn[device])
    #         print(f"{i} device {device} in: {listSNMPConn[device].getUDPInNow()} | out: {listSNMPConn[device].getUDPOutNow()}")

    # # Testing SNMP
    # testGetNext = SNMPConnection("getNext", "10.99.2.1", 161, "management")
    # print(testGetNext.getSystemDesc)
    