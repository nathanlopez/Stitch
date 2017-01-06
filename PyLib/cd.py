# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os

cd_dir = receive(client_socket)
if os.path.exists(cd_dir):
    if os.path.isdir(cd_dir):
        os.chdir(cd_dir)
        path_name = get_path()
        resp = "Directory change successful"
        send(client_socket, resp)
    else:
        err = "[!] {}: Is not a directory\n".format(cd_dir)
        send(client_socket, err)
else:
    err = "[!] {}: No such directory\n".format(cd_dir)
    send(client_socket,err)
