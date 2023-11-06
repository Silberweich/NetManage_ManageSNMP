from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import random
import time
# https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/
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
class HandleInfluxDB():
    def __init__(self, bucket, org, token, url):
        self.bucket = bucket
        self.ort = org
        self.token = token
        self.url = url
    
    # TODO: send UDP value to DataBase?
    # type should be UDP in, out.
    # in the db, in and out needs to be on different line of data.
    def sendToDB(value, type) -> bool:
        while True:
    # random number 1.0-100.0
            ran = random.uniform(1.0, 100.0)
    # set time every 30 sec
            time.sleep(30)
    # write data to influxdb
            p = influxdb_client.Point("2").tag("location", "Bangkok").field("temperature", ran)
            write_api.write(bucket=bucket, org=org, record=p)
            print(p)
            return True
    
    # TODO: send UDP value to DataBase
    def getFromDB(value) -> bool:

        return True
    