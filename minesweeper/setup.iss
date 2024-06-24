[Setup]
AppName=MineSweeper
AppVersion=1.0.1
WizardStyle=classic
DefaultDirName={autodesktop}\MineSweeper
DefaultGroupName=MineSweeper
UninstallDisplayIcon={app}\MineSweeper.exe

Compression=lzma2/ultra64
InternalCompressLevel=ultra64
LZMANumBlockThreads=1
LZMANumFastBytes=273
LZMAUseSeparateProcess=yes
LZMADictionarySize=65536
SolidCompression=yes

SourceDir=.
OutputDir=.
OutputBaseFilename=MineSweeperInstaller

ArchitecturesAllowed=x64
PrivilegesRequired=lowest
DisableWelcomePage=no
LicenseFile=LICENSE.txt

[Files]
Source: "MineSweeper.exe"; DestDir: "{app}"
Source: "images\tiles.jpg"; DestDir: "{app}/images/"

[Icons]
Name: "{group}\Launch MineSweeper"; Filename: "{app}\MineSweeper.exe"
Name: "{group}\Uninstall"; Filename: "{app}\unins000.exe"

[Run]
Filename: "{app}\MineSweeper.exe"; Description: "Launch MineSweeper"; Flags: postinstall nowait skipifsilent

