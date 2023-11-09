from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import random
import time

class HandleInfluxDB():
    def __init__(self, bucket, org, token, url):
        self.bucket = bucket
        self.org = org
        self.token = token
        self.url = url
        self.write_api =  influxdb_client.InfluxDBClient(
                        url= self.url,
                        token= self.token,
                        org= self.org
                    ).write_api(write_options=SYNCHRONOUS)

    # TODO: send UDP value to DataBase?
    # type should be UDP in, out.
    # in the db, in and out needs to be on different line of data.
    def sendToDBudp(self, Devicename, UDPin, UDPout) -> bool:
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("UDPin", UDPin)
        
        self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        #print(p)
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("UDPout", UDPout)
        
        self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        
        # print(p)
        return True

    def sendToDBsystemDesc(self, Devicename, Iproutetable) -> bool:
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("systemDescription", Iproutetable)
        
        self.write_api.write(bucket=self.bucket, org=self.org, record=p)

        # print(p)
        return True

    def sendToDBIPRouteTable(self, Devicename, Systemdesc) -> bool:
        # data should be in list
        """
        test = [
                ["test1","test2","test3","test4","test5"],
                ["testo1","testo2","testo3","testo4","testo5"],
                ["testoo1","testoo2","testoo3","testoo4","testoo5"]
                ]
        """
        length = len(Systemdesc)
        for i in Systemdesc:
            p = influxdb_client.Point(Devicename).tag(
                "IP", Devicename).field("IP Route Table", str(i))
            self.write_api.write(bucket=self.bucket, org=self.org, record=p)
        # print(p)
        return True
