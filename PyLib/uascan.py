# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import _winreg
import subprocess

def check_uac():
    uac_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
    val=_winreg.QueryValueEx(uac_key, "EnableLUA")
    if val[0] == 1:
        return "\nUAC is Enabled"
    else:
        return "\nUAC is Disabled"

print check_uac()
