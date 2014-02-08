Summary:	A caching pam module for disconnected operation
Name:		pam_ccreds
Version:	10
Release:	8
Source0: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Patch0:		pam_ccreds-10-dbnss.patch
Patch1:		pam_ccreds-strdup.patch
Patch2:		pam_ccreds-automake-1.13.patch
Group:		System/Libraries
License:	GPLv2
BuildRequires:	pam-devel
BuildRequires:	db_nss-devel >= 4.2.52-5mdk
BuildRequires:	openssl-devel
Url:		http://www.padl.com/

%description
The pam_ccreds module provides a mechanism for caching
credentials when authenticating against a network
authentication service, so that authentication can still
proceed when the service is down. Note at present no
mechanism is provided for caching _authorization_ 
information, i.e. whether you are allowed to login once
authenticated. Doing this is more difficult than it
first sounds.

%prep
%setup -q
rm -f acconfig.h
%apply_patches

%build
autoreconf
%configure2_5x --libdir=/%{_lib}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}/%{_sbindir}
install pam_ccreds.so %{buildroot}/%{_lib}/security
install cc_dump cc_test %{buildroot}/%{_sbindir}
install ccreds_chkpwd %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/var/cache
touch %{buildroot}/var/cache/.security.db

%files
%defattr(-,root,root,755)
%doc AUTHORS README ChangeLog pam.conf
%attr(4755,root,root) %{_sbindir}/ccreds_chkpwd
%{_sbindir}/cc_dump
%{_sbindir}/cc_test
/%{_lib}/security/pam_ccreds.so
%ghost /var/cache/.security.db

%post
if [ ! -f /var/cache/.security.db ]; then
%{_sbindir}/cc_test -update any root - > /dev/null 2>/dev/null || :
fi

%clean
rm -rf %{buildroot}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 10-5mdv2011.0
+ Revision: 666976
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 10-4mdv2011.0
+ Revision: 607056
- rebuild

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 10-3mdv2010.1
+ Revision: 532513
- rebuild for new openssl

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 10-2mdv2010.1
+ Revision: 511608
- rebuilt against openssl-0.9.8m

* Thu Jul 30 2009 Luca Berra <bluca@mandriva.org> 10-1mdv2010.0
+ Revision: 404498
- updated to version 10
- removed merged patches, rediffed dbnss patch

* Mon Jul 27 2009 Luca Berra <bluca@mandriva.org> 4-5mdv2010.0
+ Revision: 400565
- more strxxx fixes, resolves GDM segfault which passes empty username to pam (#45989)

* Fri Apr 10 2009 Luca Berra <bluca@mandriva.org> 4-4mdv2009.1
+ Revision: 365670
- fix a segfault in cc_test
  create empty db on first installation

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 4-3mdv2009.0
+ Revision: 220243
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Thu Nov 16 2006 Buchan Milne <bgmilne@mandriva.org> 4-2mdv2007.0
+ Revision: 84964
- ship the ccreds_validate binary required for non-root use

* Sat Oct 07 2006 Buchan Milne <bgmilne@mandriva.org> 4-1mdv2007.1
+ Revision: 62924
- Import pam_ccreds

* Tue Oct 03 2006 Buchan Milne <bgmilne@mandriva.org> 4-1mdv2007.0
- new version 4
- apply patch adding setuid helper from Mike Petullo

* Tue Jan 03 2006 Buchan Milne <bgmilne@mandriva.org> 3-1mdk
- New release 3
- use %%mkrel

* Sun Sep 18 2005 Luca Berra <bluca@vodka.it> 0.1-3mdk
- rebuild

* Tue Aug 17 2004 Luca Berra <bluca@vodka.it> 0.1-2mdk 
- updated to use libdb_nss 4.2

* Tue Mar 02 2004 Luca Berra <bluca@vodka.it> 0.1-1mdk 
- initial mandrake contrib

