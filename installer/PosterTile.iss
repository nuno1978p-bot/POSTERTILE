#define MyAppName "NONIVERUS PosterTile Luxury Studio"
#define MyAppVersion "0.8.12"
#define MyAppExeName "NONIVERUS PosterTile.exe"
#define MyAppPublisher "NONIVERUS"

[Setup]
AppId={{4D36C7B0-3D41-4BAE-9B5F-0CB5B3BF79F8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\NONIVERUS\PosterTile
DisableDirPage=no
DefaultGroupName=NONIVERUS
OutputDir=..\release
OutputBaseFilename=NONIVERUS_PosterTile_Setup_v0.8.12
SetupIconFile=..\assets\branding\postertile_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
LicenseFile=..\distribution\INSTALLATION_NOTICE.txt
VersionInfoVersion=0.8.12.0
VersionInfoCompany=NONIVERUS
VersionInfoDescription=NONIVERUS PosterTile Installer
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
ChangesAssociations=no

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\NONIVERUS PosterTile\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LEGAL_NONIVERUS.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LEIA_ME_A3_2_A4_v0_8_1.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\distribution\THIRD_PARTY_NOTICE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\NONIVERUS PosterTile"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\NONIVERUS PosterTile"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

; Do not delete user projects, exported PDFs, backups or QSettings keys on uninstall.
; Application data may live outside {app}; never remove it automatically.
