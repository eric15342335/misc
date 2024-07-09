rem Clone the respective repositories
git clone https://github.com/pyinstaller/pyinstaller --depth=1
git clone https://github.com/yt-dlp/yt-dlp --depth=1
virtualenv venv
venv\scripts\activate
cd pyinstaller/bootloader
rem Cmd and Powershell command
set PATH=%PATH%;E:\Personal Data\Repositories\mingw64\bin
rem $env:PATH += 'E:\Personal Data\Repositories\mingw64\bin'
rem Build PyInstaller bootloader using custom gcc binaries
python .\waf all --gcc
cd ..\
pip3 install -e .
cd ..\
rm -rf pyinstaller
rem Build yt-dlp
cd yt-dlp
python devscripts/update-version.py
rm ../versioninfo.txt
python ../versioninfo.py
pyinstaller -y --clean yt_dlp/__main__.py --name yt-dlp --noupx --version-file ../versioninfo.txt
cp ..\ffmpeg.exe dist\yt-dlp\
cp -r dist\yt-dlp\ ..\yt_dlp\
cp README.md ..\yt_dlp\
cp LICENSE ..\yt_dlp\
cd ..\
rm -rf yt-dlp
