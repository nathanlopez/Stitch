#!/usr/bin/python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import subprocess,os,sys,shutil

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
    if os.path.exists(pld_exe_path):
        fw_pgm = subprocess.Popen(r'netsh advfirewall firewall delete rule name="{}" program="{}"'.format(key,pld_exe_path),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        fw_pgm_output, errors = fw_pgm.communicate()
        tsk = subprocess.Popen(r'schtasks /delete /tn {}_ST /f'.format(key),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        tsk_output, errors = tsk.communicate()
        shutil.rmtree(pld_path)
