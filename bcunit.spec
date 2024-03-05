#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Provide C programmers basic testing functionality
Summary(pl.UTF-8):	Podstawowa funkcjonalność testów dla programistów C
Name:		bcunit
Version:	5.3.26
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcunit/tags
Source0:	https://gitlab.linphone.org/BC/public/bcunit/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	9d428059bc8b636d0ca41e1b443b2117
Patch0:		lib.patch
Patch1:		%{name}-examples.patch
Patch2:		%{name}-format.patch
Patch3:		%{name}-ncurses.patch
URL:		https://linphone.org/
BuildRequires:	cmake >= 3.22
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BCUnit is a unit testing framework for C, derived from CUnit. (B)CUnit
provides various interfaces to the framework, some of which are
platform dependent (e.g. curses on *nix). The framework complies with
the conventional structure of test cases bundled into suites which are
registered with the framework for running.

%description -l pl.UTF-8
BCUnit to szkielet testów jednostkowych dla C, wywodzący się z CUnit.
(B)CUnit zapewnia różne interfejsy do szkieletu, niektóre z nich są
zależne od platformy (np. curses na systemach uniksowych). Szkielet
jest zgodny z konwencjonalną strukturą przypadków testowych
zgrupowanych w zestawy, które są rejestrowane do uruchomienia.

%package devel
Summary:	Header files for BCUnit library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki BCUnit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for BCUnit library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki BCUnit.

%package static
Summary:	Static BCunit library
Summary(pl.UTF-8):	Statyczna biblioteka BCUnit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static BCUnit library.

%description static -l pl.UTF-8
Statyczna biblioteka BCUnit.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# sources contain "build" directory, so use alternative builddir
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DENABLE_BCUNIT_AUTOMATED=ON \
	-DENABLE_BCUNIT_BASIC=ON \
	-DENABLE_BCUNIT_CONSOLE=ON \
	-DENABLE_BCUNIT_CURSES=ON

%{__make} -C builddir-static
%endif

%cmake -B builddir \
	-DENABLE_BCUNIT_AUTOMATED=ON \
	-DENABLE_BCUNIT_BASIC=ON \
	-DENABLE_BCUNIT_CONSOLE=ON \
	-DENABLE_BCUNIT_CURSES=ON \
	-DENABLE_BCUNIT_DOC=ON \
	-DENABLE_BCUNIT_EXAMPLES=ON

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged in includedir / as %doc
#{__rm} -r $RPM_BUILD_ROOT%{_docdir}/BCUnit

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/BCUnit/Examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md TODO
%attr(755,root,root) %{_libdir}/libbcunit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbcunit.so.1
%dir %{_datadir}/BCUnit
%{_datadir}/BCUnit/BCUnit*.dtd
%{_datadir}/BCUnit/BCUnit*.xsl
%{_datadir}/BCUnit/Memory-Dump.dtd
%{_datadir}/BCUnit/Memory-Dump.xsl

%files devel
%defattr(644,root,root,755)
%doc doc/*.{css,html}
%attr(755,root,root) %{_libdir}/libbcunit.so
%{_includedir}/BCUnit
%{_pkgconfigdir}/bcunit.pc
%{_datadir}/BCUnit/cmake
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man3/BCUnit.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbcunit.a
%endif
