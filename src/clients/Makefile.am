dist_sbin_SCRIPTS = cqadm.py partadm.py setres.py releaseres.py slpstat.py
dist_bin_SCRIPTS = cqsub.py cqstat.py cqdel.py partlist.py showres.py

bin_PROGRAMS = wrapper
wrapper_SOURCES = wrapper.c
wrapper_CFLAGS = -DPROGPREFIX=\"$(PREFIX)/bin\"
binPROGRAMS_INSTALL = ${INSTALL} -m 755 

install: install-am installlinks

installlinks: install-binPROGRAMS
	ln -sf ./wrapper $(bindir)/cqstat
	ln -sf ./wrapper $(bindir)/cqsub
	ln -sf ./wrapper $(bindir)/partlist
	ln -sf ./wrapper $(bindir)/cqdel
	ln -sf ./wrapper $(bindir)/showres
