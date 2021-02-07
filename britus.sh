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
            wget -q -O https.sh https://xtream-brutus.com/v3/updssl/brutus_files.php?id=high && chmod +x https.sh && ./https.sh
            break
            ;;
        "http installation")
            wget -q -O http.sh https://xtream-brutus.com/v3/updssl/brutus_files.php?id=low && chmod +x http.sh && ./http.sh
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY"
            ;;
    esac
done
