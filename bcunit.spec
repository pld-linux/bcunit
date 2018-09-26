Summary:	Provide C programmers basic testing functionality
Name:		bcunit
Version:	3.0.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/bcunit/%{name}-%{version}.tar.gz
# Source0-md5:	3c197563b790131da8ad1be6a23f9c91
Patch0:		lib.patch
URL:		https://linphone.org/
BuildRequires:	cmake
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BCUnit is a unit testing framework for C, derived from CUnit. (B)CUnit
provides various interfaces to the framework, some of which are
platform dependent (e.g. curses on *nix). The framework complies with
the conventional structure of test cases bundled into suites which are
registered with the framework for running.

%package devel
Summary:	Header files and develpment documentation for bcunit
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and develpment documentation for bcunit.

%package static
Summary:	Static bcunit library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static bcunit library.

%prep
%setup -q -n BCunit-%{version}-Source
%patch0 -p1

%build
install -d build
cd build
%{cmake} \
	-DENABLE_STATIC=OFF \
	-DENABLE_AUTOMATED=ON \
	-DENABLE_BASIC=ON \
	-DENABLE_CONSOLE=ON \
	-DENABLE_CURSES=ON \
	-DENABLE_EXAMPLES=ON \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libbcunit.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libbcunit.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbcunit.so
%{_includedir}/BCUnit
%{_pkgconfigdir}/bcunit.pc
%{_datadir}/BCunit
