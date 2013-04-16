%define name    ampache 
%define version 3.5.4
%define release: 4

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Web-based MP3/Ogg/RM/Flac/WMA/M4A manager
License:        GPL
Group:		Networking/WWW
URL:            http://www.ampache.org
Source:		http://www.ampache.org/downloads/%{name}-%{version}.tar.gz
Patch0:		%name-browser.patch
Requires:	apache-mod_php
Requires:	php-iconv
Requires:	php-mysql
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Ampache is a Web-based MP3/Ogg/RM/Flac/WMA/M4A manager.
It allows you to view, edit, and play your audio files via HTTP/IceCast/Mpd 
or Moosic. It has support for downsampling, playlists, artist, 
and album views, album art, random play, song play tracking, user themes, 
and remote catalogs using XML-RPC.

%prep
%setup -q
%patch0 -p0

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/%{name}
cp -r * %{buildroot}%{_var}/www/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Ampache configuration

Alias /%{name} %{_var}/www/%{name}
<Directory %{_var}/www/%{name}>
    Order allow,deny
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc docs/*
%{_var}/www/%{name}
%config(noreplace) %{_webappconfdir}/%{name}.conf


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.5.4-3mdv2011.0
+ Revision: 609971
- rebuild

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.5.4-2mdv2010.1
+ Revision: 513190
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Feb 06 2010 Frederik Himpe <fhimpe@mandriva.org> 3.5.4-1mdv2010.1
+ Revision: 501330
- update to new version 3.5.4

* Sun Dec 27 2009 Frederik Himpe <fhimpe@mandriva.org> 3.5.3-1mdv2010.1
+ Revision: 482738
- update to new version 3.5.3

* Mon Jul 13 2009 Frederik Himpe <fhimpe@mandriva.org> 3.5.1-1mdv2010.0
+ Revision: 395571
- update to new version 3.5.1

* Wed Jun 10 2009 Funda Wang <fwang@mandriva.org> 3.5-1mdv2010.0
+ Revision: 384616
- New version 3.5

* Tue Jan 20 2009 Funda Wang <fwang@mandriva.org> 3.4.4-1mdv2009.1
+ Revision: 331620
- update to new version 3.4.4

* Sun Aug 31 2008 Funda Wang <fwang@mandriva.org> 3.4.3-1mdv2009.0
+ Revision: 277908
- update to new version 3.4.3

* Sun Jul 27 2008 Funda Wang <fwang@mandriva.org> 3.4.2-1mdv2009.0
+ Revision: 250493
- update to new version 3.4.2

* Sun Jun 01 2008 Funda Wang <fwang@mandriva.org> 3.4.1-1mdv2009.0
+ Revision: 214089
- New version 3.4.1

* Sun May 11 2008 Funda Wang <fwang@mandriva.org> 3.4-1mdv2009.0
+ Revision: 205440
- New version 3.4

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 3.3.3.5-2mdv2008.1
+ Revision: 170698
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Aug 20 2007 Erwan Velu <erwan@mandriva.org> 3.3.3.5-1mdv2008.0
+ Revision: 67200
- 3.3.3.5

* Fri Jul 27 2007 Funda Wang <fwang@mandriva.org> 3.3.3.4-1mdv2008.0
+ Revision: 56236
- New version 3.3.3.4

* Mon Jun 11 2007 Erwan Velu <erwan@mandriva.org> 3.3.3.3-1mdv2008.0
+ Revision: 38037
- 3.3.3.3

* Fri May 11 2007 Erwan Velu <erwan@mandriva.org> 3.3.3.2-1mdv2008.0
+ Revision: 26356
- 3.3.3.2

* Thu Apr 26 2007 Erwan Velu <erwan@mandriva.org> 3.3.3.1-1mdv2008.0
+ Revision: 18423
- Import ampache

