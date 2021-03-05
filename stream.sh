#!/bin/bash
URL="https://t2.tvmak.com/tv/VIZIONPLUS.m3u8?Up7sSDKBzH"
echo DOWNLOADING:${URL}
ffmpeg -i ${URL} -c copy vizion.m3u8
