Name:		ampache
Version:	8.4.0
Release:	1
Summary:	Web-based audio and video streaming catalog
License:	AGPL-3.0
Group:		Networking/WWW
URL:		https://www.ampache.org
# GitHub tag archive. The top-level directory is ampache-8.4.0.
Source0:	https://github.com/ampache/ampache/archive/refs/tags/%{version}.tar.gz#/ampache-%{version}.tar.gz
# composer install --no-dev --prefer-dist --no-interaction --no-scripts --optimize-autoloader
# getID3's bundled Windows helper binaries are omitted.
Source1:	ampache-%{version}-vendor.tar.xz
# npm ci && npm run build. public/dist, public/lib/components and the
# material-symbols icons. Rolldown's native binding is not shipped.
Source2:	ampache-%{version}-assets.tar.xz
BuildArch:	noarch
Requires:	apache-mod_php
Requires:	php-cli
Requires:	php-curl
Requires:	php-dom
Requires:	php-gd
Requires:	php-iconv
Requires:	php-intl
Requires:	php-mbstring
Requires:	php-pdo_mysql
Requires:	php-zip
Recommends:	mariadb
Recommends:	php-ldap
Recommends:	php-sockets

%description
Ampache is a web-based audio and video streaming application. It
browses a local or remote catalog, with playlists, album art,
transcoding, and the Ampache, Subsonic and optional Jellyfin APIs.

The site is published at /ampache. The Apache web root is
/srv/www/ampache/public. Open /ampache/ to run the installer, which
writes config/ampache.cfg.php. Catalog and admin commands are
`php /srv/www/ampache/bin/cli`.

%prep
%autosetup -n ampache-%{version}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}

%build

%install
install -d %{buildroot}/srv/www/ampache
cp -a bin config locale public src vendor %{buildroot}/srv/www/ampache/
rm -rf %{buildroot}/srv/www/ampache/locale/base
rm -f %{buildroot}/srv/www/ampache/bin/*.bat
install -d %{buildroot}/srv/www/ampache/resources
cp -a resources/images resources/sql resources/templates \
	%{buildroot}/srv/www/ampache/resources/

find %{buildroot}/srv/www/ampache -type d -exec chmod 0755 {} +
find %{buildroot}/srv/www/ampache -type f -exec chmod 0644 {} +
sed -i '1s|^#!/usr/bin/env php|#!/usr/bin/php|' \
	%{buildroot}/srv/www/ampache/bin/cli \
	%{buildroot}/srv/www/ampache/bin/installer
chmod 0755 %{buildroot}/srv/www/ampache/bin/cli \
	%{buildroot}/srv/www/ampache/bin/installer
chmod 2775 %{buildroot}/srv/www/ampache/config

# Prefix rewrite targets for Alias /ampache, matching the installer's web_path.
prefix_htaccess() {
	sed -E '/^[[:space:]]*#/b; /^[[:space:]]*RewriteRule[[:space:]]/ s#(RewriteRule[[:space:]]+[^[:space:]]+[[:space:]]+)/#\1/%{name}/#' "$1" > "$2"
	chmod 0664 "$2"
}
app=%{buildroot}/srv/www/ampache/public
prefix_htaccess "$app/.htaccess.dist" "$app/.htaccess"
prefix_htaccess "$app/play/.htaccess.dist" "$app/play/.htaccess"
prefix_htaccess "$app/rest/.htaccess.dist" "$app/rest/.htaccess"
prefix_htaccess "$app/jellyfin/.htaccess.dist" "$app/jellyfin/.htaccess"
prefix_htaccess "$app/rss/.htaccess.dist" "$app/rss/.htaccess"
prefix_htaccess "$app/daap/.htaccess" "$app/daap/.htaccess.new"
mv "$app/daap/.htaccess.new" "$app/daap/.htaccess"

install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/ampache.conf <<'EOF'
# Web root is public/. src, vendor, config and resources are not published.
Alias /ampache /srv/www/ampache/public

<Directory /srv/www/ampache/public>
	Options FollowSymLinks
	AllowOverride All
	Require all granted
	DirectoryIndex index.php

	SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1

	<FilesMatch "^\.|\.cfg\.php$|\.(bak|old|orig|save|swp|swo|sql|log|ini|neon|sh|dist|cache|md|lock)$">
		Require all denied
	</FilesMatch>
</Directory>

# php-fpm needs flushpackets=on (see upstream docs/examples/apache-site.conf).
# mod_php does not. no-gzip still applies: mod_deflate would buffer the
# catalog progress stream until the scan finishes.
<Directory /srv/www/ampache/public/server>
	<Files "sse.server.php">
		SetEnv no-gzip 1
		SetEnv dont-vary 1
		php_flag zlib.output_compression Off
		php_flag implicit_flush On
		php_value output_buffering 0
	</Files>
</Directory>
EOF

install -d -m 0775 %{buildroot}/var/log/ampache

%files
%defattr(-,root,www,-)
%doc README.md LICENSE.md docs
/srv/www/ampache
%config(noreplace) %attr(0644,root,root) %{_webappconfdir}/ampache.conf
%dir %attr(0775,www,www) /var/log/ampache
