%define dver %{?rhel}%{?!rhel:6}
Name:		buildsys-macros
Summary:	Macros for the HTCondor team's usage of the OSG Koji instance
Version:        7.condor
Release:	9.el%{dver}
License:	GPL
Group:		Development/Buildsystem
BuildArch:      noarch
Requires:	rpmdevtools

%description
%{summary}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
DVER=%{dver}
printf %s%b "%" "rhel $DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "dist .el$DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "el$DVER 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "uw_build 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "__arch_install_post /usr/lib/rpm/check-buildroot\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.checkbuild


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild

%changelog
* Wed Mar 14 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 7.condor-9
- Drop .uw from dist tag

* Thu Mar 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 7-8.uw
- Add .uw to the dist tag

* Mon Mar 03 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 7-7
- Bump to rebuild with buildsys-macros 7-6

* Mon Mar 03 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 7-6
- Bump to rebuild with buildsys-macros 7-5
* Mon Mar 03 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 7-5
- Create condor version of buildsys-macros

* Wed Dec 11 2013 Carl Edquist <edquist@cs.wisc.edu> - 7-4
- Bump to rebuild with buildsys-macros 7-3

* Tue Dec 10 2013 Carl Edquist <edquist@cs.wisc.edu> - 7-3
- Create osg-internal version of buildsys-macros

* Tue Oct 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-2
- Bump to rebuild with buildsys-macros 7-1

* Tue Oct 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-1
- Add osg major version to dist tag (e.g. .osg32.el5)
- No longer base Version on the %%rhel macro

* Fri Aug 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6-8
- Added 'osg' macro that's 1 for all osg builds

* Wed Jan 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 6-7.osg
- Added rhel6 version

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 5-6.osg
- Creation of the OSG buildsys-macros.

* Mon May 21 2007 Dennis Gilmore <dennis@ausil.us> 
- add el<ver> 1  fro new disttag guidelines

* Wed Sep 27 2006 Dennis Gilmore <dennis@ausil.us>
- add macro to run check-buildroot

* Mon Jul 07 2006 Dennis Gilmore <dennis@ausil.us>
- rhel version

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com>
- Initial build.
