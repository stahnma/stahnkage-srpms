# This package follows the Fedora Packaging Guidelines as closely as possible.
# This package is not able to be in Fedora because it has Oracle lib requirements.
# If you find issues with this spec file, let me know on github.
# This package requires another package I wrote call oracle-instantclient
#   because when you install you will need rpm to be aware of libclntsh.so.11.1

%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global realgemname ruby-oci8
%global gemname oci8
%global geminstdir %{gemdir}/gems/%{realgemname}-%{version}
%{!?ruby_sitearchdir: %global ruby_sitearchdir %(/usr/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Summary: Ruby interface for Oracle using OCI8 API
Name: rubygem-%{gemname}
Version: 1.0.7
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://ruby-oci8.rubyforge.org
Source0: %{realgemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# You will need to get oracle-instantclient11.2 packages from oracle.com
Requires: rubygems, ruby(abi) >= 1.8
Requires: oracle-instantclient >= 11.2
BuildRequires: rubygems, oracle-instantclient11.2-basic, oracle-instantclient11.2-devel
Provides: rubygem(%{gemname}) = %{version}

%description
rubygem-oci8 is a ruby interface for Oracle using OCI8 API. It is available with
Oracle8, Oracle8i, Oracle9i, Oracle10g, Oracle11g and Oracle Instant Client.

%prep 
%setup -q -c -T

%build
mkdir -p ./%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/11.2/client/lib/
gem install -V --local --install-dir ./%{gemdir} \
            --force --rdoc %{SOURCE0}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{ruby_sitearchdir}
# Remove duplicate copy of oci8lib.so
rm -f /usr/lib/ruby/gems/1.8/gems/ruby-oci8-1.0.7/ext/oci8/oci8lib.so
# Put so file in proper directory
mv %{buildroot}%{geminstdir}/lib/oci8lib.so %{buildroot}%{ruby_sitearchdir}
# Remove ext source code
rm -rf %{buildroot}%{geminstdir}/ext/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gemdir}/doc/%{realgemname}-%{version}
%doc %{geminstdir}/README
%doc %{geminstdir}/ChangeLog
%doc %{geminstdir}/NEWS
%doc %{geminstdir}/VERSION
%doc %{geminstdir}/Makefile
%doc %{gemdir}/gems/%{realgemname}-%{version}/doc
%doc %{geminstdir}/test
%doc %{geminstdir}/support
%dir %{gemdir}/gems/%{realgemname}-%{version}/
%{ruby_sitearchdir}/*.so
%{geminstdir}/*.gemspec
%{geminstdir}/dist-files
%{geminstdir}/lib
%{geminstdir}/metaconfig
%{geminstdir}/pre-distclean.rb
%{geminstdir}/*.spec
%{gemdir}/gems/%{realgemname}-%{version}/setup.rb
%{gemdir}/cache/%{realgemname}-%{version}.gem
%{gemdir}/specifications/*.gemspec

%changelog
* Tue Jul 06 2010  <stahnma@fedoraproject.org> - 1.0.7-1
- Initial package
