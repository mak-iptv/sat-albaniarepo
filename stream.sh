#!/bin/bash
URL="http://cobra2016.dyndns.tv:1947/get.php?username=enjoyimcob_SkYpE&password=8LftLI6H71&type=m3u"
echo DOWNLOADING:${URL}
ffmpeg -i ${URL} -c copy playlist.m3u8
