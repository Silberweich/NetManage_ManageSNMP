from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import random
import time
# https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/
bucket = "jeen"
org = "jeen"
token = "44KDRmqUmCSc6g5aRsL5nHXqxuVQGlmMQycnWkX4me3J6-QMbjXYaGMabYpSq5XvXxDPz_2gD7MCwS8WLfV3Hg=="
# Store the URL of your InfluxDB instance
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)


class HandleInfluxDB():
    def __init__(self, bucket, org, token, url):
        self.bucket = bucket
        self.org = org
        self.token = token
        self.url = url

    # TODO: send UDP value to DataBase?
    # type should be UDP in, out.
    # in the db, in and out needs to be on different line of data.
    def sendToDBudp(self, Devicename, UDPin, UDPout) -> bool:
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("UDPin", UDPin)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("UDPout", UDPout)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        return True

    def sendToDBiproute(self, Devicename, Iproutetable) -> bool:
        p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("Iproutetable", Iproutetable)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        return True

    def sendToDBsystemdesc(self, Devicename, Systemdesc) -> bool:
        # data should be in list
        """
        test = [
                ["test1","test2","test3","test4","test5"],
                ["testo1","testo2","testo3","testo4","testo5"],
                ["testoo1","testoo2","testoo3","testoo4","testoo5"]
                ]
        """
        length = len(Systemdesc)
        for i in range(0,length):
            p = influxdb_client.Point(Devicename).tag(
            "IP", Devicename).field("Systemdesc", Systemdesc[i])
            write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        return True
