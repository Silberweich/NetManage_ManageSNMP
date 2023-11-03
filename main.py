import argparse
import ipaddress
from pysnmp import hlapi 
from pysnmp.entity.rfc3413.oneliner import cmdgen

# some resources
# https://pysnmp.readthedocs.io/en/latest/docs/pysnmp-hlapi-tutorial.html
# DEPENDENCIES: pyasn1==0.4.8 only 0.5.0 WILL NOT WORK AND CAUSE ERROR

##### Initialize program with parser #####
parser = argparse.ArgumentParser(
    prog = "Project 5: simple SNMP browser",
    description = "This program contains simple SNMP function: get, get-next",
    epilog = """
    Project by 
    Phuthana A. [6388002],
    Kongkiet K. [6388023],
    Phichayut N. [6388035],
    Perakorn N. [6388127]
    """
)

# make this a default argument
parser.add_argument("-g", 
                    "--get", 
                    action= "store_true",
                    help = "This argument should be activated by default, perform a GET request")
parser.add_argument("-n", 
                    "--get-next", 
                    action = "store_true",
                    help = "use this argument to perform a GET-NEXT request")
parser.add_argument("-p", 
                    "--port", 
                    action = "store", 
                    default = 161, 
                    type = int,
                    help = "in case you need to change SNMP port")
parser.add_argument("-c",
                    "--community",
                    action = "store",
                    default = "public",
                    type = ascii,
                    help = "community string for authorization")
parser.add_argument("ip",
                    help = "input only ipv4")
parser.add_argument("oid",
                    help = "input the oid")

args = parser.parse_args()
##### END OF PARSER INITIALIZATION #####

##### Functions #####

# make sure that flag -gn will not work. 
check_request_type = lambda g, n: not (g and n)

def initCheck(ip: str, oid:str, g: bool, n: bool) -> bool:
    try:
        ipaddress.ip_address(ip)
        print("The IP address", ip, "is valid, proceeding...")
    except ValueError:
        print("The IP address", ip, "is not valid, EXITING.")
        exit()
    
    if not check_request_type(g, n):
        print("please pick one of the option (-g, -n), not both, EXITING")
        exit()

    return True

# 1.3.6.1.2.1.1.5.0 "management"
def getSNMP(ip, port, oid, community):
    auth = cmdgen.CommunityData(community.replace('"', '').replace("'", ""))

    cmdGen = cmdgen.CommandGenerator()
    
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((ip, port)),
    cmdgen.MibVariable(oid),
    lookupMib=False,
    )

    if errorIndication:
        print(errorStatus, errorIndication, errorIndex, "error")
        exit()
    
    for oid, val in varBinds:
        print("Error Status:", errorStatus, "::\n  ", oid.prettyPrint(), "::\n  ", val.prettyPrint())


def getNextSNMP(ip, port, oid, community):
    auth = cmdgen.CommunityData(community.replace('"', '').replace("'", ""))

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
    auth,
    cmdgen.UdpTransportTarget((ip, port)),
    cmdgen.MibVariable(oid),
    lookupMib=False,
    )

    if errorIndication:
        print(errorStatus, errorIndication, errorIndex, "error")
        exit()
    
    print(varBinds)

    for i in varBinds:
        for j in i:
            for k in j:
                print(k)

    # for oid, val in varBinds:
    #     print("Error Status:", errorStatus, "::\n  ", oid.prettyPrint(), "::\n  ", val.prettyPrint())
    # print("func 4")

##### End of Functions#####

if __name__ == '__main__':
    initCheck(args.ip, args.oid, args.get, args.get_next)
    # debug
    print(args)

    # start
    if not args.get and not args.get_next:
        print("runnning get on ::", args.oid, "::")
        getSNMP(args.ip, args.port, args.oid, args.community)
    elif args.get_next:
        print("runnning get next on ", args.oid, "::")
        getNextSNMP(args.ip, args.port, args.oid, args.community)
    else:
        print("runnning get on ::", args.oid, "::")
        getSNMP(args.ip, args.port, args.oid, args.community)
