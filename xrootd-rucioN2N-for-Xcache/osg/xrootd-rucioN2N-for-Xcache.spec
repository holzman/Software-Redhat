Name:      xrootd-rucioN2N-for-Xcache
Version:   1.2
Release:   1%{?dist}
Summary:   Xrootd Name-to-Name plugin for Disk Caching Proxy (Xcache) to utilize RUCIO metalink
Group:     System Environment/Libraries
License:   BSD 
Vendor:    Stanford University/SLAC
URL:       https://github.com/wyang007/rucioN2N-for-Xcache


Source0:   rucioN2N-for-Xcache-%{version}.tar.gz
Patch1: link_to_lXrdPfc5.patch 
BuildArch: x86_64

%define xrootd_current 5.0
%define xrootd_next %(echo %xrootd_current | awk '{print $1,$2+1}' FS=. OFS=.)

BuildRequires: xrootd-server-devel >= 1:%{xrootd_current}.0-0
BuildRequires: xrootd-server-devel <  1:%{xrootd_next}.0-0
BuildRequires: xrootd-client-devel >= 1:%{xrootd_current}.0-0
BuildRequires: xrootd-client-devel <  1:%{xrootd_next}.0-0
BuildRequires: xrootd-devel >= 1:%{xrootd_current}.0-0
BuildRequires: xrootd-devel <  1:%{xrootd_next}.0-0
BuildRequires: libcurl-devel openssl-devel

Requires: xrootd >= 1:%{xrootd_current}.0-0
Requires: xrootd <  1:%{xrootd_next}.0-0
Requires: xrootd-client >= 1:%{xrootd_current}.0-0
Requires: xrootd-client <  1:%{xrootd_next}.0-0
Requires: libcurl openssl

%description
rucioN2N-for-Xcache is a xrootd plugin module that will identify multiple copies of a distributed file based on ATLAS RUCIO data management system. Please refers to project's twiki in github (https://github.com/wyang007/rucioN2N-for-Xcache) for more info.

%prep
#%setup -q -c -D -T %{name} 
%setup -q -c %{name} 
%patch1 -p0

%build
pwd
ls
cd rucioN2N-for-Xcache-%{version}
# Caution !!!
# if you build along with the xrootd rpms, uncommand the folloing line and comment out the 2 lines after it
make
#make XRD_INC=/afs/slac/package/xrootd/xrootd-4.6.0/xrootd/src XRD_LIB=/afs/slac/package/xrootd/xrootd-4.6.0/@sys/src
#mv XrdName2NameDCP4RUCIO.so XrdName2NameDCP4RUCIO-4.so

%install
mkdir -p %{buildroot}/usr/lib64
cp rucioN2N-for-Xcache-%{version}/XrdName2NameDCP4RUCIO.so %{buildroot}/usr/lib64/XrdName2NameDCP4RUCIO.so


%files
/usr/lib64/XrdName2NameDCP4RUCIO.so

%post -p /sbin/ldconfig

%changelog 
* Sat Feb 1 2020 Diego Davila <didavila@ucsd.edu> - v1.2-1
- Building against Xrootd 5.0 (SOFTWARE-3923)
- Adding patch: link_to_lXrdPfc5.patch 
- Bumping version 1.2-1

* Mon Aug 5 2019 Edgar Fajardo <emfajard@ucsd.edu> - v1.2-0
- Bumping version 1.2 (SOFTWARE-3784)

* Thu Jul 18 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-4
- Rebuild against xrootd 4.10.0 (SOFTWARE-3697)

* Wed Apr 24 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-3
- Rebuild against xrootd 4.9.1 (SOFTWARE-3678)

* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

* Fri Sep 21 2018 Edgar Fajardo <emfajard@ucsd.edu> v1.1-1
- Releasing for SOFTWARE-3383
- Removed some noise from the spec only needed for rhel5

* Tue Oct 3 2017 Wei Yang <yangw.slac.stanford.edu> v1.0, require xrootd 4.7, generate -4.so
- Tue Oct 3 2017 initial version
