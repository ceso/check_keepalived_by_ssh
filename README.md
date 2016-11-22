# check_keepalived_by_ssh
This is a script for check the role which have an instance of Keepalived through ssh, executing snmpget inside
the target host.

This is based in check-linux-by-ssh by nanpruba:
    https://github.com/naparuba/check-linux-by-ssh

# Requeriments
For this script work, you need: 

- Have schekcs.py:

https://github.com/naparuba/check-linux-by-ssh/blob/master/schecks.py

- Have configured SNMP inside the host/s is running Keepalived. For achievement this, you need to have the following inside /etc/snmp/snmpd.conf:


    rocommunity public
    
    master agentx

 
    
