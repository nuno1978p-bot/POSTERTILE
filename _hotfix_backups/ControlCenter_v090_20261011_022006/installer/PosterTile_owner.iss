#define MyAppName "NONIVERUS PosterTile Owner"
#define MyAppVersion "0.9.0.1"
#define MyAppExeName "NONIVERUS PosterTile Owner.exe"

[Setup]
AppId={{A21297EC-47C8-4A17-8CB9-DA95C70645A9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=NONIVERUS
DefaultDirName={autopf}\NONIVERUS\PosterTile\Owner
DisableDirPage=no
DefaultGroupName=NONIVERUS
OutputDir=..\release_editions
OutputBaseFilename=NONIVERUS_PosterTile_Owner_Setup_v0.9.0.1
SetupIconFile=..\assets\branding\postertile_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
VersionInfoVersion=0.9.0.1
VersionInfoCompany=NONIVERUS
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist_editions\NONIVERUS PosterTile Owner\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LEGAL_NONIVERUS.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\distribution\THIRD_PARTY_NOTICE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

; Owner: NEVER distribute. Preview: install only on authorized recipients.
; Uninstall must not delete documents, QSettings, or user license files.
