#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    This script is a check of for known the role which have
    a instance of keepalived
'''
import os
import sys
import optparse

# try load the directory where iam for load the plugin utils
myDir = os.path.dirname(__file__)
sys.path.insert(0, myDir)

try:
    import schecks
except ImportError:
    print("ERROR: This plugin needs the local schecks.py lib. Please install it")
    sys.exit(2)

version = "0.1"
# There is no Warning, only critical
defaultWarning = None
defaultCritical = "backup"

def getRoleKa(client):
    # We're looking for a line like this:
    # KEEPALIVED-MIB::vrrpInstanceState.1 = INTEGER: master(2)
    cmdGetRole = r""" /usr/bin/snmpget -v2c -cpublic localhost KEEPALIVED-MIB::vrrpInstanceState.1 """
    #print(client.exec_command(cmdGetRole))
    stdin, stdout, stderr = client.exec_command(cmdGetRole)
    # parse the stoutput, and store the current role of ka
    currentRole = [l for l in stdout][0].strip().split(' ')[-1].rstrip('\n').split('(')[0]

    # before return, close the connection
    client.close()

    return currentRole

parser = optparse.OptionParser(
    "%prog [options]", version="%prog " + version)
parser.add_option("-H", "--hostname",
    dest="hostname",
    metavar="hostname",
    help="Hostname to connect to.")
parser.add_option("-p", "--port",
    dest="port", type="int", default=22,
    metavar="port",
    help="SSH port to connect to. Default: 22")
parser.add_option("-i", "--ssh-key",
    dest="sshKeyFile",
    metavar="sshKeyFile",
    help="SSH key file to use. By default will take ~/.ssh/id_rsa.")
parser.add_option("-u", "--user",
    dest="user",
    metavar="user",
    help="Remote user to use. By default shinken")
parser.add_option("-P", "--passphrase",
    dest="passPhrase",
    metavar="passPhrase",
    help="SSH key passphrase. By default will use void.")
parser.add_option("-e", "--expected-state",
    dest="kaExpectedState",
    metavar="kaExpectedState",
    help="The expected state which Keepalived shall return. By default will be master")
parser.add_option("-c", "--critical",
    dest="critical",
    metavar="critical",
    help="Critical value for the instance of keepalived. By default will be backup")

if __name__ == '__main__':
    # first parse arguments
    opts, args = parser.parse_args()
    if args:
        parser.error("Does not accept any argument.")

    hostname = opts.hostname or ""
    port = opts.port
    sshKeyFile = opts.sshKeyFile or os.path.expanduser("~/.ssh/id_rsa")
    user = opts.user or "shinken"
    passPhrase = opts.passPhrase or ""
    kaExpectedState = opts.kaExpectedState or "master"
    critical = opts.critical or defaultCritical

    # now, connect to the target and try to get the values
    client = schecks.connect(hostname, port, sshKeyFile, passPhrase, user)
    kaCurrentRole = getRoleKa(client)

    if kaCurrentRole == critical:
        print("Critical: expected role was {}, but the current is {}.".format(kaExpectedState, kaCurrentRole))
        sys.exit(2)
    elif kaCurrentRole == "fault":
        print("KA is in fault state.")
        sys.exit(2)
    elif kaCurrentRole == kaExpectedState:
        print("OK: the expected role was {}, and the current is {}.".format(kaExpectedState, kaCurrentRole))
        sys.exit(0)
    else:
        print("Unknown: SNMP or KA isn't running and I can't get the current role.")
        sys.exit(3)
