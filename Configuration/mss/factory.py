#!/usr/bin/env python
# coding: utf-8
''' This is part of the MSS Python's module.
    Source: https://github.com/BoboTiG/python-mss
'''

from platform import system

from .exception import ScreenshotError


def mss(*args, **kwargs):
    ''' Factory returning a proper MSS class instance.

        It detects the plateform we are running on
        and choose the most adapted mss_class to take
        screenshots.

        It then proxies its arguments to the class for
        instantiation.
    '''

    operating_system = system().lower()
    if operating_system == 'darwin':
        from .darwin import MSS
    elif operating_system == 'linux':
        from .linux import MSS
    elif operating_system == 'windows':
        from .windows import MSS
    else:
        err = 'System "{0}" not implemented.'.format(operating_system)
        raise ScreenshotError(err)

    return MSS(*args, **kwargs)
