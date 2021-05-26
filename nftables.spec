#
# Conditional build:
%bcond_without	systemd		# without systemd unit

Summary:	Administration tool for packet filtering and classification
Summary(pl.UTF-8):	Narzędzie administracyjne do filtrowania i klasyfikacji pakietów
Name:		nftables
Version:	0.9.9
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://netfilter.org/projects/nftables/files/%{name}-%{version}.tar.bz2
# Source0-md5:	95bc3731a2e57d790482aac5bdd50c59
Source1:	%{name}.service
Source2:	%{name}.conf
Patch0:		%{name}-python.patch
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
BuildRequires:	libnftnl-devel >= 1.2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.644
Requires:	iptables-libs >= 1.6.1
Requires:	libmnl >= 1.0.4
Requires:	libnftnl >= 1.2.0
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
Summary:	Python bindings for libnftables library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libnftables
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-nftables
Python bindings for libnftables library.

%description -n python-nftables -l pl.UTF-8
Wiązania Pythona do biblioteki libnftables.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-json \
	--with-xtables

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir}}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

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

%py_postclean

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

%files static
%defattr(644,root,root,755)
%{_libdir}/libnftables.a

%files -n python-nftables
%defattr(644,root,root,755)
%dir %{py_sitedir}/nftables
%{py_sitedir}/nftables/*.py[co]
%{py_sitedir}/nftables/schema.json
%{py_sitedir}/nftables-0.1-py*.egg-info
