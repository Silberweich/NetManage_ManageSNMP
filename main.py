from src.handledb import HandleInfluxDB
from src.handlesnmp import SNMPConnection
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import time
import threading 

class DataProcessing:
    def __init__(self, devName:str, conn:SNMPConnection, db:HandleInfluxDB) -> None:
        self.devName = devName
        self.conn = conn
        self.db = db

        self.sendTableToDB()
        self.sendSysDescToDB()

        thread = threading.Thread(target=self.getPPNToDB, args=(10,))
        thread.daemon = False                            
        thread.start() 

    def sendTableToDB(self) -> None:
        data = self.conn.getIPRouteDest()
        self.db.sendToDBIPRouteTable(self.devName, data)
        
    def sendSysDescToDB(self) -> None:
        data = self.conn.getSystemDesc()
        self.db.sendToDBsystemDesc(self.devName, str(data))

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

bucket = "jeen"
org = "jeen"
token = "X3CQyUr33EdVb9Vzwa-G7MWumwtPZ8uXG9rMXuPrNNSO4vFrPje2VVUcpg9AraSnDz-Gz-DKIV-7A1aQi126cA=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

# this part initialize classes for each device
for device in deviceList:
    listSNMPConn[device] = (SNMPConnection(device, deviceList[device], "161", "management"))
    # TODO: See this shit? implement a way to keep multiple database connection like this
    listDBConn[device] = (HandleInfluxDB(bucket, org, token, url))

## Run all kind of
if __name__ == "__main__":
    # print("doing your mom")
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
    # print("\n Testing area")
    # # Local test
    # # localTest = (SNMPConnection("local", "localhost", "161", "public"))
    # notlocalTest = (SNMPConnection("notlocal", "192.168.100.2", "161", "management"))

    # print(notlocalTest.getUDPInNow())
    # all_table = notlocalTest.getIPRouteDest()
    
    # oid_name_table = ["IP ROUTE DESTINATION", "IP ROUTE NEXT HOP", "IP ROUTE TYPE", "IP ROUTE PROTO", "IP ROUTE AGE"]
    # for i in range (5):
    #     print("\n")
    #     for item in all_table[i]:
    #         print(item)
    #print(localTest.getUDPInNow())
    #print(localTest.getBulkTest()
    """
    for i in range(0, 5):
        for j in range(0, 4):
            if(result_table[i][j]):
                print(result_table[i][j], end=" ")
            else:
                pass
    """
    """
    data1 = listSNMPConn["C2960SW"].getBulkTest()
    with open('file.txt', 'w') as f:
    # Define the data to be written
        f.write(data1)
    """
    