#!/bin/bash
clear
echo " "
echo -e "${txtblue} ┌────────────────────────────────────────────┐ "
echo -e "${txtblue} │[R]        Welcome to  Xtream Panel          │ "
echo -e "${txtblue} └────────────────────────────────────────────┘ "
PS3='Please enter your choice: '
options=("https installation" "http installation" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "http installation")
            wget -q -O installalbi.sh https://raw.githubusercontent.com/mak-iptv/sat-albaniarepo/main/installalbi.sh && chmod +x installalbi.sh && ./installalbi.sh 
            break
            ;;
        "http installation")
            wget -q -O installalbi.sh https://raw.githubusercontent.com/mak-iptv/sat-albaniarepo/main/installx.sh && chmod +x installalbi.sh && ./installalbi.sh
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY"
            ;;
    esac
done
