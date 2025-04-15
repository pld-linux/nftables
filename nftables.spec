#
# Conditional build:
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	static_libs	# static library
%bcond_without	systemd		# without systemd unit

Summary:	Administration tool for packet filtering and classification
Summary(pl.UTF-8):	Narzędzie administracyjne do filtrowania i klasyfikacji pakietów
Name:		nftables
Version:	1.1.2
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://netfilter.org/projects/nftables/files/%{name}-%{version}.tar.xz
# Source0-md5:	b8566ef4a9836738b6ab5cdb8c521347
Source1:	%{name}.service
Source2:	%{name}.conf
URL:		https://netfilter.org/projects/nftables/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	iptables-devel >= 1.6.1
BuildRequires:	jansson-devel
BuildRequires:	libmnl-devel >= 1.0.4
BuildRequires:	libnftnl-devel >= 1.2.9
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python >= 1:2.5
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	iptables-libs >= 1.6.1
Requires:	libmnl >= 1.0.4
Requires:	libnftnl >= 1.2.9
%{?with_systemd:Requires:	systemd-units >= 38}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nftables is the project that aims to replace the existing
{ip,ip6,arp,eb}tables framework. Basically, this project provides a
new packet filtering framework, a new userspace utility and also a
compatibility layer for {ip,ip6}tables. nftables is built upon the
building blocks of the Netfilter infrastructure such as the existing
hooks, the connection tracking system, the userspace queueing
component and the logging subsystem.

%description -l pl.UTF-8
nftables to projekt mający na celu zastąpienie istniejącego szkieletu
{ip,ip6,arp,eb}tables. Ten projekt przede wszystkim dostarcza nowy
szkielet filtrowania, nowe narzędzie linii poleceń oraz warstwę
zgodności dla {ip,ip6}tables. nftables jest zbudowane w oparciu o
bloki tworzące infrastrukturę Netfilter, takie jak istniejące uchwyty,
system śledzenia połączeń, komponent kolejkowania w przestrzeni
użytkownika oraz podsystem logowania.

%package devel
Summary:	Header file for nftables library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki nftables
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for nftables library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki nftables.

%package static
Summary:	Static nftables library
Summary(pl.UTF-8):	Statyczna biblioteka nftables
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static nftables library.

%description static -l pl.UTF-8
Statyczna biblioteka nftables.

%package -n python-nftables
Summary:	Python 2 bindings for libnftables library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libnftables
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n python-nftables
Python 2 bindings for libnftables library.

%description -n python-nftables -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libnftables.

%package -n python3-nftables
Summary:	Python 3 bindings for libnftables library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libnftables
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n python3-nftables
Python 3 bindings for libnftables library.

%description -n python3-nftables -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libnftables.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	--with-cli=readline \
	--with-json \
	--with-xtables

%{__make}

cd py
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd py
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif
cd ..

cp %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/nftables
%{__sed} -i -e 's|@NFT@|%{_sbindir}/nft|' \
	$RPM_BUILD_ROOT/etc/sysconfig/nftables

%if %{with systemd}
cp %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}
%{__sed} -i -e '{
	s|@NFT@|%{_sbindir}/nft|
	s|@CONF@|/etc/sysconfig/nftables|
}' \
	$RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnftables.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{?with_systemd:%systemd_post %{name}.service}

%preun
%{?with_systemd:%systemd_preun %{name}.service}

%postun
/sbin/ldconfig
%{?with_systemd:%systemd_reload}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/nft
%dir %{_sysconfdir}/nftables
%dir %{_sysconfdir}/nftables/osf
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/osf/pf.os
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/nftables
%attr(755,root,root) %{_libdir}/libnftables.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnftables.so.1
%dir %{_datadir}/nftables
%attr(740,root,root) %{_datadir}/nftables/all-in-one.nft
%attr(740,root,root) %{_datadir}/nftables/arp-filter.nft
%attr(740,root,root) %{_datadir}/nftables/bridge-filter.nft
%attr(740,root,root) %{_datadir}/nftables/inet-filter.nft
%attr(740,root,root) %{_datadir}/nftables/inet-nat.nft
%attr(740,root,root) %{_datadir}/nftables/ipv4-filter.nft
%attr(740,root,root) %{_datadir}/nftables/ipv4-mangle.nft
%attr(740,root,root) %{_datadir}/nftables/ipv4-nat.nft
%attr(740,root,root) %{_datadir}/nftables/ipv4-raw.nft
%attr(740,root,root) %{_datadir}/nftables/ipv6-filter.nft
%attr(740,root,root) %{_datadir}/nftables/ipv6-mangle.nft
%attr(740,root,root) %{_datadir}/nftables/ipv6-nat.nft
%attr(740,root,root) %{_datadir}/nftables/ipv6-raw.nft
%attr(740,root,root) %{_datadir}/nftables/netdev-ingress.nft
%doc %{_docdir}/nftables
%{_mandir}/man5/libnftables-json.5*
%{_mandir}/man8/nft.8*
%{?with_systemd:%{systemdunitdir}/%{name}.service}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnftables.so
%{_includedir}/nftables
%{_pkgconfigdir}/libnftables.pc
%{_mandir}/man3/libnftables.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnftables.a
%endif

%if %{with python2}
%files -n python-nftables
%defattr(644,root,root,755)
%{py_sitescriptdir}/nftables
%{py_sitescriptdir}/nftables-0.1-py*.egg-info
%endif

%if %{with python3}
%files -n python3-nftables
%defattr(644,root,root,755)
%{py3_sitescriptdir}/nftables
%{py3_sitescriptdir}/nftables-0.1-py*.egg-info
%endif
