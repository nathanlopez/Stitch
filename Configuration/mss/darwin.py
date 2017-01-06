#!/usr/bin/env python
# coding: utf-8
''' This is part of the MSS Python's module.
    Source: https://github.com/BoboTiG/python-mss
'''

# pylint: disable=import-error

from ctypes import (
    POINTER, Structure, byref, c_double, c_float, c_int32, c_ubyte, c_uint32,
    c_void_p, cast, cdll)
from ctypes.util import find_library
from sys import maxsize

from .base import MSSBase
from .exception import ScreenshotError

__all__ = ['MSS']


def cgfloat():
    ''' Get the appropriate value for a float. '''

    return c_double if maxsize > 2 ** 32 else c_float


def get_infinity(maxi=False):
    ''' Get infinity "numbers". '''

    return 1.7976931348623157e+308 if maxi else -8.988465674311579e+307


class CGPoint(Structure):
    ''' Structure that contains coordinates of a rectangle. '''

    _fields_ = [('x', cgfloat()), ('y', cgfloat())]


class CGSize(Structure):
    ''' Structure that contains dimensions of an rectangle. '''

    _fields_ = [('width', cgfloat()), ('height', cgfloat())]


class CGRect(Structure):
    ''' Structure that contains informations about a rectangle. '''

    _fields_ = [('origin', CGPoint), ('size', CGSize)]


class MSS(MSSBase):
    ''' Mutliple ScreenShots implementation for MacOS X.
        It uses intensively the Quartz.
    '''

    max_displays = 32  # Could be augmented, if needed ...

    def __init__(self):
        ''' MacOS X initialisations. '''

        coregraphics = find_library('CoreGraphics')
        if not coregraphics:
            raise ScreenshotError('No CoreGraphics library found.')
        self.core = cdll.LoadLibrary(coregraphics)

        self._set_argtypes()
        self._set_restypes()

    def _set_argtypes(self):
        ''' Functions arguments. '''

        self.core.CGGetActiveDisplayList.argtypes = \
            [c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
        self.core.CGDisplayBounds.argtypes = [c_uint32]
        self.core.CGRectStandardize.argtypes = [CGRect]
        self.core.CGDisplayRotation.argtypes = [c_uint32]
        self.core.CGWindowListCreateImage.argtypes = \
            [CGRect, c_uint32, c_uint32, c_uint32]
        self.core.CGImageGetWidth.argtypes = [c_void_p]
        self.core.CGImageGetHeight.argtypes = [c_void_p]
        self.core.CGImageGetDataProvider.argtypes = [c_void_p]
        self.core.CGDataProviderCopyData.argtypes = [c_void_p]
        self.core.CFDataGetBytePtr.argtypes = [c_void_p]
        self.core.CGDataProviderRelease.argtypes = [c_void_p]

    def _set_restypes(self):
        ''' Functions return type. '''

        self.core.CGGetActiveDisplayList.restype = c_int32
        self.core.CGDisplayBounds.restype = CGRect
        self.core.CGRectStandardize.restype = CGRect
        self.core.CGDisplayRotation.restype = c_float
        self.core.CGWindowListCreateImage.restype = c_void_p
        self.core.CGImageGetWidth.restype = c_uint32
        self.core.CGImageGetHeight.restype = c_uint32
        self.core.CGImageGetDataProvider.restype = c_void_p
        self.core.CGDataProviderCopyData.restype = c_void_p
        self.core.CFDataGetBytePtr.restype = c_void_p
        self.core.CGDataProviderRelease.restype = c_void_p

    def enum_display_monitors(self, force=False):
        ''' Get positions of monitors (see parent class). '''

        if not self.monitors or force:
            self.monitors = []

            # All monitors
            self.monitors.append({
                'left': int(get_infinity()),
                'top': int(get_infinity()),
                'width': int(get_infinity(True)),
                'height': int(get_infinity(True))
            })

            # Each monitors
            display_count = c_uint32(0)
            active_displays = (c_uint32 * self.max_displays)()
            self.core.CGGetActiveDisplayList(self.max_displays,
                                             active_displays,
                                             byref(display_count))
            rotations = {0.0: 'normal', 90.0: 'right', -90.0: 'left'}
            for idx in range(display_count.value):
                display = active_displays[idx]

                rect = self.core.CGDisplayBounds(display)
                rect = self.core.CGRectStandardize(rect)
                left, top = rect.origin.x, rect.origin.y
                width, height = rect.size.width, rect.size.height
                rot = self.core.CGDisplayRotation(display)
                if rotations[rot] in ['left', 'right']:
                    width, height = height, width
                self.monitors.append({
                    'left': int(left),
                    'top': int(top),
                    'width': int(width),
                    'height': int(height)
                })

        return self.monitors

    def get_pixels(self, monitor):
        ''' Retrieve all pixels from a monitor. Pixels have to be RGB. '''

        width, height = monitor['width'], monitor['height']
        left, top = monitor['left'], monitor['top']
        rect = CGRect((left, top), (width, height))

        image_ref = self.core.CGWindowListCreateImage(rect, 1, 0, 0)
        if not image_ref:
            err = 'CoreGraphics.CGWindowListCreateImage() failed.'
            raise ScreenshotError(err)

        self.width = int(self.core.CGImageGetWidth(image_ref))
        self.height = int(self.core.CGImageGetHeight(image_ref))
        prov = self.core.CGImageGetDataProvider(image_ref)
        data = self.core.CGDataProviderCopyData(prov)
        data_ref = self.core.CFDataGetBytePtr(data)
        buf_len = self.height * self.width * 4  # or CFDataGetLength()
        data = cast(data_ref, POINTER(c_ubyte * buf_len))
        self.core.CGDataProviderRelease(prov)

        # Replace pixels values: BGRA to RGB.
        image_data = bytearray(data.contents)
        image = bytearray(self.height * self.width * 3)
        image[0::3], image[1::3], image[2::3] = \
            image_data[2::4], image_data[1::4], image_data[0::4]
        self.image = bytes(image)
        return self.image
