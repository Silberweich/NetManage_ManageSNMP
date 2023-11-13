# Network Management: NMS

This is the repository containing project 5 and 6 for year 4 Network Management class

## Note for Project 6

This is not the finalized version, bucket, org, and credentials information for the database is changed on deployment.

***Documentation provided with the attached PDFs.***

This code would not work without a functioning influxDB database. We plan to incorporate a docker compose at first, but we decided it was too over kill for the job. At first we wanted to run 3 container (python, influxDB, nodeRed), but only influxDB is necessary.  

The project is considered done, and does not need to change :D We could do better, but oh so busy the final month.

Usage for creating docker:

```sh
$ docker run --name influxdb -d \
    -p 8086:8086 \
    --volume /data:/var/lib/influxdb2 \
    --volume /data:/etc/influxdb2/config.yml \
    influxdb:alpine
```

Setup can be done with env, if we are not lazy. As for now the setup needed to be done by hand. The user will set bucket and org as "snmp" and "snmp" respectively. The user will retrieve the token, and type it in the `main.py` file at the correct location.
Then you can just simply:

```sh
$ pip install -r requirement.txt
$ python main.py
```

User may edit the device list as they needed, if there are more devices to add.

**NOTE: If there is an unexpected error please recheck if pyasn1 is at version 0.4.8**  
**NOTE: If you cannot replicate the result, contact the team member. And remember you have seen the system running before.**

## Note for Project 5 (previous project)

the file `cli-main.py` is the original code for Project 5: CLI-based SNMP querying. Usage:

```bash
PS C:\Users\User\NetManage_ManageSNMP> python .\cli-main.py -h
usage: Project 5: simple SNMP browser [-h] [-g] [-n] [-p PORT] [-c COMMUNITY] ip oid

This program contains simple SNMP function: get, get-next

positional arguments:
  ip                    input only ipv4
  oid                   input the oid

options:
  -h, --help            show this help message and exit
  -g, --get             This argument should be activated by default, perform a GET request
  -n, --get-next        use this argument to perform a GET-NEXT request
  -p PORT, --port PORT  in case you need to change SNMP port
  -c COMMUNITY, --community COMMUNITY
                        community string for authorization

Project by Phuthana A. [6388002], Kongkiet K. [6388023], Phichayut N. [6388035], Perakorn N. [6388127] 

## RUNNING BELOW ##

PS C:\Users\User\Desktop\NetManage_ManageSNMP> python .\cli-main.py -c public 127.0.0.1 1.3.6.1.2.1.1.5.0
The IP address 127.0.0.1 is valid, proceeding...
Namespace(get=False, get_next=False, port=161, community="'public'", ip='127.0.0.1', oid='1.3.6.1.2.1.1.5.0')
runnning get on :: 1.3.6.1.2.1.1.5.0 ::
Error Status: 0 ::
   1.3.6.1.2.1.1.5.0 ::
   PC-MacabreLamentation
```
