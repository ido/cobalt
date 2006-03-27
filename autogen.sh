#!/bin/sh

autoheader
aclocal-1.8
automake-1.8 -a -c
autoconf
touch config.h.in
