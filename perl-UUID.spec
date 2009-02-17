Name:           perl-UUID
Version:        0.03
Release:        1%{?dist}
Summary:        Perl extension for using UUID interfaces as defined in e2fsprogs
License:        Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/UUID/
Source0:        http://www.cpan.org/modules/by-module/UUID/UUID-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  e2fsprogs-devel
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
With these 3 routines UUID's can easily be generated and parsed/un-parsed.

%prep
%setup -q -n UUID-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes License
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/UUID*
%{_mandir}/man3/*

%changelog
* Mon Feb 16 2009 <stahnma@fedoraproject.org> 0.03-1
- Initial build
