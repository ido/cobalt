Summary: Cobalt System Software Suite
Name: cobalt
Version: 0.96pre1
Release: 2
License: GPL
Group: System Software
URL: http://www.mcs.anl.gov/cobalt
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: pyOpenSSL, python

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
./configure --prefix=/usr --sysconfdir=/etc

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=${RPM_BUILD_ROOT}/usr sssinitdir=${RPM_BUILD_ROOT}/etc/init.d sysconfdir=${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/var/spool/cobalt
chmod 700 ${RPM_BUILD_ROOT}/var/spool/cobalt

%clean
rm -rf $RPM_BUILD_ROOT

%files -n cobalt
/usr/sbin/*
/etc/cobalt.conf.sample
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

