# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

status = nt_kl.get_status()
if not status:
    resp = '[+] Keylogger is already inactive\n'
else:
    nt_kl.stop()
    status = nt_kl.get_status()
    if not status:
        resp = '[+] Keylogger has been successfully stopped\n'
    else:
        resp = '[!] Keylogger failed to stop\n'

send(client_socket,resp)
