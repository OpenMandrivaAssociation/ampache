%define name    ampache 
%define version 3.3.3.5
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Ampache is a Web-based MP3/Ogg/RM/Flac/WMA/M4A manager
License:        GPL
Group:		Networking/WWW
URL:            http://www.ampache.org
Source:		http://www.ampache.org/downloads/%{name}-%{version}.tar.bz2
Patch0:		%name-browser.patch
Requires:	apache, mysql, apache-mod_php, php-mysql, php-iconv
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16-2mdv2007.0
Requires(postun):	rpm-helper >= 0.16-2mdv2007.0
BuildRequires:	rpm-helper >= 0.16-2mdv2007.0
BuildRequires:	rpm-mandriva-setup >= 1.23-1mdv2007.0
BuildArch:      noarch

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
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc docs/*
%{_var}/www/%{name}
%config(noreplace) %{_webappconfdir}/%{name}.conf
