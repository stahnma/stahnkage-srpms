Name:           oracle-instantclient                                                                                              
Version:        10.2.0.4                                                                                                          
Release:        1%{?dist}                                                                                                         
Summary:        Virtual Package for Oracle Instantclients                                                                         

Group:          Applications/Databases
License:        BSD
URL:            http://github.com/stahnma/stahnkage-srpms
Source0:        README.oracleinstantclient
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       oracle-instantclient-basic, oracle-instantclient-devel
Requires:       oracle-instantclient-sqlplus
BuildArch:      noarch
# The whole purpose of this RPM is to provide this library.  The Oracle instantclient
#   rpms *should*, however, they don't.  So, I wrote a provider dummy RPM.
Provides:       libclntsh.so.10.1

%description
Provides the libclntsh.so.10.1 to the RPM database.

%prep
cp -f %{SOURCE0} .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.oracleinstantclient

%changelog
* Fri May 08 2009 <stahnma@fedoraproject.org> - 10.2.0.4-1
- Initial Package
