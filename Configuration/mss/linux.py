#!/usr/bin/env python
# coding: utf-8
''' This is part of the MSS Python's module.
    Source: https://github.com/BoboTiG/python-mss
'''

from ctypes import (
    POINTER, Structure, byref, c_char_p, c_int, c_int32, c_long, c_uint,
    c_uint32, c_ulong, c_ushort, c_void_p, cast, cdll, create_string_buffer)
from ctypes.util import find_library
from os import environ
from os.path import abspath, dirname, isfile, realpath
from struct import pack
from sys import maxsize, version

from .base import MSSBase
from .exception import ScreenshotError

__all__ = ['MSS']


class Display(Structure):
    ''' Structure that serves as the connection to the X server
        and that contains all the information about that X server.
    '''


class XWindowAttributes(Structure):
    ''' Attributes for the specified window. '''

    _fields_ = [('x', c_int32), ('y', c_int32), ('width', c_int32),
                ('height', c_int32), ('border_width', c_int32),
                ('depth', c_int32), ('visual', c_ulong), ('root', c_ulong),
                ('class', c_int32), ('bit_gravity', c_int32),
                ('win_gravity', c_int32), ('backing_store', c_int32),
                ('backing_planes', c_ulong), ('backing_pixel', c_ulong),
                ('save_under', c_int32), ('colourmap', c_ulong),
                ('mapinstalled', c_uint32), ('map_state', c_uint32),
                ('all_event_masks', c_ulong), ('your_event_mask', c_ulong),
                ('do_not_propagate_mask', c_ulong),
                ('override_redirect', c_int32), ('screen', c_ulong)]


class XImage(Structure):
    ''' Description of an image as it exists in the client's memory.
        https://tronche.com/gui/x/xlib/graphics/images.html
    '''

    _fields_ = [('width', c_int), ('height', c_int), ('xoffset', c_int),
                ('format', c_int), ('data', c_void_p),
                ('byte_order', c_int), ('bitmap_unit', c_int),
                ('bitmap_bit_order', c_int), ('bitmap_pad', c_int),
                ('depth', c_int), ('bytes_per_line', c_int),
                ('bits_per_pixel', c_int), ('red_mask', c_ulong),
                ('green_mask', c_ulong), ('blue_mask', c_ulong)]


class XRRModeInfo(Structure):
    ''' Voilà, voilà. '''


class XRRScreenResources(Structure):
    ''' Structure that contains arrays of XIDs that point to the
        available outputs and associated CRTCs.
    '''

    _fields_ = [('timestamp', c_ulong), ('configTimestamp', c_ulong),
                ('ncrtc', c_int), ('crtcs', POINTER(c_long)),
                ('noutput', c_int), ('outputs', POINTER(c_long)),
                ('nmode', c_int), ('modes', POINTER(XRRModeInfo))]


class XRRCrtcInfo(Structure):
    ''' Structure that contains CRTC informations. '''

    _fields_ = [('timestamp', c_ulong), ('x', c_int), ('y', c_int),
                ('width', c_int), ('height', c_int), ('mode', c_long),
                ('rotation', c_int), ('noutput', c_int),
                ('outputs', POINTER(c_long)), ('rotations', c_ushort),
                ('npossible', c_int), ('possible', POINTER(c_long))]


class MSS(MSSBase):
    ''' Mutliple ScreenShots implementation for GNU/Linux.
        It uses intensively the Xlib and Xrandr extension.
    '''

    # pylint: disable=too-many-instance-attributes

    display = None
    use_mss = False
    mss = None
    xlib = None
    xrandr = None
    display = None
    root = None

    def __del__(self):
        ''' Disconnect from X server. '''

        if self.display:
            self.xlib.XCloseDisplay(self.display)
            self.display = None

    def __init__(self, display=None):
        ''' GNU/Linux initialisations. '''

        if not display:
            try:
                if version > '3':
                    display = bytes(environ['DISPLAY'], 'utf-8')
                else:
                    display = environ['DISPLAY']
            except KeyError:
                err = '$DISPLAY not set. Stopping to prevent segfault.'
                raise ScreenshotError(err)

        x11 = find_library('X11')
        if not x11:
            raise ScreenshotError('No X11 library found.')
        self.xlib = cdll.LoadLibrary(x11)

        xrandr = find_library('Xrandr')
        if not xrandr:
            raise ScreenshotError('No Xrandr extension found.')
        self.xrandr = cdll.LoadLibrary(xrandr)

        # libmss = find_library('mss')
        libmss = '{0}/linux/{1}/libmss.so'.format(
            dirname(realpath(abspath(__file__))), arch())
        if isfile(libmss):
            self.mss = cdll.LoadLibrary(libmss)
            self.use_mss = True
        else:
            print('No MSS library found. Using slow native function.')

        self._set_argtypes()
        self._set_restypes()

        self.display = self.xlib.XOpenDisplay(display)
        try:
            assert self.display.contents
        except ValueError:
            raise ScreenshotError('Cannot open display "{0}".'.format(display))
        screen = self.xlib.XDefaultScreen(self.display)
        self.root = self.xlib.XDefaultRootWindow(self.display, screen)

    def _set_argtypes(self):
        ''' Functions arguments.

            Curiously, if we set up XGetPixel arguments type,
            the entire process takes twice more time.
            So, no need to waste this precious time :)
            Note: this issue does not occur when using libmss.
        '''

        self.xlib.XOpenDisplay.argtypes = [c_char_p]
        self.xlib.XDefaultScreen.argtypes = [POINTER(Display)]
        self.xlib.XDefaultRootWindow.argtypes = [POINTER(Display), c_int]
        self.xlib.XGetWindowAttributes.argtypes = [POINTER(Display),
                                                   POINTER(XWindowAttributes),
                                                   POINTER(XWindowAttributes)]
        self.xlib.XAllPlanes.argtypes = []
        self.xlib.XGetImage.argtypes = [POINTER(Display), POINTER(Display),
                                        c_int, c_int, c_uint, c_uint, c_ulong,
                                        c_int]
        # self.xlib.XGetPixel.argtypes = [POINTER(XImage), c_int, c_int]
        self.xlib.XDestroyImage.argtypes = [POINTER(XImage)]
        self.xlib.XCloseDisplay.argtypes = [POINTER(Display)]
        self.xrandr.XRRGetScreenResources.argtypes = [POINTER(Display),
                                                      POINTER(Display)]
        self.xrandr.XRRGetCrtcInfo.argtypes = [POINTER(Display),
                                               POINTER(XRRScreenResources),
                                               c_long]
        self.xrandr.XRRFreeScreenResources.argtypes = \
            [POINTER(XRRScreenResources)]
        self.xrandr.XRRFreeCrtcInfo.argtypes = [POINTER(XRRCrtcInfo)]
        if self.use_mss:
            self.mss.GetXImagePixels.argtypes = [POINTER(XImage), c_void_p]

    def _set_restypes(self):
        ''' Functions return type. '''

        def validate(value):
            ''' Validate the returned value of xrandr.XRRGetScreenResources().
                We can end on a segfault if not:
                    Xlib:  extension "RANDR" missing on display "...".
            '''

            if value == 0:
                err = 'xrandr.XRRGetScreenResources() failed.'
                err += ' NULL pointer received.'
                raise ScreenshotError(err)

            return cast(value, POINTER(XRRScreenResources))

        self.xlib.XOpenDisplay.restype = POINTER(Display)
        self.xlib.XDefaultScreen.restype = c_int
        self.xlib.XGetWindowAttributes.restype = c_int
        self.xlib.XAllPlanes.restype = c_ulong
        self.xlib.XGetImage.restype = POINTER(XImage)
        self.xlib.XGetPixel.restype = c_ulong
        self.xlib.XDestroyImage.restype = c_void_p
        self.xlib.XCloseDisplay.restype = c_void_p
        self.xlib.XDefaultRootWindow.restype = POINTER(XWindowAttributes)
        self.xrandr.XRRGetScreenResources.restype = validate
        self.xrandr.XRRGetCrtcInfo.restype = POINTER(XRRCrtcInfo)
        self.xrandr.XRRFreeScreenResources.restype = c_void_p
        self.xrandr.XRRFreeCrtcInfo.restype = c_void_p
        if self.use_mss:
            self.mss.GetXImagePixels.restype = c_int

    def enum_display_monitors(self, force=False):
        ''' Get positions of monitors (see parent class). '''

        if not self.monitors or force:
            self.monitors = []

            # All monitors
            gwa = XWindowAttributes()
            self.xlib.XGetWindowAttributes(self.display, self.root, byref(gwa))
            self.monitors.append({
                'left': int(gwa.x),
                'top': int(gwa.y),
                'width': int(gwa.width),
                'height': int(gwa.height),
                'monitor': 0
            })

            # Each monitors
            # Fix for XRRGetScreenResources:
            #     expected LP_Display instance instead of LP_XWindowAttributes
            root = cast(self.root, POINTER(Display))
            mon = self.xrandr.XRRGetScreenResources(self.display, root)
            for num in range(mon.contents.ncrtc):
                crtc = self.xrandr.XRRGetCrtcInfo(self.display, mon,
                                                  mon.contents.crtcs[num])
                self.monitors.append({
                    'left': int(crtc.contents.x),
                    'top': int(crtc.contents.y),
                    'width': int(crtc.contents.width),
                    'height': int(crtc.contents.height),
                    'monitor': num
                })
                self.xrandr.XRRFreeCrtcInfo(crtc)
            self.xrandr.XRRFreeScreenResources(mon)

        return self.monitors

    def get_pixels(self, monitor):
        ''' Retrieve all pixels from a monitor. Pixels have to be RGB. '''

        self.width = monitor['width']
        self.height = monitor['height']
        left, top = monitor['left'], monitor['top']
        zpixmap = 2
        allplanes = self.xlib.XAllPlanes()

        # Fix for XGetImage:
        #     expected LP_Display instance instead of LP_XWindowAttributes
        root = cast(self.root, POINTER(Display))
        ximage = self.xlib.XGetImage(self.display, root, left, top,
                                     self.width, self.height, allplanes,
                                     zpixmap)
        if not ximage:
            err = 'xlib.XGetImage() failed. Monitor informations: '
            for key, val in sorted(monitor.items()):
                err = '{0}{1}: {2}, '.format(err, key, val)
            err = err.strip(', ')
            raise ScreenshotError(err)

        if not self.use_mss:
            self.get_pixels_slow(ximage)
        else:
            self.image = create_string_buffer(self.height * self.width * 3)
            ret = self.mss.GetXImagePixels(ximage, self.image)
            if not ret:
                self.xlib.XDestroyImage(ximage)
                err = 'libmss.GetXImagePixels() failed (retcode={0}).'
                raise ScreenshotError(err.format(ret))
        self.xlib.XDestroyImage(ximage)
        return self.image

    def get_pixels_slow(self, ximage):
        ''' Retrieve all pixels from a monitor. Pixels have to be RGB.
            (!) Insanely slow version, see doc/linux-slow-version. (!)
        '''

        # @TODO: this part takes most of the time. Need a better solution.
        def pix(pixel, _resultats={}, p__=pack):
            ''' Apply shifts to a pixel to get the RGB values.
                This method uses of memoization.
            '''

            # pylint: disable=dangerous-default-value

            if pixel not in _resultats:
                _resultats[pixel] = p__('<B', (pixel & rmask) >> 16) + \
                    p__('<B', (pixel & gmask) >> 8) + \
                    p__('<B', pixel & bmask)
            return _resultats[pixel]

        self.width = ximage.contents.width
        self.height = ximage.contents.height
        rmask = ximage.contents.red_mask
        bmask = ximage.contents.blue_mask
        gmask = ximage.contents.green_mask
        get_pix = self.xlib.XGetPixel
        pixels = [pix(get_pix(ximage, x, y))
                  for y in range(self.height) for x in range(self.width)]
        self.image = b''.join(pixels)
        return self.image


def arch():
    ''' Detect OS architecture.
        Returns an int: 32 or 64
    '''

    return 64 if maxsize > 2 ** 32 else 32
