# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import os
import sys
import string
import random
import base64
import logging

banner = '''\
===============================================================

       ...             s      .        s
   .x888888hx    :    :8     @88>     :8              .uef^"
  d88888888888hxx    .88     %8P     .88            :d88E
 8" ... `"*8888%`   :888ooo   .     :888ooo      .  `888E
!  "   ` .xnxx.  -*8888888  .@88u -*8888888 .udR88N  888E .z8k
X X   .H8888888%:   8888   ''888E`  8888   <888'888k 888E~?888L
X 'hn8888888*"   >  8888     888E   8888   9888 'Y"  888E  888E
X: `*88888%`     !  8888     888E   8888   9888      888E  888E
'8h.. ``     ..x8> .8888Lu=  888E  .8888Lu=9888      888E  888E
 `88888888888888f  ^%888*    888&  ^%888*  ?8888u../ 888E  888E
  '%8888888888*"     'Y"     R888"   'Y"    "8888P' m888N= 888>
     ^"****""`                ""              "P'    `Y"   888
                                                          J88"
Version 1.0                                               @%
https://github.com/nathanlopez/Stitch                    :"
===============================================================
'''

st_tag      = "[Stitch]"
st_eof      = base64.b64decode('c3RpdGNoNjI2aGN0aXRz')
st_complete = base64.b64decode('c3RpdGNoLjpjb21wbGV0ZTouY2h0aXRz')

options_fw_osx    = ['status','open','close']
options_fw_win    = ['status','open','close','allow']
options_hostsfile = ['update','remove','show']
options_freeze    = ['status','start','stop']
options_keylogger = ['status','start','stop','dump']

stitch_path        = os.path.dirname(os.path.realpath(sys.argv[0]))
app_path           = os.path.join(stitch_path,'Application')
stitch_vars_path   = os.path.join(app_path,'Stitch_Vars')
pylib_path         = os.path.join(stitch_path,'PyLib')
uploads_path       = os.path.join(stitch_path,'Uploads')
downloads_path     = os.path.join(stitch_path,'Downloads')
payloads_path      = os.path.join(stitch_path,'Payloads')
log_path           = os.path.join(stitch_path,'Logs')
stitch_temp_path   = os.path.join(stitch_path,'Temp')
tools_path         = os.path.join(stitch_path,'Tools')
configuration_path = os.path.join(stitch_path,'Configuration')
elevation_path     = os.path.join(stitch_path,'Elevation')

st_config   = os.path.join(stitch_vars_path,'stitch_config.ini')
hist_ini    = os.path.join(stitch_vars_path,'history.ini')
stitch_log  = os.path.join(log_path,'stitch.log')
st_aes      = os.path.join(stitch_vars_path,'st_aes.py')
st_aes_lib  = os.path.join(stitch_vars_path, 'st_aes_lib.ini')
imgsnp_fld  = os.path.join(tools_path,'ImageSnap-v0.2.5')
imagesnap   = os.path.join(imgsnp_fld, 'imagesnap')

st_paths = [pylib_path,
            uploads_path,
            downloads_path,
            payloads_path,
            log_path,
            stitch_temp_path,
            configuration_path]

for p in st_paths:
    if not os.path.exists(p):
        os.mkdir(p)

if not os.path.exists(st_aes):
    key  = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(32))
    key  = base64.b64encode(key)
    code = '''# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

import base64

aes_encoded = '{}'
aes_abbrev = '{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}'.format(
    aes_encoded[21],aes_encoded[0],aes_encoded[1],aes_encoded[43],aes_encoded[5],
    aes_encoded[13],aes_encoded[7],aes_encoded[24],aes_encoded[31],
    aes_encoded[35],aes_encoded[16],aes_encoded[39],aes_encoded[28])
secret=base64.b64decode(aes_encoded)'''.format(key)

    with open(st_aes,'w') as s:
        s.write(code)

if not os.path.exists(stitch_log):
    with open(stitch_log,'w') as s: pass

st_log = logging.getLogger(stitch_log)
st_log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(stitch_log, 'a')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)
st_log.addHandler(file_handler)
