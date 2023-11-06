import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time
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


while True:
    # random number 1.0-100.0
    ran = random.uniform(1.0, 100.0)
    # set time every 30 sec
    time.sleep(30)
    # write data to influxdb
    p = influxdb_client.Point("2").tag("location", "Bangkok").field("temperature", ran)
    write_api.write(bucket=bucket, org=org, record=p)
    print(p)