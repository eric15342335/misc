# Clone the respective repositories
git clone https://github.com/pyinstaller/pyinstaller --depth=1
git clone https://github.com/yt-dlp/yt-dlp --depth=1
cd pyinstaller/bootloader
# Cmd and Powershell command
set PATH=%PATH%;E:\Personal Data\Repositories\mingw64\bin
# $env:PATH += 'E:\Personal Data\Repositories\mingw64\bin'
# Build PyInstaller bootloader using custom gcc binaries
python .\waf all --gcc
cd ..\
python -m build
# Copy wheel to yt-dlp folder and cleanup folders
cd ..\
cp pyinstaller/dist/*.whl yt-dlp/
rm -rf pyinstaller
# Build yt-dlp
cd yt-dlp
virtualenv venv
venv\scripts\activate
python devscripts/update-version.py
ls *.whl > wheelname
pip install -r wheelname .
rm ../versioninfo.txt
python ../versioninfo.py
pyinstaller -y --clean yt_dlp/__main__.py --name yt-dlp --noupx --version-file ../versioninfo.txt
cp ..\ffmpeg.exe dist\yt-dlp\
cp -r dist\yt-dlp\ ..\yt_dlp\
cp README.md ..\yt_dlp\
cp LICENSE ..\yt_dlp\
cd ..\
rm -rf yt-dlp
