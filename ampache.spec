%define name    ampache 
%define version 3.5.4
%define release %mkrel 3

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

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc docs/*
%{_var}/www/%{name}
%config(noreplace) %{_webappconfdir}/%{name}.conf
