%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

Name:		globus-gram-job-manager-scripts
%global _name %(tr - _ <<< %{name})
Version:	4.1
Release:	3.1%{?dist}
Summary:	Globus Toolkit - GRAM Job ManagerScripts

Group:		Applications/Internet
BuildArch:	noarch
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.0/packages/src/%{_name}-%{version}.tar.gz

# OSG-specific patches
Patch0:         gratia.patch
Patch1:         osg-environment.patch
Patch2:         osg-path.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common-progs >= 14
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8

%package doc
Summary:	Globus Toolkit - GRAM Job ManagerScripts Documentation Files
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GRAM Job ManagerScripts

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GRAM Job ManagerScripts Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --without-flavor \
           --%{docdiroption}=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/GRAM
%dir %{_docdir}/%{name}-%{version}

%files doc -f package-doc.filelist
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/perl
%dir %{_docdir}/%{name}-%{version}/perl/Globus
%dir %{_docdir}/%{name}-%{version}/perl/Globus/GRAM

%changelog
* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 4.1-3.1
- Merge OSG changes
- Remove GRAM-278.diff, incorporated upstream

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-3
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-2
- Last sync prior to 5.2.0

* Mon Nov 28 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-1
- GRAM-278: GASS cache location not set in the perl environment

* Tue Nov 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.0-7
- Switch to fix for GRAM-278 from Globus.

* Mon Nov 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.0-6
- Properly configure the GASS cache from the job manager.

* Mon Oct 24 2011 Alain Roy <roy@cs.wisc.edu> - 4.0-4
- Updated pathnames in osg-environment.patch

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 4.0-3
- Add explicit dependencies on >= 5.2 libraries

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 4.0-2
- Update for 5.1.2 release
  
* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.1-3
- Small syntax error in the default path patch.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.1-2
- Porting OSG patches to GT5.2.

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.12-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-1
- Update to Globus Toolkit 5.0.2

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.5-2
- Mass rebuild with perl-5.12.0

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.4-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.7-1
- Autogenerated
