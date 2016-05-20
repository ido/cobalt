Summary: Cobalt System Software Suite
Name: cobalt
Version: $Version$

Release: 1
License: CPL
Group: System Software
URL: http://www.mcs.anl.gov/cobalt
Prefix: /usr
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python >= 2.6

%package -n cobalt-clients
Version: %{version}
Summary: Cobalt Resource Management System clients
Group: Applications/System
Requires: %{requires}

%description -n cobalt-clients
Cobalt Resource Management clients. 

%description
The Cobalt Resource Management System

%prep

%setup -q
python2.6 setup.py build
%define client_wrapper_dir /usr/libexec/cobalt
%define python_wrapper_dir %{client_wrapper_dir}/bin

%build
cd src/clients && make PROGPREFIX=%{client_wrapper_dir}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{client_wrapper_dir}

python2.6 setup.py install --prefix=${RPM_BUILD_ROOT}%{client_wrapper_dir} --install-lib ${RPM_BUILD_ROOT}/usr/lib64/python2.6/site-packages
install -m 755 src/clients/wrapper ${RPM_BUILD_ROOT}%{python_wrapper_dir}
install -m 755 src/clients/cobalt-admin ${RPM_BUILD_ROOT}%{_sbindir$}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/slp.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bgsched.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/user_script_forker.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cqm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bg_mpirun_forker.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bg_runjob_forker.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/system_script_forker.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/gravina.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/partadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/setres.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/releaseres.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cqadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bgsystem.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bgqsystem.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/schedctl.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cluster_system.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cluster_simulator.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/nodeadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/perfdata.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/prologue_helper.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cdbwriter.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__rm} -f ${RPM_BUILD_ROOT}%{python_wrapper_dir}/test*
%{__rm} -f ${RPM_BUILD_ROOT}%{python_wrapper_dir}/brun.py
%{__rm} -f ${RPM_BUILD_ROOT}%{python_wrapper_dir}/bstat.py
%{__rm} -f ${RPM_BUILD_ROOT}%{python_wrapper_dir}/pmrun.py
%{__rm} -f ${RPM_BUILD_ROOT}%{python_wrapper_dir}/cdump.py
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
#install -m 644 misc/cobalt ${RPM_BUILD_ROOT}/etc/init.d
#mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 644 misc/cobalt.conf ${RPM_BUILD_ROOT}/etc
cd ${RPM_BUILD_ROOT}%{_sbindir}
#for file in `find . -name \*.py | sed -e 's/\.py//' ` ; do ln -s cobalt-admin $file ; done
cd ${RPM_BUILD_ROOT}%{python_wrapper_dir}
for file in `find . -name \*.py | sed -e 's/\.py//' |grep -v fake` ; do ln -sf  %{python_wrapper_dir}/wrapper ${RPM_BUILD_ROOT}%{_bindir}/$file ; done
find . -wholename "./Parser" -prune -o -name '*.py' -type f -print0 | xargs -0 grep -lE '^#! *(/usr/.*bin/(env +)?) ?python' | xargs sed -r -i -e '1s@^#![[:space:]]*(/usr/(local/)?bin/(env +)?)?python@#!/usr/bin/python@'
#cd ${RPM_BUILD_ROOT}%{python_wrapper_dir} ; for file in `find . -name \*.py -print` ; do ln -sf wrapper `echo ${RPM_BUILD_ROOT}%{_bindir}/$file|sed -e 's/.py//'` ; done
cd ${RPM_BUILD_ROOT}/usr/sbin ; for file in `find . -name \*.py -print` ; do ln -sf $file `echo $file|sed -e 's/.py//'` ; done
#put manpages back in the right place
%{__mv} ${RPM_BUILD_ROOT}%{client_wrapper_dir}/share ${RPM_BUILD_ROOT}/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if ! /usr/bin/getent group cobalt &>/dev/null
then
    groupadd cobalt
fi

%post -n cobalt
if test ! -d /var/spool/cobalt ; then
    mkdir -p /var/spool/cobalt
    chmod 700 /var/spool/cobalt
fi

if test ! -d /var/spool/cobalt/overflow ; then
    mkdir -p /var/spool/cobalt/overflow
    chmod 700 /var/spool/cobalt/overflow
fi
if [ ! -d /var/log/cobalt ]; then
    mkdir -p /var/log/cobalt
    chmod 755 /var/log/cobalt
    chgrp cobalt /var/log/cobalt
fi

%files -n cobalt
/usr/sbin/*
%config (noreplace) %attr(640,root,cobalt) /etc/cobalt.conf
#%config(noreplace) /etc/init.d/cobalt
/usr/share/man/man5/*
/usr/share/man/man8/*.8*


%files -n cobalt-clients
%{python_wrapper_dir}/*
/usr/bin/*
%attr(2755,root,cobalt) %{python_wrapper_dir}/wrapper
/usr/lib*/python2.6/site-packages/Cobalt/*
/usr/lib*/python2.6/site-packages/Cobalt-*egg-info*
/usr/share/man/man1/*.1*

%defattr(-,root,root,-)

%doc


%changelog
* Tue Oct  4 2005 Narayan Desai <desai@mcs.anl.gov> - 
- Initial build.

