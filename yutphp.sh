#!/bin/bash
echo "Welcome to the YT Installation script by Firez."
ip=$(dig @ns1-1.akamaitech.net ANY whoami.akamai.net +short)

if [ "$EUID" -ne 0 ]
  then echo "Please run as root."
  exit
fi

read -r -p "Are you sure you want to install? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY]) 
        sudo wget "https://yt-dl.org/downloads/latest/youtube-dl" -O "/usr/local/bin/youtube-dl"
        sudo chmod a+rx "/usr/local/bin/youtube-dl"
        sudo apt-get install apache2 -y
        sudo wget "https://pastebin.com/raw/hc4RpEgH?yt.php" -O "/var/www/html/yt.php"
        echo "Successfully installed."
        echo "URL: http://$ip/yt.php?id=YOUTUBEID"
        ;;
    *)
        echo "Exiting installation.."
        exit
        ;;
esac
