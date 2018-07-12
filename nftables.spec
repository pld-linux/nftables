Summary:	Administration tool for packet filtering and classification
Summary(pl.UTF-8):	Narzędzie administracyjne do filtrowania i klasyfikacji pakietów
Name:		nftables
Version:	0.9.0
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://netfilter.org/projects/nftables/files/%{name}-%{version}.tar.bz2
# Source0-md5:	d4dcb61df80aa544b2e142e91d937635
URL:		https://netfilter.org/projects/nftables/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	dblatex
BuildRequires:	docbook2X
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	iptables-devel >= 1.6.1
BuildRequires:	jansson-devel
BuildRequires:	libmnl-devel >= 1.0.3
BuildRequires:	libnftnl-devel >= 1.1.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
Requires:	iptables-libs >= 1.6.1
Requires:	libmnl >= 1.0.3
Requires:	libnftnl >= 1.1.1
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	DOCBOOK2X_MAN=/usr/bin/docbook2X2man \
	--disable-silent-rules \
	--with-json \
	--with-xtables

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnftables.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/nft
%dir %{_sysconfdir}/nftables
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/all-in-one.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/arp-filter.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/bridge-filter.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/inet-filter.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv4-filter.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv4-mangle.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv4-nat.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv4-raw.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv6-filter.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv6-mangle.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv6-nat.nft
%attr(740,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nftables/ipv6-raw.nft
%attr(755,root,root) %{_libdir}/libnftables.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnftables.so.0
%{_mandir}/man8/nft.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnftables.so
%{_includedir}/nftables
%{_pkgconfigdir}/libnftables.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnftables.a
