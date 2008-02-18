Summary: Cobalt System Software Suite
Name: cobalt
Version: 0.98.0pre3
Release: 1
License: GPL
Group: System Software
URL: http://www.mcs.anl.gov/cobalt
Prefix: /usr
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python2.5, python-tlslite, python-m2crypto

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
python2.5 setup.py install --prefix=${RPM_BUILD_ROOT}/usr
install -m 755 src/clients/wrapper ${RPM_BUILD_ROOT}/usr/bin
mkdir %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/slp.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/bgsched.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/scriptm.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/cqm.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/brooklyn.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/partadm.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/setres.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/releaseres.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/cqadm.py %{buildroot}%{_sbindir}
%{__mv} %{buildroot}/usr/bin/bgsystem.py %{buildroot}%{_sbindir}
%{__rm} -f %{buildroot}/usr/bin/test*
%{__rm} -f %{buildroot}/usr/bin/brun.py
%{__rm} -f %{buildroot}/usr/bin/bstat.py
%{__rm} -f %{buildroot}/usr/bin/pmrun.py
%{__rm} -f %{buildroot}/usr/bin/cdump.py
mkdir -p %{buildroot}%{_initrddir}
install -m 644 misc/cobalt ${RPM_BUILD_ROOT}/etc/init.d
#mkdir %{buildroot}%{_sysconfdir}
install -m 644 misc/cobalt.conf ${RPM_BUILD_ROOT}/etc
# need to create links here
mkdir -p ${RPM_BUILD_ROOT}/var/spool/cobalt
chmod 700 ${RPM_BUILD_ROOT}/var/spool/cobalt
find . -wholename "./Parser" -prune -o -name '*.py' -type f -print0 | xargs -0 grep -lE '^#! *(/usr/.*bin/(env +)?) ?python' | xargs sed -r -i -e '1s@^#![[:space:]]*(/usr/(local/)?bin/(env +)?)?python@#!/usr/bin/python2.5@'
cd ${RPM_BUILD_ROOT}/usr/bin ; for file in `find . -name \*.py -print` ; do ln -s wrapper `echo $file|sed -e 's/.py//'` ; done 

%clean
#rm -rf $RPM_BUILD_ROOT

%files -n cobalt
/usr/sbin/*
%config (noreplace) /etc/cobalt.conf
%config(noreplace) /etc/init.d/cobalt
/usr/share/man/man5/*
/usr/share/man/man8/*.8*
/var/spool/cobalt

%files -n cobalt-clients
/usr/bin/*
/usr/lib/python2.5/site-packages/Cobalt/*
/usr/lib/python2.5/site-packages/Cobalt-0.98.0pre3-py2.5.egg-info
/usr/share/man/man1/*.1*

%defattr(-,root,root,-)

%doc


%changelog
* Tue Oct  4 2005 Narayan Desai <desai@mcs.anl.gov> - 
- Initial build.

