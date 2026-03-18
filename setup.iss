; Скрипт для Inno Setup
[Setup]
AppName=CryptoLab
AppVersion=1.0
DefaultDirName={pf}\CryptoLab
DefaultGroupName=CryptoLab
UninstallDisplayIcon={app}\CryptoLab.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=CryptoLab_Setup

[Files]
Source: "dist\CryptoLab.exe"; DestDir: "{app}"
Source: "README.txt"; DestDir: "{app}"
Source: "icon.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\CryptoLab"; Filename: "{app}\CryptoLab.exe"
Name: "{group}\Uninstall CryptoLab"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CryptoLab"; Filename: "{app}\CryptoLab.exe"

[Run]
Filename: "{app}\CryptoLab.exe"; Description: "Запустить CryptoLab"; Flags: postinstall nowait skipifsilent