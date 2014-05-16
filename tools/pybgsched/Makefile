#Makefile for python bindings for SWIG


CC = /usr/bin/g++
SWIG = /usr/bin/swig

MODULE = pybgsched

SWIGFLAGS = -python -threads -c++
INTERFACE_FILE = $(MODULE).i

PYTHON_INCLUDE = /usr/include/python2.6
PYTHON_WRAPPER = $(MODULE).py

BOOST = /bgsys/linux/RHEL6.1_base/usr
HLCS = /bgsys/drivers/ppcfloor/hlcs
LOG4CXX = /bgsys/drivers/ppcfloor/extlib
CFLAGS = -Wall -c -fPIC -g -Wall -I$(BOOST)/include -I$(HLCS)/include -I$(PYTHON_INCLUDE)
LFLAGS = -Wall -shared -fPIC -Wl,-rpath,$(HLCS)/lib,-rpath,$(LOG4CXX)/lib -o
LIBS = -L$(BOOST)/lib64 -L$(HLCS)/lib -lbgsched



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

$(MODULE)_wrap.o: $(MODULE)_wrap.cxx
	$(CC) $(CFLAGS) $(MODULE)_wrap.cxx

$(PYTHON_WRAPPER): $(wildcard *.i) $(wildcard *.h)
	$(SWIG) $(SWIGFLAGS) $(INTERFACE_FILE)

$(LIBNAME): $(OBJS) 
	$(CC) $(LFLAGS) $(LIBNAME) $(OBJS) $(LIBS)

.PHONY: clean
clean:
	rm $(OBJS) $(LIBNAME) $(PYTHON_WRAPPER)
