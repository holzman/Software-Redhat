%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:		globus-gram-job-manager-condor
%global _name %(tr - _ <<< %{name})
Version:	0.0
Release:	3%{?dist}
Summary:	Globus Toolkit - Condor Job Manager

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		%{_name}-%{version}.tar.gz
Source1:        condor_accounting_groups.pm

# OSG Patches
Patch0:         job_status.patch
Patch1:         gratia.patch
Patch2:         nfslite.patch
Patch3:         groupacct.patch
Patch4:         managedfork.patch
Patch5:         conf_location.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-job-manager-scripts
Requires:	globus-gass-cache-program >= 2
Requires:	globus-common-progs >= 2
Requires:	globus-gram-job-manager >= 10.59
Requires:	globus-gatekeeper >= 7.3
Requires:       condor
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-core
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	tex(latex)
%else
BuildRequires:	tetex-latex
%endif

Provides:  globus-gram-job-manager-setup-condor
Obsoletes: globus-gram-job-manager-setup-condor < 4.5

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Condor Job Manager 

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0


# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

CONDOR_RM=/usr/bin/condor_rm \
CONDOR_SUBMIT=/usr/bin/condor_submit \
    %configure --%{docdiroption}=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Remove jobmanager-condor from install dir so that it can be
# added/removed by post scripts
rm $RPM_BUILD_ROOT/etc/grid-services/jobmanager-condor

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

sed -i s!$RPM_BUILD_ROOT!! $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_rtl.filelist \
  | sed s!^!%{_prefix}! \
  | sed s!^%{_prefix}/etc!/etc! > package.filelist

cat package.filelist

# Install the group accounting patch
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg
touch $RPM_BUILD_ROOT%{_sysconfdir}/osg/uid_table.txt
touch $RPM_BUILD_ROOT%{_sysconfdir}/osg/extattr_table.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
globus-gatekeeper-admin -e jobmanager-condor

%postun
globus-gatekeeper-admin -d jobmanager-condor || true

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%config(noreplace) %{_sysconfdir}/osg/extattr_table.txt
%config(noreplace) %{_sysconfdir}/osg/uid_table.txt
%{perl_vendorlib}/Globus/GRAM/JobManager/condor_accounting_groups.pm

%changelog
* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0-3
- Port all OSG patches to GT52.

* Fri Aug 12 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0-2
- Add provides in order to provide a smooth transition from previous packaging.

