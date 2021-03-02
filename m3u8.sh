#!/bin/sh

# Author : Wang Poh Peng
# Description : Use FFMPEG to download videos into mkv or mp4 format

RED='\033[1;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
CYAN='\033[0;36m'

command -v ffmpeg >/dev/null 2>&1 || { echo >&2 "${RED}ffmpeg is required for the script to download video stream. Run \`brew install ffmpeg\` if you are on Homebrew"; exit 1; }

echo "${GREEN}Enter m3u8 file url endpoint:${NC}"
read ENDPOINT
echo "${GREEN}Enter video file name to be saved as including extension eg. video1.mp4${NC}"
read FILENAME

ffmpeg -user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7" -i $ENDPOINT -c copy $FILENAME

echo "${CYAN}The video file is saved at $PWD/$FILENAME"
echo "${NC} Resetting Terminal Font Color..."
