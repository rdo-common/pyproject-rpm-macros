Name:           pyproject-rpm-macros
Summary:        RPM macros for PEP 517 Python packages
License:        MIT

%bcond_without tests

# Keep the version at zero and increment only release
Version:        0
Release:        5%{?dist}

Source0:        macros.pyproject
Source1:        pyproject_buildrequires.py

Source8:        README.md
Source9:        LICENSE

Source10:       test_pyproject_buildrequires.py
Source11:       testcases.yaml

URL:            https://src.fedoraproject.org/rpms/pyproject-rpm-macros

BuildArch:      noarch

Requires: python3-pip >= 19
Requires: python3-devel

# We keep these here for now to avoid one loop of %%generate_buildrequires
# But those are also always in the output of %%generate_buildrequires
# in order to be removable in the future
Requires: python3dist(packaging)
Requires: python3dist(pytoml)

# This is not output from %%generate_buildrequires to work around:
#   https://github.com/rpm-software-management/mock/issues/336
Requires: (python3dist(importlib-metadata) if python3 < 3.8)

%if %{with tests}
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(pyyaml)
BuildRequires: python3dist(packaging)
%if 0%{fedora} < 32
# The %%if should not be needed, it works around:
#   https://github.com/rpm-software-management/mock/issues/336
BuildRequires: (python3dist(importlib-metadata) if python3 < 3.8)
%endif
BuildRequires: python3dist(pytoml)
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(tox-current-env) >= 0.0.2
BuildRequires: python3dist(wheel)
%endif


%description
This is a provisional implementation of pyproject RPM macros for Fedora 30+.
These macros are useful for packaging Python projects that use the PEP 517
pyproject.toml file, which specifies the package's build dependencies
(including the build system, such as setuptools, flit or poetry).


%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%build
# nothing to do, sources are not buildable

%install
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_rpmconfigdir}/redhat
install -m 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
install -m 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/redhat/

%if %{with tests}
%check
%{__python3} -m pytest -vv
%endif


%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/redhat/pyproject_buildrequires.py

%doc README.md
%license LICENSE

%changelog
* Fri Jul 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0-5
- Allow to fetch test dependencies from tox
- Add %%tox macro to invoke tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-3
- Add %%pyproject_buildrequires

* Tue Jul 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0-2
- Fix shell syntax errors in %%pyproject_install
- Drop PATH warning in %%pyproject_install

* Fri Jun 28 2019 Patrik Kopkan <pkopkan@redhat.com> - 0-1
- created package
