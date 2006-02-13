SUBDIRS = src .
man1_MANS = man/*.1
man5_MANS = man/*.5
man8_MANS = man/*.8

EXTRA_DIST = $(man1_MANS) $(man5_MANS) $(man8_MANS)

sssinitdir = @sysconfdir@/init.d

dist_sssinit_SCRIPTS = misc/cobalt

sysconf_DATA = misc/cobalt.conf.sample
