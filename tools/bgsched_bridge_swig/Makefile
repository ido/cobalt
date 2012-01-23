#Makefile for python bindings for SWIG


CC = /usr/bin/g++
SWIG = /home/richp/swig/bin/swig 

MODULE = pybgsched

SWIGFLAGS = -python -c++
INTERFACE_FILE = $(MODULE).i

PYTHON_INCLUDE = /usr/include/python2.6
PYTHON_WRAPPER = $(MODULE).py

HLCS = /bgsys/drivers/ppcfloor/hlcs
CFLAGS = -Wall -c -fPIC -g -Wall -I$(HLCS)/include -I$(PYTHON_INCLUDE)
LFLAGS = -Wall -shared -fPIC -Wl,-rpath,$(HLCS)/lib -o
LIBS = -L$(HLCS)/lib -lbgsched


LIBNAME = _$(MODULE).so
OBJS = $(MODULE)_wrap.o

.SUFFIXES: .cpp .cxx .o .i
.cpp.o :
	$(CC) $(CFLAGS) $(wildcard *.cpp)

#SWIG likes to make these.
.cxx.o :
	$(CC) $(CFLAGS) $(wildcard *.cxx)

all: $(PYTHON_WRAPPER) $(LIBNAME)
.PHONY: all

#Make for SWIG.  This works a little differently..
.PHONY: swig
swig: $(PYTHON_WRAPPER)

$(PYTHON_WRAPPER): $(wildcard *.i)
	$(SWIG) $(SWIGFLAGS) $(INTERFACE_FILE)

$(LIBNAME): $(OBJS) 
	$(CC) $(LFLAGS) $(LIBNAME) $(OBJS) $(LIBS)

.PHONY: clean
clean:
	rm $(OBJS) $(LIBNAME) $(PYTHON_WRAPPER)
