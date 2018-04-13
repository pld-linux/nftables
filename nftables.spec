Summary:	Administration tool for packet filtering and classification
Summary(pl.UTF-8):	Narzędzie administracyjne do filtrowania i klasyfikacji pakietów
Name:		nftables
Version:	0.8.3
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://netfilter.org/projects/nftables/files/%{name}-%{version}.tar.bz2
# Source0-md5:	a604501c10a302fa417410b16f293d2c
URL:		https://netfilter.org/projects/nftables/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1.6
BuildRequires:	bison
BuildRequires:	dblatex
BuildRequires:	docbook2X
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	iptables-devel >= 1.6.1
BuildRequires:	libmnl-devel >= 1.0.3
BuildRequires:	libnftnl-devel >= 1.0.9
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
Requires:	iptables-libs >= 1.6.1
Requires:	libmnl >= 1.0.3
Requires:	libnftnl >= 1.0.9
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
	--with-xtables

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO files/examples
%attr(755,root,root) %{_sbindir}/nft
%{_mandir}/man8/nft.8*
