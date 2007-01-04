dist_sbin_SCRIPTS = cqadm.py partadm.py setres.py releaseres.py slpstat.py
dist_bin_SCRIPTS = cqsub.py cqstat.py cqdel.py partlist.py showres.py

bin_PROGRAMS = wrapper
wrapper_SOURCES = wrapper.c
wrapper_CFLAGS = -DPROGPREFIX=\"$(PREFIX)/bin\"
binPROGRAMS_INSTALL = ${INSTALL} -m 755 

install: install-am installlinks

installlinks: install-binPROGRAMS install-dist_binSCRIPTS install-wrapper
	test -z $(bindir) || $(mkdir_p) $(bindir)
	ln -sf $(WRAPPERDIR)/wrapper $(bindir)/cqstat
	ln -sf $(WRAPPERDIR)/wrapper $(bindir)/cqsub
	ln -sf $(WRAPPERDIR)/wrapper $(bindir)/partlist
	ln -sf $(WRAPPERDIR)/wrapper $(bindir)/cqdel
	ln -sf $(WRAPPERDIR)/wrapper $(bindir)/showres

install-binPROGRAMS:
install-wrapper: $(bin_PROGRAMS)
	${INSTALL} -m 755 wrapper $(WRAPPERDIR)
# 	${INSTALL} -m 2755 -g cobalt wrapper $(WRAPPERDIR)

