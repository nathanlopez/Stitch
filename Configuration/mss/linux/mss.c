/*
 * This is part of the MSS Python's module.
 * This will be compiled into libmss.so and then
 * you can call it from ctypes.
 *
 * See MSSLinux:get_pixels() for a real world example.
 *
 * Source: https://github.com/BoboTiG/python-mss
 */

#include <X11/Xlib.h>
#include <X11/Xutil.h>  /* For XGetPixel prototype */

int GetXImagePixels(XImage *ximage, unsigned char *pixels) {
    unsigned int x, y, offset;
    unsigned long pixel;

    if ( !ximage ) {
        return -1;
    }
    if ( !pixels ) {
        return 0;
    }

    for ( x = 0; x < ximage->width; ++x ) {
        for ( y = 0; y < ximage->height; ++y ) {
            offset =  x * 3 + ximage->width * y * 3;
            pixel = XGetPixel(ximage, x, y);
            pixels[offset]     = (pixel & ximage->red_mask) >> 16;
            pixels[offset + 1] = (pixel & ximage->green_mask) >> 8;
            pixels[offset + 2] =  pixel & ximage->blue_mask;
        }
    }
    return 1;
}
