%global debug_package %{nil}

%bcond_with test

%bcond_with racket

Name:           idris2
Version:        0.3.0
Release:        1%{?dist}
Summary:        Purely functional programming language with first class types

License:        BSD
URL:            https://www.idris-lang.org/
Source0:        https://www.idris-lang.org/idris2-src/%{name}-%{version}.tgz

%if %{with test}
BuildRequires:  clang
%endif
%if %{with racket}
BuildRequires:  racket
Requires:       racket
%else
BuildRequires:  chez-scheme
Requires:       chez-scheme
%endif

%description
Idris is a programming language designed to encourage Type-Driven Development.

%prep
%setup -q -n Idris2-%{version}


%build
%global idris_prefix %{_libdir}/%{name}

make %{?with_racket:bootstrap-racket}%{!?with_racket:bootstrap SCHEME=scheme} PREFIX=%{buildroot}%{idris_prefix}


%install
export PATH=%{buildroot}%{idris_prefix}/bin:$PATH
make install PREFIX=%{buildroot}%{idris_prefix}

%if %{without racket}
sed -i -e "s!$PWD/build/exec!%{idris_prefix}/bin!" %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez
chmod a-x %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez
%endif
sed -i -e "s!%{buildroot}!!" %{buildroot}%{idris_prefix}/bin/idris2_app/%{!?with_racket:idris2.ss}%{?with_racket:idris2.rkt}

sed -i -e '/^esac/a export IDRIS2_PREFIX=$(dirname $(dirname $DIR))' %{buildroot}%{idris_prefix}/bin/idris2

chmod -R a=,+rwX %{buildroot}%{idris_prefix}/%{name}-%{version}

mkdir -p %{buildroot}%{_bindir}
ln -s %{idris_prefix}/bin/idris2 %{buildroot}%{_bindir}


%if %{with test}
%check
make test
%endif


%files
%license LICENSE
%doc docs
%{_bindir}/idris2
%{_libdir}/idris2


%changelog
* Tue Jun 23 2020 Jens Petersen <petersen@redhat.com>
- initial packaging
