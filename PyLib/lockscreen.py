# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import ctypes

if win_client():
    success = "[+] Command successfully executed.\n"
    ctypes.windll.user32.LockWorkStation()
    send(client_socket,success)
if osx_client():
    resp=run_command('/System/Library/CoreServices/"Menu Extras"/User.menu/Contents/Resources/CGSession -suspend')
    send(client_socket,resp)
if lnx_client():
    resp=run_command('vlock -a -s')
    send(client_socket,resp)
