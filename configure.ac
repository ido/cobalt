# Autoconf requirements
AC_INIT(Cobalt,0.97.1pre1)
AM_INIT_AUTOMAKE(Cobalt,0.97.1pre1)

AC_CONFIG_HEADER(config.h)

# definately need a C compiler
AC_PROG_CC()

# for now, require python 2.2+ and python-xml
#AM_PATH_PYTHON(2.2)

AC_ARG_WITH(pidfile,[  --with-pidfile             pidfile location (default /var/tmp)],
        ac_cv_pidfile=$withval)


if test "${prefix}" = "NONE"; then
        prefix=/usr/local
        if test -z "$ac_cv_var"; then
                ac_cv_pidfile=/usr/local/tmp
        fi
else
        if test -z "$ac_cv_var"; then
                ac_cv_pidfile=/var/run
        fi
fi


AC_ARG_WITH(wrapper,[  --with-wrapper            location for wrapper to be installed (default $prefix/bin)],
	ac_cv_wrapper=$withval)

if test -z "${ac_cv_wrapper}"; then
        ac_cv_wrapper=$bindir
fi

AM_PATH_PYTHON(2.2)

PREFIX=${prefix}
AC_SUBST(PREFIX)
PATH_TO_PIDFILE=$ac_cv_pidfile
AC_SUBST(PATH_TO_CONFIG)
AC_SUBST(PATH_TO_PIDFILE)

WRAPPERDIR=$ac_cv_wrapper
AC_SUBST(WRAPPERDIR)

AC_CONFIG_FILES(Makefile
	src/Makefile
	src/components/Makefile
	src/clients/Makefile
	src/lib/Makefile
	misc/cobalt)
AC_OUTPUT()
