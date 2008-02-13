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
mkdir %{buildroot}%{_initrddir}
%{_install} -m 644 misc/cobalt ${buildroot}%{_initrddir}
mkdir %{buildroot}%{_sysconfdir}
%{_install} -m 644 misc/cobalt.conf ${buildroot}%{_sysconfdir}
# need to create links here
mkdir -p ${RPM_BUILD_ROOT}/var/spool/cobalt
chmod 700 ${RPM_BUILD_ROOT}/var/spool/cobalt

%clean
rm -rf $RPM_BUILD_ROOT

%files -n cobalt
/usr/sbin/*
%config (noreplace) /etc/cobalt.conf
%config(noreplace) /etc/init.d/cobalt
/usr/man/man5/*
/usr/man/man8/*.8*
/var/spool/cobalt

%files -n cobalt-clients
/usr/bin/*
/usr/lib/python2.3/site-packages/Cobalt/*
/usr/man/man1/*.1*

%defattr(-,root,root,-)

%doc


%changelog
* Tue Oct  4 2005 Narayan Desai <desai@mcs.anl.gov> - 
- Initial build.

