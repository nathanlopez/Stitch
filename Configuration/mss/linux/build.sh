#!/bin/sh
#
# Build the MSS library for the Python MSS module.
# See https://github.com/BoboTiG/python-mss
#

set -e -u

CC="gcc"
CFLAGS="-s -shared -rdynamic -fPIC -Wall -pedantic -lX11"
ARCH=$(getconf LONG_BIT)

clean() {
	echo "rm -f */libmss.so"
	rm -f */libmss.so
}

build() {
	local arch="$1"

        echo "mkdir -p $arch"
	mkdir -p $arch
	echo "$CC $CFLAGS -m$arch  mss.c -o $arch/libmss.so"
	$CC $CFLAGS -m$arch mss.c -o $arch/libmss.so
}

if [ $ARCH -eq 64 ]; then
	build 64
fi
build 32
