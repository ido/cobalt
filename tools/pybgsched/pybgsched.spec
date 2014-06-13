Summary: Python bindings to IBM's BlueGene/Q control system scheduler interface 
Name: pybgsched
Version: 0.1.4

Release: 1
License: None
Group: System Software
#URL: None
Prefix: /usr/lib64/python2.6/site-packages
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python >= 2.6 
#must put in dep for swig rpm and driver rpm's

%description
This is a SWIG-generated wrapper interface for python applications to access the
scheduler interface of the BlueGene/Q control system.  

%prep
%setup -q

%build
make swig
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/usr/lib64/python2.6/site-packages
install -m 644 ${RPM_BUILD_DIR}/%{name}-%{version}/pybgsched.py ${RPM_BUILD_ROOT}/usr/lib64/python2.6/site-packages
install -m 644 ${RPM_BUILD_DIR}/%{name}-%{version}/_pybgsched.so ${RPM_BUILD_ROOT}/usr/lib64/python2.6/site-packages


%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/lib64/python2.6/site-packages/pybgsched.py
/usr/lib64/python2.6/site-packages/_pybgsched.so
/usr/lib64/python2.6/site-packages/pybgsched.pyc
/usr/lib64/python2.6/site-packages/pybgsched.pyo

%changelog
* Fri Mar 07 2014 Paul Rich <richp@alcf.al.gov> -
- Changed threading to avoid situations where exception processing can cause python runtime crashes.
* Fri Feb 15 2013 Paul Rich <richp@alcf.anl.gov> -
- adding support for Action field in Blocks
- V1R2M0 additions for compilation and linking of library
- required for Cobalt v0.99.19 and later
- library now releases the GIL when operating on the database
* Fri Sep 21 2012 Paul Rich <richp@alcf.anl.gov> -
- rev 4: recompilation and relink wtih V1R1M2
* Thu Jul 26 2012 Paul Rich <richp@alcf.anl.gov> -
- Additions for V1R1M1
* Thu Feb  2 2012 Paul Rich <richp@alcf.anl.gov> -
- Initial build.

