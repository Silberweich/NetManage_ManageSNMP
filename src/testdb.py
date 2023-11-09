import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time
bucket = "jeen"
org = "jeen"
token = "44KDRmqUmCSc6g5aRsL5nHXqxuVQGlmMQycnWkX4me3J6-QMbjXYaGMabYpSq5XvXxDPz_2gD7MCwS8WLfV3Hg=="
test = [["test1","test2","test3","test4","test5"],
        ["testo1","testo2","testo3","testo4","testo5"],
        ["testoo1","testoo2","testoo3","testoo4","testoo5"]]
# Store the URL of your InfluxDB instance
url="http://localhost:8086"
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)
test = [["test1","test2","test3","test4","test5"],
        ["testo1","testo2","testo3","testo4","testo5"],
        ["testoo1","testoo2","testoo3","testoo4","testoo5"]]
i=0
while True:
    # random number 1.0-100.0
    ran = random.uniform(1.0, 100.0)
    # set time every 30 sec
    time.sleep(2)
    # write data to influxdb
    if(i>=3):
       break
    #print(test[i])
    p = influxdb_client.Point("testarray").tag("help", "dog").field("array", str(test[i]))
    i+=1
    write_api.write(bucket=bucket, org=org, record=p)
    print(p)