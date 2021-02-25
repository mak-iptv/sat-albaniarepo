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
        sudo wget "https://github.com/mak-iptv/sat-albaniarepo/raw/main/YouTube_Script.zip" -O "/home/xtreamcodes/iptv_xtream_codes/wwwdir"
        sudo chmod a+rx "/home/xtreamcodes/iptv_xtream_codes/wwwdir"
        sudo apt-get install apache2 -y
       
       echo "Successfully installed."
        echo "URL: http://$ip:port/youtube/streaming/youtube_live.php?id=30qZjexZ8bQ
"
        ;;
    *)
        echo "Exiting installation.."
        exit
        ;;
esac
