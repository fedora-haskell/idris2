%global debug_package %{nil}

Name:           idris2
Version:        0.3.0
Release:        1%{?dist}
Summary:        Purely functional programming language with first class types

License:        BSD
URL:            https://www.idris-lang.org/
Source0:        https://www.idris-lang.org/idris2-src/%{name}-%{version}.tgz

# needed for testsuite
BuildRequires:  clang
BuildRequires:  chez-scheme
Requires:       chez-scheme

%description
Idris is a programming language designed to encourage Type-Driven Development.

%prep
%setup -q -n Idris2-%{version}


%build
%global idris_prefix %{_libdir}/%{name}

make bootstrap SCHEME=scheme PREFIX=%{buildroot}%{idris_prefix}


%install
export PATH=$PATH:%{buildroot}%{idris_prefix}/bin
make install PREFIX=%{buildroot}%{idris_prefix}

sed -i -e "s!$PWD/build/exec!%{idris_prefix}/bin!" %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez
sed -i -e "s!%{buildroot}!!" %{buildroot}%{idris_prefix}/bin/idris2_app/idris2.ss
#sed -i -e 's%!/bin/sh%!/usr/bin/sh%' %{buildroot}%{idris_prefix}/bin/idris2

#%{buildroot}%{idris_prefix}/%{name}-%{version}/{refc,support}
chmod -R -x+X %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez

mkdir -p %{buildroot}%{_bindir}
ln -s %{idris_prefix}/bin/idris2 %{buildroot}%{_bindir}


%check
make test


%files
%license LICENSE
%doc docs
%{_bindir}/idris2
%{_libdir}/idris2


%changelog
* Tue Jun 23 2020 Jens Petersen <petersen@redhat.com>
- initial packaging
