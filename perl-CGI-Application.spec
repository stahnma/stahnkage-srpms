Name:           perl-CGI-Application
Version:        4.21
Release:        1%{?dist}
Summary:        Framework for building reusable web-applications

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/CGI-Application
Source0:        http://www.cpan.org/modules/by-module/CGI/CGI-Application-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
# Correct for lots of packages, other common choices include eg. Module::Build
BuildRequires:  perl(ExtUtils::MakeMaker), perl(HTML::Template)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
GI::Application - Framework for building reusable web-applications

%prep
%setup -q -n CGI-Application-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Examples
# For noarch packages: vendorlib
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Mar 17 2009 <stahnma@fedoraproject.org> - 4.21
- Initial Package
