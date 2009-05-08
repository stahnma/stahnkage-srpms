%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

# Figure out Oracle version and make a good guess at $ORACLE_HOME
%global oracle_ver %(ls -1 %{_includedir}/oracle | grep 10 | tail -1 )
# Show Oracle HOME
%global oracle_home %{_libdir}/oracle/%oracle_ver/client/lib

%global pecl_name oci8

Name:           php-pecl-oci8
Version:        1.3.5
Release:        1%{?dist}
Summary:        PHP Extension for Oracle Database

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/oci8
Source0:        http://pecl.php.net/get/oci8-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel php-pear >= 1:1.4.9-1.2
BuildRequires:  oracle-instantclient-devel,oracle-instantclient-basic
Provides:       php-pecl(oci8) = %{version}

%if %{?php_zend_api}0
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
# for EL-5
Requires:       php-api = %{php_apiver}
%endif
Requires:       oracle-instantclient-basic

%description
This extension allows you to access Oracle databases using the Oracle
Call Interface (OCI8). It can be built with PHP 4.3.9 to 5.x. It can 
be linked with Oracle 9.2, 10.2 or 11.1 client libraries.

%prep
%setup -qcn oci8-%{version}
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml
cd oci8-%{version}


%build
cd oci8-%{version}
phpize
%configure --with-oci8=instantclient,%oracle_home 
make %{?_smp_mflags}


%install
cd oci8-%{version}
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/oci8.ini << 'EOF'
; Enable oci8 extension module
extension=oci8.so
EOF

# Install XML package description
install -d $RPM_BUILD_ROOT%{pecl_xmldir}
install -pm 644 %{pecl_name}.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc oci8-%{version}/CREDITS oci8-%{version}/README
%config(noreplace) %{_sysconfdir}/php.d/oci8.ini
%{php_extdir}/oci8.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Tue May 05 2009 Michael Stahnke <stahnma@fedoraproject.org> 1.3.5-1
- Initial Package
