Name:           oracle-instantclient                                                                                              
Version:        11.2.0.1.0                                                                                                    
Release:        1%{?dist}                                                                                                         
Summary:        Virtual Package for Oracle Instantclients                                                                         

Group:          Applications/Databases
License:        BSD
URL:            http://github.com/stahnma/stahnkage-srpms/oracle-instantclient
Source0:        README.oracleinstantclient
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       oracle-instantclient-basic>10
Requires:       oracle-instantclient-devel>10
Requires:       oracle-instantclient-sqlplus>10
Requires:       oracle-instantclient-jdbc>10
Requires:       oracle-instantclient-odbc>10

BuildArch:      noarch
# The whole purpose of this RPM is to provide this library.  The Oracle instantclient
#   rpms *should*, however, they don't.  So, I wrote a provider dummy RPM.
# This is useful for things like perl-DBI-oracle, php-pecl-oci8, ruby-oci8, etc
Provides:       libclntsh.so = 11.1

%description
Provides the libclntsh.so to the RPM database.

%prep
cp -f %{SOURCE0} .

%build

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.oracleinstantclient

%changelog
* Thu May 27 2010 <stahnma@fedoraproject.org> - 11.2.0.1.0-1
- Updated package for 11g.

* Fri May 08 2009 <stahnma@fedoraproject.org> - 10.2.0.4-2
- Updated URL

* Fri May 08 2009 <stahnma@fedoraproject.org> - 10.2.0.4-1
- Initial Package
