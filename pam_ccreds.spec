%define	name	pam_ccreds
%define	version	10
%define	release	%mkrel 3

Summary:	A caching pam module for disconnected operation
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Patch0:		pam_ccreds-10-dbnss.patch
Patch1:		pam_ccreds-strdup.patch
Group:		System/Libraries
License:	GPLv2
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
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
%patch0 -p1 -b .dbnss
%patch1 -p1 -b .strdup

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
