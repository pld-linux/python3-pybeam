#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pybeam
Summary:	Python module to parse Erlang BEAM files
Name:		python3-%{module}
Version:	0.8.1
Release:	1
License:	MIT
Group:		Libraries/Python
# PyPI sdist lacks doc/
Source0:	https://github.com/matwey/pybeam/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	a9fdb3979647128a29cf39d7817e1e4a
URL:		https://github.com/matwey/pybeam
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:61.0
%if %{with tests} || %{with doc}
BuildRequires:	python3-construct >= 2.9
BuildRequires:	python3-construct < 2.11
%endif
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python module to parse Erlang BEAM files.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest test
%endif

%if %{with doc}
sphinx-build-3 -b html doc/ build/doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%dir %{py3_sitescriptdir}/%{module}/schema
%{py3_sitescriptdir}/%{module}/schema/*.py
%{py3_sitescriptdir}/%{module}/schema/__pycache__
%dir %{py3_sitescriptdir}/%{module}/schema/beam
%{py3_sitescriptdir}/%{module}/schema/beam/*.py
%{py3_sitescriptdir}/%{module}/schema/beam/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/*
%endif
