#
# spec file for package cray_messaging
#
# Copyright (c) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name: cray_messaging
Version: 1.0
Release: 1
License: UNRELEASED
Summary: Cray ALPS message-generation library for python 2.7
Group: System Software
Provides: cray_messaging.py
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-build
Source0: %{name}-%{version}.tar.gz
Requires: python >= 2.7

%description
XML message generation library for use with ALPS Basil on Cray systems.  This
library targets BASIL protocol versions 1.7 and later.  Use with earlier
protocol versions is not supported.  This protocol version corresponds to
CLE 6.0/SMW 8.0 UP00 from Cray.

%prep
%setup -q
python setup.py -v build

%build

%install
python2.7 setup.py install --prefix ${RPM_BUILD_ROOT}/usr/lib64/python2.7/site-packages --install-lib ${RPM_BUILD_ROOT}/usr/lib64/python2.7/site-packages

%clean
rm -rf $RPM_BUILD_ROOT
%post

%postun

%files
/usr/lib*/python2.7/site-packages/*
/usr/lib*/python2.7/site-packages/cray_messaging-*egg-info*
%defattr(-,root,root)
%doc README.md


