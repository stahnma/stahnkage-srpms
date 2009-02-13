Name:           perl-vmware
Version:        1.0.0
Release:        2%{?dist}
Summary:        Perl scripting interface to the VMware Infrastructure API

Group:          Development/Libraries
License:        Commercial
URL:            http://www.vmware.com/support/developer/viperltoolkit/
Source0:        VMware-VIPerl-Toolkit-%{version}-source.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) 
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl(VMware::VIM2Runtime) = %{version}-%{release}
Provides:       perl(VMware::VIM2Stub) = %{version}-%{release}

#TODO put *.pl files in libexec and then link in bindir without .pl extension
# fix provides
# create app util directory
%description
None.

%prep
%setup -q -n viperltoolkit
pushd apps/vm
# Make it so it defaults to /etc/vmware for configs and such
#  rather than a relative ../
%{__sed} -i 's/"\.\./"\/etc\/vmware/g' *
popd
# Change so that things are not 755 all over
find . -type f -exec chmod 644 {} \;
# Fix line feed issues
for file in `find doc -type f -name \*.pl -or -name  \*.pm -or -name \*.txt -or -name \*.xml -or -name \*.html -or -name \*.css`
do
  %{__sed} -i 's/\r//'  $file
done
#  Fix the ones not in doc 
%{__sed} -i 's/\r//'  readme.html sdkpubs.css EULA.txt Changes



%build
# Remove OPTIMIZE=... from noarch packages (unneeded)
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# now add the .pm files that don't get auto-packaged by the Makefile
cd apps/AppUtil
install -p -m644  *.pm $RPM_BUILD_ROOT%{perl_vendorlib}/
cd ../..
# The make install doesn't include the actual apps...how odd
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/vmware/{sampledata,schema}
cd apps/vm
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m755 * $RPM_BUILD_ROOT%{_bindir}
cd ../schema
install -p -m644 * $RPM_BUILD_ROOT%{_sysconfdir}/vmware/schema
cd ../sampledata
install -p -m644 * $RPM_BUILD_ROOT%{_sysconfdir}/vmware/sampledata
cd


# Now we fix rpmlint errors
for file in `find $RPM_BUILD_ROOT -type f -name \*.pl -or -name  \*.pm -or -name \*.txt -or -name \*.xml -or -name \*.html`
do
  %{__sed} -i 's/\r//'  $file
done


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc readme.html Changes EULA.txt sdkpubs.css
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/vmware

%changelog
* Fri Feb 13 2009 <michael.stahnke@cat.com> - 1.0.0-2
- Complete rebuild
