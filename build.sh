#!/bin/sh -e

autoconf
aclocal
libtoolize --force
automake --add-missing
autoreconf
./configure
make
