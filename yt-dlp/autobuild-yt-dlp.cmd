rem Clone the respective repositories
git clone https://github.com/pyinstaller/pyinstaller --depth=50
git clone https://github.com/yt-dlp/yt-dlp --depth=1

rem Clear cache
pip install -U uv
uv cache prune
uv venv

.venv\scripts\activate
cd pyinstaller/bootloader

rem Cmd and Powershell command
set PATH=%PATH%;E:\Personal Data\Repositories\mingw64\bin
rem $env:PATH += 'E:\Personal Data\Repositories\mingw64\bin'

rem Build PyInstaller bootloader using custom gcc binaries
set CFLAGS=-flto -pipe
python .\waf all --gcc -j 21
cd ..\

rem Install pyinstaller
uv pip install -e .

cd ..\
cd yt-dlp

rem Update version info
python devscripts/update-version.py
cp ../versioninfo.py versioninfo.py
python versioninfo.py

rem Build yt-dlp
set PYTHONOPTIMIZE=2
uv pip install -e .

pyinstaller -y --clean yt_dlp/__main__.py --name yt-dlp --noupx --version-file versioninfo.txt --collect-submodules yt-dlp.yt_dlp.utils --icon ../banner.ico --recursive-copy-metadata yt-dlp --recursive-copy-metadata pyinstaller
pyinstaller -y --onefile yt_dlp/__main__.py --name yt-dlp --noupx --version-file versioninfo.txt --collect-submodules yt-dlp.yt_dlp.utils --icon ../banner.ico --recursive-copy-metadata yt-dlp --recursive-copy-metadata pyinstaller

cp ..\ffmpeg.exe dist\yt-dlp\
xcopy dist\* ..\dist\ /E /I /Y
cp README.md ..\yt_dlp\
cd ..\

rem Clean up
rem rm -rf yt-dlp
rem rm -rf pyinstaller
rem rm -rf venv
