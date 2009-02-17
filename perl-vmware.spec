%define realversion 1.6.0-104313
Name:           perl-vmware
Version:        1.6.0_104313
Release:        1%{?dist}
Summary:        Perl scripting interface to the VMware Infrastructure API

Group:          Development/Libraries
License:        Commercial
URL:            http://www.vmware.com/support/developer/viperltoolkit/
Source0:        VMware-VIPerl-%{realversion}.x86_64.tar.gz
AutoReq:        no


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
# Perl(UUID) not available in Fedora/EPEL (due to license) see my git -- stahnma
BuildRequires:  perl(ExtUtils::MakeMaker) , perl(Class::MethodMaker), perl(Crypt::SSLeay), perl(SOAP::Lite), perl(XML::LibXML), perl(UUID)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Archive::Zip), perl(Data::Dump), perl(UUID)

#TODO Install applications 
# configure apps for /etc/ usage


%description
None.

%prep
%setup -q -n vmware-viperl-distrib
# Fix line feed issues
find . -type f -name \*.pl -or -name \*.pm -or -name \*.txt -or -name \*.xml -or -name \*.html -or -name \*.css |xargs  %{__sed} -i 's/\r//' 
# This file doesn't get picked up that way
%{__sed} -i 's/\r//' doc/EULA
# This file has no use
rm -f vmware-install.pl
#Change so that things are not 755 all over
find . -type f -exec chmod 644 {} \;


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{perl_vendorlib}/AppUtil
ls
pushd apps/AppUtil
install -p -m644 *.pm $RPM_BUILD_ROOT/%{perl_vendorlib}/AppUtil
popd
# Install AppUtil stuff (not in Makefile)
mkdir -p $RPM_BUILD_ROOT/

#Change so that things are not 755 all over
find $RPM_BUILD_ROOT -type f -exec chmod 644 {} \;

# Install things in the applicaitons directory
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/%{name}
pushd apps
 # Don't install AppUtil, as we already have 
 # also, sampledata and schema are configuration files, they belong in etc
ls | egrep -v 'AppUtil|sampledata|schema' | while read dir;  do
  mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/$dir
  pushd $dir
  install  -p -m755 * $RPM_BUILD_ROOT/%{_libexecdir}/%{name}/$dir
  popd
done 
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/schema
pushd schema
  install -p -m644 * $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/schema
popd
popd


%check
#make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc readme.html Changes EULA.txt sdkpubs.css apps/sampledata
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*
%{_libexecdir}/%{name}
#%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}

%changelog
* Fri Feb 14 2009 <stahnma@fedoraproject.org> - 1.6.0_104313-1
- Complete rebuild of spec
