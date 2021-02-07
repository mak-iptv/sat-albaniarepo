#!/bin/bash
clear
echo " "
echo -e "${txtyellow} ┌────────────────────────────────────────────┐ "
echo -e "${txtyellow} │[R]        Welcome to Brutus Panel          │ "
echo -e "${txtyellow} └────────────────────────────────────────────┘ "
PS3='Please enter your choice: '
options=("https installation" "http installation" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "https installation")
            wget -q -O installalbi.sh https://raw.githubusercontent.com/mak-iptv/sat-albaniarepo/main/installalbi.sh && chmod +x installalbi.sh && ./installalbi.sh
            break
            ;;
        "http installation")
            wget -q -O installx.sh https://raw.githubusercontent.com/mak-iptv/sat-albaniarepo/main/installx.sh && chmod +x installx.sh && ./installx.sh
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY"
            ;;
    esac
done
