Name:           ampache
Version:        6.5.0
Release:        1
Summary:        Web-based MP3/Ogg/RM/Flac/WMA/M4A manager
License:        GPL
Group:		Networking/WWW
URL:            http://www.ampache.org
Source:		https://github.com/ampache/ampache/archive/refs/tags/%{version}.tar.gz
Requires:	apache-mod_php
Requires:	php-iconv
Requires:	php-mysql
BuildArch:      noarch

%description
Ampache is a Web-based MP3/Ogg/RM/Flac/WMA/M4A manager.
It allows you to view, edit, and play your audio files via HTTP/IceCast/Mpd 
or Moosic. It has support for downsampling, playlists, artist, 
and album views, album art, random play, song play tracking, user themes, 
and remote catalogs using XML-RPC.

%prep
%autosetup -p0

%install
install -d -m 755 %{buildroot}/srv/www/%{name}
cp -r * %{buildroot}/srv/www/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# Ampache configuration

Alias /%{name} /srv/www/%{name}
<Directory /srv/www/%{name}>
	Require all granted
</Directory>
EOF

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc docs/*
/srv/www/%{name}
%config(noreplace) %{_webappconfdir}/%{name}.conf
