#!/bin/bash
# iIPTVPanel.com Installation on Debian OS
clear
echo "Welcome to iIPTV Panel Basic v1.2.1 Installation Script"
echo "We currently support only Debian"
echo "More Information on www.iIPTVPanel.com"
green='\e[0;32m'
NC='\e[0m' # No Color
VER=$(exec uname -m|grep 64)
if [ "$VER" = "" ]
then VER="x86"
else VER="x64"
fi
OS=$(cat /etc/debian_version)
if [ "$OS" = "" ]
then
echo "Your Operating System is NOT supported!"
echo "We currently support ONLY Debian Operating System"
exit 0
else
echo "Your System is Debian $OS - $VER"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
read -p "Please enter a password for your MySQL root user:" mysqlpassword
echo > /var/iIPTVPanel-Error.log
apt-get -y update > /dev/null 2>&1
apt-get -y install psmisc > /dev/null 2>&1
killall -9 apache2 > /dev/null 2>&1
killall -9 nginx > /dev/null 2>&1
apt-get -y install git > /dev/null 2>&1
apt-get -y install htop > /dev/null 2>&1
apt-get -y install unzip > /dev/null 2>&1
apt-get -y remove apache2 > /dev/null 2>&1
apt-get -y install build-essential libpcre3 libpcre3-dev libssl-dev make git > /dev/null 2>&1

echo "[+] Installing VLC"
echo 'deb http://http.debian.net/debian wheezy-backports main' >> /etc/apt/sources.list
apt-get -qq update > /dev/null 2>&1
apt-get upgrade -y > /dev/null 2>&1
apt-get -y -t wheezy-backports install vlc > /dev/null 2>&1

echo "[+] Installing Sudo"
apt-get -y install sudo > /dev/null 2>&1
echo 'www-data ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

echo "[+] Installing MySQL Server"
echo mysql-server mysql-server/root_password password $mysqlpassword | debconf-set-selections > /dev/null 2>&1
echo mysql-server mysql-server/root_password_again password $mysqlpassword | debconf-set-selections > /dev/null 2>&1
apt-get -y install mysql-server > /dev/null 2>&1

echo "[+] Importing SQL Files"
wget -q http://download.iiptvpanel.com/sql/iIPTV-BASIC.sql > /dev/null 2>&1
mysql -uroot -p$mysqlpassword -e "CREATE DATABASE iIPTV" > /dev/null 2>&1
mysql -uroot -p$mysqlpassword iIPTV < iIPTV-BASIC.sql > /dev/null 2>&1
rm -f iIPTV-BASIC.sql > /dev/null 2>&1


echo "[+] Creating Directory and Files"
mkdir /home/iIPTV > /dev/null 2>&1
mkdir /home/iIPTV/logs/ > /dev/null 2>&1
mkdir /home/iIPTV/movies/ > /dev/null 2>&1
mkdir /home/iIPTV/vod/ > /dev/null 2>&1
mkdir /home/iIPTV/tmp/ > /dev/null 2>&1
mkdir /home/iIPTV/nginx/ > /dev/null 2>&1
mkdir /home/iIPTV/GeoIP > /dev/null 2>&1
mkdir /home/iIPTV/dbbackup > /dev/null 2>&1
mkdir /var/www > /dev/null 2>&1
mkdir /var/www/config > /dev/null 2>&1

chown www-data /home/iIPTV/ > /dev/null 2>&1
chown www-data /home/iIPTV/logs > /dev/null 2>&1
chown www-data /home/iIPTV/vod > /dev/null 2>&1
chown www-data /home/iIPTV/movies > /dev/null 2>&1
chown www-data /home/iIPTV/tmp > /dev/null 2>&1
chown www-data /home/iIPTV/nginx > /dev/null 2>&1
chown www-data /home/iIPTV/GeoIP > /dev/null 2>&1
chown www-data /home/iIPTV/dbbackup > /dev/null 2>&1
chown www-data /var/www > /dev/null 2>&1
chown www-data /var/www/config >/dev/null 2>&1

echo "[+] Installing NGiNX"
cd /home/iIPTV/ >/dev/null 2>&1
git clone git://github.com/arut/nginx-rtmp-module.git > /dev/null 2>&1
wget http://nginx.org/download/nginx-1.9.6.tar.gz > /dev/null 2>&1
tar xzf nginx-1.9.6.tar.gz > /dev/null 2>&1
cd nginx-1.9.6 > /dev/null 2>&1
./configure --prefix=/home/iIPTV/nginx --sbin-path=/home/iIPTV/nginx/sbin/nginx --conf-path=/home/iIPTV/nginx/conf/nginx.conf --pid-path=/home/iIPTV/nginx/nginx.pid --add-module=/home/iIPTV/nginx-rtmp-module --with-http_ssl_module > /dev/null 2>&1
make > /dev/null 2>&1
make install > /dev/null 2>&1


wget -q http://download.iiptvpanel.com/config.zip > /dev/null 2>&1
unzip -o config.zip -d /var/www/config/ > /dev/null 2>&1
rm -f config.zip > /dev/null 2>&1
echo 'define("DB_HOST", "localhost");' >> /var/www/config/config.php
echo 'define("DB_NAME", "iIPTV");' >> /var/www/config/config.php
echo 'define("DB_USER", "root");' >> /var/www/config/config.php
a='define("DB_PASS", "'
b='");'
c=$a$mysqlpassword$b
echo $c >> /var/www/config/config.php

wget -q http://download.iiptvpanel.com/GeoLiteCity.dat
mv GeoLiteCity.dat /home/iIPTV/GeoIP/GeoLiteCity.dat

mv /home/iIPTV/nginx/conf/default.conf /home/iIPTV/nginx/conf/default.conf_old > /dev/null 2>&1
wget http://download.iiptvpanel.com/nginxBasic.zip -O /home/iIPTV/tmp/nginxBasic.zip > /dev/null 2>&1
unzip -o /home/iIPTV/tmp/nginxBasic.zip -d /home/iIPTV/nginx/conf > /dev/null 2>&1
rm -f /home/iIPTV/tmp/nginxBasic.zip > /dev/null 2>&1

echo "[+] Installing PHP5, PHP5-FPM"
apt-get -y install php5-fpm php5-cgi php5-mysql php5-curl php5-gd php5-idn php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-mhash php5-pspell php5-recode php5-sqlite php5-tidy php5-xmlrpc php5-xsl > /dev/null 2>&1
echo 'cgi.fix_pathinfo = 1' >> /etc/php5/cgi/php.ini > /dev/null 2>&1

/home/iIPTV/nginx/sbin/nginx -s stop > /dev/null 2>&1
/home/iIPTV/nginx/sbin/nginx > /dev/null 2>&1
service php5-fpm stop > /dev/null 2>&1
service php5-fpm start > /dev/null 2>&1

wget -q http://download.iiptvpanel.com/IPTVBASICv1.2.1.zip > /dev/null 2>&1
unzip -o IPTVBASICv1.2.1.zip -d /var/www/ > /dev/null 2>&1
rm -f IPTVBASICv1.2.1.zip > /dev/null 2>&1

echo "[+] Adding Cronjobs"
crontab -l > IPTV > /dev/null 2>&1
echo "*/1 * * * * php -q /var/www/cronjob/check_stream.php" >> IPTV
echo "59 23 * * 1-7 php -q /var/www/cronjob/check_user.php" >> IPTV
echo "*/1 * * * * php -q /var/www/cronjob/check_vod.php" >> IPTV
echo "*/1 * * * * php -q /var/www/cronjob/check_connectivity.php" >> IPTV
echo "*/1 * * * * sudo -u www-data php -q /var/www/cronjob/restart_livestream.php" >> IPTV
echo "*/1 * * * * sudo -u www-data php -q /var/www/cronjob/restart_vodstream.php" >> IPTV

crontab IPTV > /dev/null 2>&1
rm IPTV > /dev/null 2>&1

echo "[+] Start Service NGiNX"
/home/iIPTV/nginx/sbin/nginx -s stop > /dev/null 2>&1
/home/iIPTV/nginx/sbin/nginx > /dev/null 2>&1
echo "[+] Start Service PHP5-FPM"
service php5-fpm stop > /dev/null 2>&1
service php5-fpm start > /dev/null 2>&1

echo "[+] Installing Quick Fixes"
mkdir /usr/local/share/GeoIP/ > /dev/null 2>&1
cp /home/iIPTV/GeoIP/GeoLiteCity.dat /usr/local/share/GeoIP/ > /dev/null 2>&1

echo "[+] Adding iIPTVPanel as Service"
wget http://download.iiptvpanel.com/iIPTV > /dev/null 2>&1
mv iIPTV /etc/init.d/ > /dev/null 2>&1
chmod 755 /etc/init.d/iIPTV > /dev/null 2>&1
update-rc.d iIPTV defaults > /dev/null 2>&1
rm iIPTV > /dev/null 2>&1

echo "[+] Restarting iIPTV"
service iIPTV stop
service iIPTV start

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "Installation successful"
echo "MySQL Server User: "root" Password: "$mysqlpassword""
echo "Enter http://SERVERIP into your Browser change for safety your admin password"
echo "Default Login |-> Username: admin | Password: admin123"
exit 0
fi
