CC = /usr/bin/g++

HLCS = /bgsys/drivers/ppcfloor/hlcs
CFLAGS = -c -fPIC -g -Wall -I$(HLCS)/include
LFLAGS = -shared -Wl,-rpath,$(HLCS)/lib -o
LIBS = -L$(HLCS)/lib -lbgsched


LIBNAME=libcorjplugin.so
OBJS=cobalt_runjob_plugin.o

.SUFFIXES: .cpp .o
.cpp.o :
	$(CC) $(CFLAGS) $*.cpp

default: $(OBJS)
	$(CC) $(LFLAGS) $(LIBNAME) $(OBJS) $(LIBS)

clean:
	rm $(OBJS) $(LIBNAME)
