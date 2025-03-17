#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pybeam
Summary:	Python module to parse Erlang BEAM files
Name:		python3-%{module}
Version:	0.7
Release:	4
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pybeam/
Source0:	https://files.pythonhosted.org/packages/source/p/pybeam/%{module}-%{version}.tar.gz
# Source0-md5:	4759e2e15052e1254cddaa0da604c957
URL:		https://pypi.org/project/pybeam/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-construct
BuildRequires:	python3-six
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
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
%py3_build %{?with_tests:test}

%if %{with doc}
sphinx-build-3 -b html doc/ build/doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

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
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/*
%endif
