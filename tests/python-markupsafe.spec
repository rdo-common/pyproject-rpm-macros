Name:           python-markupsafe
Version:        2.0.1
Release:        0%{?dist}
Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
License:        BSD
URL:            https://github.com/pallets/markupsafe
Source0:        %{url}/archive/%{version}/MarkupSafe-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
This package installs test- and docs-requirements from files
and uses them to run tests and build documentation.


%package -n python3-markupsafe
Summary:        %{summary}

%description -n python3-markupsafe
...

%prep
%autosetup -n markupsafe-%{version}

# we don't have pip-tools packaged in Fedora yet
sed -i /pip-tools/d requirements/dev.in


%generate_buildrequires
# requirements/dev.in recursively includes tests.in and docs.in
# we also list tests.in manually to verify we can pass multiple arguments,
# but it should be redundant if this was a real package
%pyproject_buildrequires -r requirements/dev.in requirements/tests.in


%build
%pyproject_wheel
%make_build -C docs html SPHINXOPTS='-n %{?_smp_mflags}'


%install
%pyproject_install
%pyproject_save_files markupsafe


%check
%pytest


%files -n python3-markupsafe -f %{pyproject_files}
%license LICENSE.rst
%doc CHANGES.rst README.rst