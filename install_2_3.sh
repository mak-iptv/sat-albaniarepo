green='\e[0;32m'
NC='\e[0m' # No Color
VER=$(exec uname -m|grep 64)
        if [ "$VER" = "" ]
                then VER="x86"
                else VER="x64"
        fi
echo -e "${green}[+]Checking System Version...${NC}"
sleep 1
echo -e "${green}[+]Detected a $VER System...${NC}"
sleep 1
OS=$(exec cat /etc/issue | grep -v grep | grep -c "Debian")
if [ $OS -ge "1" ]
then
echo 'deb http://ftp.debian.org/debian wheezy main contrib non-free' > /etc/apt/sources.list
echo 'deb http://security.debian.org wheezy/updates main contrib non-free' >> /etc/apt/sources.list
echo 'deb http://www.deb-multimedia.org squeeze main' >> /etc/apt/sources.list
echo 'deb-src http://security.debian.org/ wheezy/updates main' >> /etc/apt/sources.list
echo 'deb http://ftp.us.debian.org/debian/ squeeze main contrib non-free' >> /etc/apt/sources.list
echo 'deb-src http://ftp.us.debian.org/debian/ squeeze main contrib non-free' >> /etc/apt/sources.list
echo 'deb http://ftp.de.debian.org/debian squeeze main contrib non-free' >> /etc/apt/sources.list
echo 'deb http://ftp.de.debian.org/debian-security squeeze/updates main contrib non-free' >> /etc/apt/sources.list
echo 'deb http://ftp.tu-chemnitz.de/pub/linux/debian/debian/ squeeze main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://ftp.tu-chemnitz.de/pub/linux/debian/debian/ squeeze main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://security.debian.org/ squeeze/updates main contrib non-free' >> /etc/apt/sources.list
echo 'deb-src http://security.debian.org/ squeeze/updates main contrib non-free' >> /etc/apt/sources.list
echo 'deb http://packages.dotdeb.org wheezy-php55 all' >> /etc/apt/sources.list
echo 'deb-src http://packages.dotdeb.org wheezy-php55 all' >> /etc/apt/sources.list
echo 'deb http://nginx.org/packages/debian/ wheezy nginx' >> /etc/apt/sources.list
echo 'deb-src http://nginx.org/packages/debian/ wheezy nginx' >> /etc/apt/sources.list
fi
if [ $OS = "0" ]
then
OS=$(exec cat /etc/issue | grep -v grep | grep -c "Ubuntu")
if [ $OS -ge "1" ]
then
echo 'deb http://us.archive.ubuntu.com/ubuntu/ precise-updates multiverse' >> /etc/apt/sources.list
echo 'deb-src http://us.archive.ubuntu.com/ubuntu/ precise-updates multiverse' >> /etc/apt/sources.list
echo 'deb http://nginx.org/packages/ubuntu/ precise nginx' >> /etc/apt/sources.list
echo 'deb-src http://nginx.org/packages/ubuntu/ precise nginx' >> /etc/apt/sources.list
fi
fi
if [ $OS = "0" ]
then echo "[-] Your Linux Version Is NOT Supported. Supported Versions Are: Debian 7 64bit OR Ubuntu 13.10 64bit";
exit;
fi
wget http://www.dotdeb.org/dotdeb.gpg > /dev/null 2>&1
apt-key add dotdeb.gpg > /dev/null 2>&1
apt-get -qq update > /dev/null 2>&1
apt-get upgrade -y
echo -e "${green}[+]Installing PHP ...${NC}"
apt-get -qq install php5 php5-cli php5-fpm php5-mysql php5-mcrypt -qy > /dev/null 2>&1
apt-get -qq install unzip -qy > /dev/null 2>&1

if [ $(php -v | grep -v grep | grep -c '5\.3\.') -eq 1 ]
then PHPV="53"
elif [ $(php -v | grep -v grep | grep -c '5\.4\.') -eq 1 ]
then PHPV="54"
elif [ $(php -v | grep -v grep | grep -c '5\.5\.') -eq 1 ]
then PHPV="55"
fi
if [ "$PHPV" == "53" ] && [ "$VER" == "x86" ]
then url="http://www.xtream-codes.com/downloads/extension/x86_PHP5.3.zip"
elif [ "$PHPV" == "53" ] && [ "$VER" == "x64" ]
then url="http://www.xtream-codes.com/downloads/extension/x64_PHP5.3.zip"
elif [ "$PHPV" == "54" ] && [ "$VER" == "x86" ]
then url="http://www.xtream-codes.com/downloads/extension/x86_PHP5.4.zip"
elif [ "$PHPV" == "54" ] && [ "$VER" == "x64" ]
then url="http://www.xtream-codes.com/downloads/extension/x64_PHP5.4.zip"
elif [ "$PHPV" == "55" ] && [ "$VER" == "x86" ]
then url="http://www.xtream-codes.com/downloads/extension/x86_PHP5.5.zip"
elif [ "$PHPV" == "55" ] && [ "$VER" == "x64" ]
then url="http://www.xtream-codes.com/downloads/extension/x64_PHP5.5.zip"
fi
cd /etc/
wget -O /etc/xtream_codes.zip "$url" > /dev/null 2>&1  
unzip xtream_codes.zip > /dev/null 2>&1
rm xtream_codes.zip > /dev/null 2>&1
if ! cat /etc/php5/cli/php.ini | grep -v grep | grep -c xtream_codes.so > /dev/null
then
echo extension=mcrypt.so >> /etc/php5/cli/php.ini
echo pcre.backtrack_limit=10000000000 >> /etc/php5/cli/php.ini
echo extension=/etc/xtream_codes.so >> /etc/php5/cli/php.ini
fi

if ! cat /etc/php5/fpm/php.ini | grep -v grep | grep -c xtream_codes.so > /dev/null
then
echo extension=mcrypt.so >> /etc/php5/fpm/php.ini
echo pcre.backtrack_limit=10000000000 >> /etc/php5/fpm/php.ini
echo extension=/etc/xtream_codes.so >> /etc/php5/fpm/php.ini
fi
cd /root
wget http://xtream-codes.com/iptv_install.txt -O install.php
php install.php
fi