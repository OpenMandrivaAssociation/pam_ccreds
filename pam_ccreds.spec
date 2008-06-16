%define	name pam_ccreds
%define	version	4
%define	release	%mkrel 3

Summary: 	A caching pam module for disconnected operation
Name:       %{name}
Version:    %{version}
Release:    %{release}
Source: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Patch:		pam_ccreds-dbnss.patch
Patch1:		pam_ccreds-4-chkpwd.patch
Group:		System/Libraries
License:	GPL
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: pam-devel
BuildRequires: db_nss-devel >= 4.2.52-5mdk
BuildRequires: openssl-devel
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
%patch0 -p1 -b .dbnss
%patch1 -p1 -b .helper

%build
rm configure
touch compile
autoreconf
%configure2_5x --libdir=/%{_lib}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}/%{_sbindir}
install pam_ccreds.so %{buildroot}/%{_lib}/security
install cc_dump cc_test %{buildroot}/%{_sbindir}
install -m4755 ccreds_validate %{buildroot}/%{_sbindir}

%files
%defattr(-,root,root,755)
%doc AUTHORS README ChangeLog pam.conf
%{_sbindir}/ccreds_validate
%{_sbindir}/cc_dump
%{_sbindir}/cc_test
/%{_lib}/security/pam_ccreds.so

%clean
rm -rf %{buildroot}


