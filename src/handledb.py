from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import random
import time
# # https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/
# bucket = "jeen"
# org = "jeen"
# token = "44KDRmqUmCSc6g5aRsL5nHXqxuVQGlmMQycnWkX4me3J6-QMbjXYaGMabYpSq5XvXxDPz_2gD7MCwS8WLfV3Hg=="
# # Store the URL of your InfluxDB instance
# url="http://localhost:8086"
# client = influxdb_client.InfluxDBClient(
#    url=url,
#    token=token,
#    org=org
# )
# # Write script
# write_api = client.write_api(write_options=SYNCHRONOUS)
class HandleInfluxDB():
    def __init__(self, bucket, org, token, url):
        self.bucket = bucket
        self.org = org
        self.token = token
        self.url = url
        self.write_api = influxdb_client.InfluxDBClient(write_options=SYNCHRONOUS)
    
    # TODO: send UDP value to DataBase?
    # type should be UDP in, out.
    # in the db, in and out needs to be on different line of data.
    def sendToDBudp(self, Devicename, UDPin, UDPout) -> bool:
        p = influxdb_client.Point(Devicename).tag("IP", Devicename).field("UDPin", UDPin)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        p = influxdb_client.Point(Devicename).tag("IP", Devicename).field("UDPout", UDPout)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        return True
    def sendToDBiproutesystem(self, Devicename, Iproutetable, Systemdesc) -> bool:
        p = influxdb_client.Point(Devicename).tag("IP", Devicename).field("Iproutetable", Iproutetable)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        p = influxdb_client.Point(Devicename).tag("IP", Devicename).field("Systemdesc", Systemdesc)
        write_api.write(bucket=bucket, org=org, record=p)
        print(p)
        return True
    