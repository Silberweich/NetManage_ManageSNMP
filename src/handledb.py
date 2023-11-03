import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/

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

        return True
    
    # TODO: send UDP value to DataBase
    def getFromDB(value) -> bool:

        return True
    