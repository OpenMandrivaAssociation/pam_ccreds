Summary:	A caching pam module for disconnected operation
Name:		pam_ccreds
Version:	10
Release:	15
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.padl.com/
Source0: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Patch0:		pam_ccreds-10-dbnss.patch
Patch1:		pam_ccreds-strdup.patch
Patch2:		pam_ccreds-automake-1.13.patch
BuildRequires:	pam-devel
BuildRequires:	db_nss52-devel
BuildRequires:	pkgconfig(openssl)

%description
The pam_ccreds module provides a mechanism for caching credentials when
authenticating against a network authentication service, so that
authentication can still proceed when the service is down. Note at present
no mechanism is provided for caching _authorization_ information, i.e.
whether you are allowed to login once authenticated. Doing this is more
difficult than it first sounds.

%files
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

#----------------------------------------------------------------------------

%prep
%setup -q
rm -f acconfig.h
%apply_patches

%build
autoreconf -fi
%configure2_5x --libdir=/%{_lib}
make

%install
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}/%{_sbindir}
install pam_ccreds.so %{buildroot}/%{_lib}/security
install cc_dump cc_test %{buildroot}/%{_sbindir}
install ccreds_chkpwd %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/var/cache
touch %{buildroot}/var/cache/.security.db

