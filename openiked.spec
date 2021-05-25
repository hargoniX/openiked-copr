Name:           openiked
Version:        6.9.0
Release:        1%{?dist}
Summary:        Port of OpenBSD's OpenIKED to Linux

License:        ISC
URL:            https://github.com/openiked/openiked-portable
Source0:        https://ftp.openbsd.org/pub/OpenBSD/OpenIKED/openiked-%{version}.tar.gz
Source1:        https://ftp.openbsd.org/pub/OpenBSD/OpenIKED/openiked-%{version}.tar.gz.asc
Source2:        openiked.service
Source3:        sysusers.conf
Source4:        openiked-keygen
Source5:        openiked-keygen.service
Source6:        openiked-keygen.target

BuildArch:      x86_64 aarch64
BuildRequires:  cmake libevent-devel openssl-devel byacc clang systemd-rpm-macros
Requires:       libevent openssl

%systemd_requires
%{?sysusers_requires_compat}

%description
OpenIKED is a free, permissively licensed Internet Key Exchange (IKEv2)
implementation, developed as part of the OpenBSD project. It is intended to be
a lean, secure and interoperable daemon that allows for easy setup and
management of IPsec VPNs.

%prep
%autosetup

%build
%cmake
%cmake_build

%install
%cmake_install
install -p -D -m644 %{SOURCE2} $RPM_BUILD_ROOT/%{_unitdir}/openiked.service
install -p -D -m644 %{SOURCE3} %{buildroot}%{_sysusersdir}/openiked.conf
install -p -D -m744 %{SOURCE4} $RPM_BUILD_ROOT/%{_libexecdir}/openiked/openiked-keygen
install -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_unitdir}/openiked-keygen.service
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/%{_unitdir}/openiked-keygen.target

%check
%{__cmake_builddir}/regress/dh/dhtest
%{__cmake_builddir}/regress/parser/test_parser

%pre
%sysusers_create_compat %{SOURCE3}

%post
%systemd_post openiked.service

%postun
%systemd_postun_with_restart openiked.service

%files
%license LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iked.conf
%attr(0755,root,root) %{_sbindir}/iked
%attr(0755,root,root) %{_sbindir}/ikectl
%attr(0644,root,root) %{_mandir}/man5/iked.conf.5.gz
%attr(0644,root,root) %{_mandir}/man8/ikectl.8.gz
%attr(0644,root,root) %{_mandir}/man8/iked.8.gz
%attr(0644,root,root) %{_unitdir}/openiked.service
%{_sysusersdir}/openiked.conf
%attr(0755,root,root) %{_sysconfdir}/iked/ca
%attr(0755,root,root) %{_sysconfdir}/iked/certs
%attr(0755,root,root) %{_sysconfdir}/iked/crls
%attr(0755,root,root) %{_sysconfdir}/iked/pubkeys/ipv4
%attr(0755,root,root) %{_sysconfdir}/iked/pubkeys/ipv6
%attr(0755,root,root) %{_sysconfdir}/iked/pubkeys/fqdn
%attr(0755,root,root) %{_sysconfdir}/iked/pubkeys/ufqdn
%attr(0700,root,root) %{_sysconfdir}/iked/private
%attr(0755,root,root) %{_libexecdir}/openiked/openiked-keygen
%attr(0644,root,root) %{_unitdir}/openiked-keygen.service
%attr(0644,root,root) %{_unitdir}/openiked-keygen.target


%changelog
* Tue May 25 2021 Henrik Boeving <hargonix@gmail.com> - 6.9.0-1
- initial packaging

