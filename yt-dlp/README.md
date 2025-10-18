# preparing yt-dlp as an executable file

## Instructions

Requirements:

1. Only Windows is supported for this script.
2. Python installed.
3. GCC (MinGW-w64) compiler installed and added to PATH. (I use <https://winlibs.com/>)
4. FFmpeg.exe static build downloaded, and placed in the same directory as this script. (<https://www.ffmpeg.org/download.html#build-windows>)

Steps:

1. CD to this directory.
2. Run `cat ./autobuild-yt-dlp.cmd | cmd` in your PowerShell or Command Prompt.

## Issues I encountered while using yt-dlp

### Long file name fix

--restrict-filenames -o 1.mp4

### Premium

Add this argument:

```cmd
--extractor-args "youtube:player_client=default,ios;formats=missing_pot"
```
