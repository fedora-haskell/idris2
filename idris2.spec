# causes strip errors: cannot set time for file
#%%global debug_package %%{nil}

# always bootstrap: otherwise rebuild fails
%bcond_without boot

%bcond_without docs

# requires network?
%bcond_with test

%bcond_with racket

%if %{with racket}
# /usr/lib/.build-id file for bin/idris2 conflicts with racket-minimal starter
%define _build_id_links alldebug
%endif

Name:           idris2
Version:        0.6.0
Release:        0.2%{?dist}
Summary:        Purely functional programming language with first class types

License:        BSD
URL:            https://www.idris-lang.org/
Source0:        https://www.idris-lang.org/idris2-src/%{name}-%{version}.tgz
#Source1:        idris2.sh
# simplified https://github.com/idris-lang/Idris2/pull/1123
Patch0:         idris2-DESTDIR.patch
Patch1:         idris-Package-destdir.patch

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make
%if %{without boot}
BuildRequires:  idris2
%endif
%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
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
Requires:       %{name}-lib%{?_isa} = %{version}-%{release}

%description
Idris is a programming language designed to encourage Type-Driven Development.


%if %{with docs}
%package docs
Summary:        Idris2 documentation

%description docs
The package contains the idris2 manual
%endif


%package lib
Summary:        idris2 runtime support library

%description lib
The package provide the runtime support library for idris2.


%prep
%setup -q -n Idris2-%{version}
%patch -P0 -p1 -b .destdir
%patch -P1 -p1 -b .destdir

grep /usr/local/bin/scheme bootstrap/idris2_app/idris2.ss && sed -i -e "s!/usr/local/bin/scheme!/usr/bin/scheme!" bootstrap/idris2_app/idris2.ss


%build
%global idris_prefix %{_libdir}/%{name}

%if %{with boot}
make %{?with_racket:bootstrap-racket}%{!?with_racket:bootstrap SCHEME=scheme} PREFIX=%{idris_prefix}
%else
make
%endif

%if %{with docs}
make -C docs html
%endif


%install
export PATH=%{buildroot}%{idris_prefix}/bin:$PATH
make install DESTDIR=%{buildroot} PREFIX=%{idris_prefix}

# # FIXME: warning: Duplicate build-ids:
# # /usr/lib64/idris2/bin/idris2_app/libidris2_support.so
# # /usr/lib64/idris2/lib/libidris2_support.so
# make install-idris2 install-support DESTDIR=%{buildroot} PREFIX=%{idris_prefix}
# make install-with-src-libs DESTDIR=%{buildroot} PREFIX=%{idris_prefix}
# #make install-api PREFIX=%{idris_prefix} IDRIS2_PACKAGE_PATH=%{buildroot}%{idris_prefix}/%{name}-%{version} IDRIS2_PREFIX=%{buildroot}%{idris_prefix}

# mkdir -p %{buildroot}%{_bindir}
# mv %{buildroot}%{idris_prefix}/bin/idris2_app/idris2 %{buildroot}%{_bindir}/
# rm -r %{buildroot}%{idris_prefix}/bin
mv %{buildroot}%{idris_prefix}/lib/libidris2_support.so %{buildroot}%{_libdir}
rm %{buildroot}%{idris_prefix}/%{name}-%{version}/lib/libidris2_support.so
rm %{buildroot}%{idris_prefix}/bin/idris2_app/libidris2_support.so

# #sed -i -e "s!%{buildroot}!!" %{buildroot}%{idris_prefix}/bin/idris2_app/%{!?with_racket:idris2.ss}%{?with_racket:idris2.rkt}
# # %if %{without racket}
# # rm %{buildroot}%{idris_prefix}/bin/idris2_app/compileChez
# # %else
# # rm %{buildroot}%{idris_prefix}/bin/idris2_app/idris2-boot*
# # %endif
# # WARNING: ./usr/lib64/idris2/bin/idris2_app/idris2.rkt is executable but has no shebang, removing executable bit
# #rm %{buildroot}%{idris_prefix}/bin/idris2_app/{idris2*.ss,idris2.rkt}

mkdir %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{name}/bin/idris2 %{buildroot}%{_bindir}

#chmod -R a=,+rwX %%{buildroot}%%{idris_prefix}/%%{name}-%%{version}

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
LD_LIBRARY_PATH="%{buildroot}%{_libdir}:" %{buildroot}%{_bindir}/idris2 --bash-completion-script %{name} | sed "s/dirnames/default/" > %{buildroot}%{_datadir}/bash-completion/completions/%{name}

#install %{SOURCE1} %{buildroot}%{_bindir}/idris2
#sed -i -e 's!@IDRIS2_PREFIX@!%{idris_prefix}!' %{buildroot}%{_bindir}/idris2


%if %{with test}
%check
make test
%endif


%files
%license LICENSE
%doc *.md
%doc www/source/index.md
%{_bindir}/idris2
%{idris_prefix}
#%%{_libdir}/%%{name}-%%{version}
%{_datadir}/bash-completion/completions/%{name}


%if %{with docs}
%files docs
%doc docs/build/html
%doc samples
%endif


%files lib
%{_libdir}/libidris2_support.so


%changelog
* Sat Aug 19 2023 Jens Petersen <petersen@redhat.com> - 0.6.0-0.1
- update to 0.6.0
  https://github.com/idris-lang/Idris2/blob/v0.6.0/CHANGELOG.md
- revert to chez-scheme

* Mon Sep 20 2021 Jens Petersen <petersen@redhat.com> - 0.5.1-1
- update to 0.5.1

* Sat Sep  4 2021 Jens Petersen <petersen@redhat.com> - 0.4.0-3
- use the racket backend for codegen
- move main idris binary to bindir and libidris2_support.so to libdir
  and IDRIS2_PREFIX is now libdir (this all mimics the AUR packaging)
- drop rest of bindir files and libidris2_support.so copies
- drop idris-api package for now

* Thu Jul  8 2021 Jens Petersen <petersen@redhat.com>
- remove bootstrapping files from bin/idris2_app/
- change bash-completion from dirnames to default

* Wed Jul  7 2021 Jens Petersen <petersen@redhat.com> - 0.4.0-2
- install-with-src-libs and install-api
- add bash-completion

* Tue Jul  6 2021 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- add DESTDIR patch

* Tue Jun 23 2020 Jens Petersen <petersen@redhat.com>
- initial packaging try
