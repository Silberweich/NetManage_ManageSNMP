



if __name__ == "__main__":
    ip = "10.99.1.2"
    port = 161
    oid = "1.3.6.1.2.1.7.4.0"
    strCommunity = "management"
    for i in range(1, 100):
        getSNMP(ip, port, oid, strCommunity)