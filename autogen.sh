#!/bin/sh

autoheader
aclocal
automake -a -c
autoconf
touch config.h.in
