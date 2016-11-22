# check_keepalived_by_ssh
This is a script for check the role which have an instance of Keepalived through ssh, executing snmpget inside
the target host.

This is based in check-linux-by-ssh by nanpruba:
    https://github.com/naparuba/check-linux-by-ssh

# Requeriments
For this script work, you need: 

- Have installed schekcs.py:

https://github.com/naparuba/check-linux-by-ssh/blob/master/schecks.py

- Have configured SNMP inside the hosts who are running Keepalived, for achievement this, you need do the following:
 
    
