.PHONY: all
CC=gcc
CFLAGS=-Wall -pedantic -D_GNU_SOURCE=1
PROGPREFIX=/usr
PYTHONPATH=

all: wrapper cobalt-admin

wrapper: wrapper.c Makefile
	$(CC) $(CFLAGS) -o wrapper -DPROGPREFIX=\"$(PROGPREFIX)/bin\" -DPYTHONPATH="\"$(PYTHONPATH)\"" wrapper.c

cobalt-admin: wrapper.c Makefile
	$(CC) $(CFLAGS) -o cobalt-admin -DPROGPREFIX=\"$(PROGPREFIX)/sbin\" -DPYTHONPATH="\"$(PYTHONPATH)\"" wrapper.c

clean:
	rm -f cobalt-admin wrapper || true