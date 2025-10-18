rem We need to pipe this into cmd instead of cmd /c,
rem otherwise python virtual environment activation won't work properly.
rem however, PowerShell piping "|" will add an UTF-8 BOM marker at the start of the file,
rem which will mess up with the first line of this script.
rem Therefore, we keep "rem" comments at the start of the file to avoid issues.
rem This is probably my first time that removing a comment will cause a bug xD
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
cp README.md ..\dist\
cd ..\

rem Clean up
rem rm -rf yt-dlp
rem rm -rf pyinstaller
rem rm -rf venv
