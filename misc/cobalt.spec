Summary: Cobalt System Software Suite
Name: cobalt
Version: 0.98.3pre2
Release: 1
License: GPL
Group: System Software
URL: http://www.mcs.anl.gov/cobalt
Prefix: /usr
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python2.5, python2.5-tlslite, M2Crypto, python2.5-xml

%package -n cobalt-clients
Version: %{version}
Summary: Cobalt Resource Management System clients
Group: Applications/System

%description -n cobalt-clients
Cobalt Resource Management clients. 

%description
The Cobalt Resource Management System

%prep

%setup -q
python2.5 setup.py build

%build
cd src/clients && make 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
python2.5 setup.py install --prefix=${RPM_BUILD_ROOT}/usr
install -m 755 src/clients/wrapper ${RPM_BUILD_ROOT}/usr/bin
install -m 755 src/clients/cobalt-admin ${RPM_BUILD_ROOT}/usr/bin
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/slp.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/bgsched.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/scriptm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/cqm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/brooklyn.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/partadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/setres.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/releaseres.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/cqadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/bgsystem.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/schedctl.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/cluster_system.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/cluster_simulator.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/nodeadm.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__mv} ${RPM_BUILD_ROOT}/usr/bin/perfdata.py ${RPM_BUILD_ROOT}%{_sbindir}
%{__rm} -f ${RPM_BUILD_ROOT}/usr/bin/test*
%{__rm} -f ${RPM_BUILD_ROOT}/usr/bin/brun.py
%{__rm} -f ${RPM_BUILD_ROOT}/usr/bin/bstat.py
%{__rm} -f ${RPM_BUILD_ROOT}/usr/bin/pmrun.py
%{__rm} -f ${RPM_BUILD_ROOT}/usr/bin/cdump.py
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
install -m 644 misc/cobalt ${RPM_BUILD_ROOT}/etc/init.d
#mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 644 misc/cobalt.conf ${RPM_BUILD_ROOT}/etc
cd ${RPM_BUILD_ROOT}%{_sbindir}
#for file in `find . -name \*.py | sed -e 's/\.py//' ` ; do ln -s cobalt-admin $file ; done
cd ${RPM_BUILD_ROOT}%{_bindir}
for file in `find . -name \*.py | sed -e 's/\.py//' |grep -v fake` ; do ln -sf wrapper $file ; done
mkdir -p ${RPM_BUILD_ROOT}/var/spool/cobalt
chmod 700 ${RPM_BUILD_ROOT}/var/spool/cobalt
find . -wholename "./Parser" -prune -o -name '*.py' -type f -print0 | xargs -0 grep -lE '^#! *(/usr/.*bin/(env +)?) ?python' | xargs sed -r -i -e '1s@^#![[:space:]]*(/usr/(local/)?bin/(env +)?)?python@#!/usr/bin/python2.5@'
cd ${RPM_BUILD_ROOT}/usr/bin ; for file in `find . -name \*.py -print` ; do ln -sf wrapper `echo $file|sed -e 's/.py//'` ; done 

%clean
#rm -rf $RPM_BUILD_ROOT

%pre
if ! /usr/bin/getent group cobalt &>/dev/null
then
    groupadd cobalt
fi

%post
chmod g+s /usr/bin/wrapper


%files -n cobalt
/usr/sbin/*
%config (noreplace) %attr(640,root,cobalt) /etc/cobalt.conf
%config(noreplace) /etc/init.d/cobalt
/usr/share/man/man5/*
/usr/share/man/man8/*.8*
/var/spool/cobalt


%files -n cobalt-clients
/usr/bin/*
%attr(755,root,cobalt) /usr/bin/wrapper
/usr/lib*/python2.5/site-packages/Cobalt/*
/usr/lib*/python2.5/site-packages/Cobalt-*egg-info*
/usr/share/man/man1/*.1*

%defattr(-,root,root,-)

%doc


%changelog
* Tue Oct  4 2005 Narayan Desai <desai@mcs.anl.gov> - 
- Initial build.

