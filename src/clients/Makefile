.PHONY: all
CC=gcc
CFLAGS=-Wall -pedantic -D_GNU_SOURCE=1
PROGPREFIX=/usr

wrapper: wrapper.c Makefile
	$(CC) $(CFLAGS) -o wrapper -DPROGPREFIX=\"$(PROGPREFIX)/bin\" wrapper.c

clean:
	rm -f wrapper || true