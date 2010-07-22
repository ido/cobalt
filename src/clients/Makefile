.PHONY: all
CC=gcc
CFLAGS=-Wall -pedantic -D_GNU_SOURCE=1
PROGPREFIX=/usr

all: wrapper cobalt-admin

wrapper: wrapper.c Makefile
	$(CC) $(CFLAGS) -o wrapper -DPROGPREFIX=\"$(PROGPREFIX)/bin\" wrapper.c

cobalt-admin: wrapper.c Makefile
	$(CC) $(CFLAGS) -o cobalt-admin -DPROGPREFIX=\"$(PROGPREFIX)/sbin\" wrapper.c

clean:
	rm -f cobalt-admin wrapper || true