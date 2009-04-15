Summary:	Package that uses webapps configuration
Summary(pl.UTF-8):	Pakiet używający konfiguracji aplikacji WWW
Name:		phpids
Version:	0.5.4
Release:	0.3
License:	LGPL v3
Group:		Applications/WWW
Source0:	http://www.php-ids.org/files/%{name}-%{version}.tar.bz2
# Source0-md5:	e62e0ab3a55d904dfeba72f545d4bc1f
Source1:	https://svn.php-ids.org/svn/trunk/lib/IDS/default_filter.xml
# Source1-md5:	2624dc503acc64b7081b49c8e28cb040
Patch0:		%{name}.patch
URL:		http://www.php-ids.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-common >= 4:5.2.8-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# _phpdocdir / php_docdir / phpdoc_dir ?
%define		_phpdocdir		%{_docdir}/phpdoc

%description
This .spec is for demonstrating triggers used for linking webapp
configuration to webserver config dir.

%package phpdoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	php-dirs

%description phpdoc
Documentation for %{name}.

%description phpdoc -l pl.UTF-8
Dokumentacja do %{name}.

%prep
%setup -q
find '(' -name '*.php' -o -name '*.ini' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1

# skip overwrite if not newer
if [ %{SOURCE1} -nt lib/IDS/default_filter.xml ]; then
	cp -a %{SOURCE1} lib/IDS/default_filter.xml
fi

rm -rf lib/IDS/vendors/htmlpurifier
rmdir lib/IDS/vendors
mv lib/IDS/tmp/*.txt .
rm -rf lib/IDS/tmp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{php_data_dir},%{_phpdocdir}/%{name}-%{version}}
cp -a docs/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a docs/phpdocumentor/* $RPM_BUILD_ROOT%{_phpdocdir}/%{name}-%{version}
cp -a lib/IDS $RPM_BUILD_ROOT%{php_data_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc phpids_log.txt
%{php_data_dir}/IDS
%{_examplesdir}/%{name}-%{version}

%files phpdoc
%defattr(644,root,root,755)
%{_phpdocdir}/%{name}-%{version}
