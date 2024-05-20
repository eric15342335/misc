"""
This file is used to generate the version information for the Windows executable.
"""
import os
# get the current version from the __version__ variable in __init__.py
from yt_dlp.version import __version__
# get current UTC+8 time
from datetime import datetime
# Writes the version information to a file named versioninfo.txt
with open(os.path.join(os.path.dirname(__file__), 'versioninfo.txt'), 'w', encoding='utf-8') as f:
    # filevers should be always a tuple with four items: (1, 0, 0, 0)
    # it will be year, month, day, UTC+8 time in format of Hour+Minute (e.g. 2021, 8, 1, 1200)
    f.write("""VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({}, {}, {}, {})
        ),
    kids=[
        StringFileInfo(
        [
        StringTable(
            u'040904B0',
            [StringStruct(u'CompanyName', u'github.com/yt-dlp/yt-dlp'),
            StringStruct(u'FileDescription', u'A feature-rich command-line audio/video downloader'),
            StringStruct(u'FileVersion', u'{}'),
            StringStruct(u'InternalName', u'yt-dlp'),
            StringStruct(u'LegalCopyright', u'This is free and unencumbered software released into the public domain.'),
            StringStruct(u'OriginalFilename', u'yt-dlp.exe'),
            StringStruct(u'ProductName', u'yt-dlp'),
            StringStruct(u'ProductVersion', u'{}')])
        ]),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
        ]
    )""".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().strftime('%H%M'), __version__, __version__))

print('Version information written to versioninfo.txt')