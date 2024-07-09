rem Clone the respective repositories
git clone https://github.com/pyinstaller/pyinstaller --depth=50
git clone https://github.com/yt-dlp/yt-dlp --depth=1
pip cache purge

virtualenv venv --clear
venv\scripts\activate
cd pyinstaller/bootloader

rem Cmd and Powershell command
set PATH=%PATH%;E:\Personal Data\Repositories\mingw64\bin
rem $env:PATH += 'E:\Personal Data\Repositories\mingw64\bin'

rem Build PyInstaller bootloader using custom gcc binaries
set CFLAGS=-flto
set LDFLAGS=-flto
python .\waf all --gcc -j 21
cd ..\
pip3 install -e .
cd ..\
cd yt-dlp

rem Update version info
python devscripts/update-version.py
cp ../versioninfo.py versioninfo.py
python versioninfo.py

rem Build yt-dlp
set PYTHONOPTIMIZE=2
pip install -e .
pyinstaller -y --clean yt_dlp/__main__.py --name yt-dlp --noupx --version-file versioninfo.txt --collect-submodules yt-dlp.yt_dlp.utils --icon ../banner.ico --recursive-copy-metadata yt-dlp --recursive-copy-metadata pyinstaller
pyinstaller -y --onefile --clean yt_dlp/__main__.py --name yt-dlp --noupx --version-file versioninfo.txt --collect-submodules yt-dlp.yt_dlp.utils --icon ../banner.ico --recursive-copy-metadata yt-dlp --recursive-copy-metadata pyinstaller
cp ..\ffmpeg.exe dist\yt-dlp\
cp -r dist\yt-dlp\ ..\yt_dlp\
cp README.md ..\yt_dlp\
cd ..\

rem Clean up
rem rm -rf yt-dlp
rem rm -rf pyinstaller
rem rm -rf venv

