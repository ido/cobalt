Summary: Plugin for IBM's runjob mux  
Name: libcorjplugin
Version: 0.1.0

Release: 1
License: None
Group: System Software
#URL: None
Prefix: /usr
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python >= 2.6 
#must put in dep for swig rpm and driver rpm's

%description
This is the plugin library for the runjob multiplexer. This plugin is used to simplify 
running subblock jobs.

%prep
%setup -q

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
install -m 644 ${RPM_BUILD_ROOT}/libcorjplugin.so ${RPM_BUILD_ROOT}/usr/lib64/


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* 2012-02-02 <richp@alcf.anl.gov> - 
- Initial build.

