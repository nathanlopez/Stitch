# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

f_name = receive(client_socket)
system = sys.platform
if os.path.exists(f_name):
    if win_client():
        resp = run_command("attrib -H {}".format(f_name))
    if osx_client():
        resp = run_command("chflags nohidden {}".format(f_name))
    if lnx_client() and not f_name.startswith('.'):
        resp = '[*] File is already unhidden.\n'
    elif lnx_client():
        resp = run_command("mv {} {}".format(f_name,f_name[1:]))
else:
    if lnx_client() and f_name.startswith('.'):
        if os.path.exists(f_name[1:]):
            resp = '[*] File is already unhidden.\n'
    else:
        resp = "[!] {}: No such file or directory\n".format(f_name)
send(client_socket,resp)
