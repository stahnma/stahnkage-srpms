Name:           websages-repo
Version:        0
Release:        1%{?dist}
Summary:        Packages for WebSages

Group:          System Environment/Base
License:        GPLv2+
URL:            http://websages.com
Source0:        http://www.jameswhite.org/~james/websages.com_trustchain.pem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Perhaps require EPEL if 5?
# Pehaps  not

%description
None.

%prep
cp %{SOURCE0} .


%build


%install
rm -rf $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc



%changelog
