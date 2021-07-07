%global debug_package %{nil}

# always bootstrap: otherwise rebuild fails
%bcond_without boot

%bcond_with test

# causes /usr/lib/.build-id file conflict with racket-minimal
%bcond_with racket

Name:           idris2
Version:        0.4.0
Release:        2%{?dist}
Summary:        Purely functional programming language with first class types

License:        BSD
URL:            https://www.idris-lang.org/
Source0:        https://www.idris-lang.org/idris2-src/%{name}-%{version}.tgz
# simplified https://github.com/idris-lang/Idris2/pull/1123
Patch0:         idris2-0.4-DESTDIR.patch

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make
%if %{without boot}
BuildRequires:  idris2
%endif
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
%patch0 -p1 -b .destdir

grep /usr/bin/chezscheme9.5  bootstrap/idris2_app/idris2.ss && sed -i -e "s!/usr/bin/chezscheme9.5!/usr/bin/scheme!" bootstrap/idris2_app/idris2.ss


%build
%global idris_prefix %{_libdir}/%{name}

%if %{with boot}
make %{?with_racket:bootstrap-racket}%{!?with_racket:bootstrap SCHEME=scheme} PREFIX=%{idris_prefix}
%else
make
%endif


%install
export PATH=%{buildroot}%{idris_prefix}/bin:$PATH
# FIXME: warning: Duplicate build-ids:
# /usr/lib64/idris2/bin/idris2_app/libidris2_support.so
# /usr/lib64/idris2/lib/libidris2_support.so
make install-idris2 install-support DESTDIR=%{buildroot} PREFIX=%{idris_prefix}
make install-with-src-libs DESTDIR=%{buildroot} PREFIX=%{idris_prefix}
make install-api PREFIX=%{idris_prefix} IDRIS2_PACKAGE_PATH=%{buildroot}%{idris_prefix}/%{name}-%{version} IDRIS2_PREFIX=%{buildroot}%{idris_prefix}

%if %{without racket}
chmod a-x %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez
%endif
#sed -i -e "s!%{buildroot}!!" %{buildroot}%{idris_prefix}/bin/idris2_app/%{!?with_racket:idris2.ss}%{?with_racket:idris2.rkt}

chmod -R a=,+rwX %{buildroot}%{idris_prefix}/%{name}-%{version}

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{idris_prefix}/bin/idris2 --bash-completion-script %{name} > %{buildroot}%{_datadir}/bash-completion/completions/%{name}

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
%{_datadir}/bash-completion/completions/%{name}


%changelog
* Wed Jul  7 2021 Jens Petersen <petersen@redhat.com> - 0.4.0-2
- install-with-src-libs and install-api
- add bash-completion

* Tue Jul  6 2021 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- add DESTDIR patch

* Tue Jun 23 2020 Jens Petersen <petersen@redhat.com>
- initial packaging try
