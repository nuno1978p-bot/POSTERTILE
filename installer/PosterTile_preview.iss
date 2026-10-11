#define MyAppName "NONIVERUS PosterTile Private Preview"
#define MyAppVersion "0.9.0.2"
#define MyAppExeName "NONIVERUS PosterTile Private Preview.exe"

[Setup]
AppId={{47FD65E8-338F-45CE-9F74-2DF0B0AB9C41}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=NONIVERUS
DefaultDirName={autopf}\NONIVERUS\PosterTile\PrivatePreview
DisableDirPage=auto
UsePreviousAppDir=yes
UsePreviousTasks=yes
DefaultGroupName=NONIVERUS
OutputDir=..\release_editions
OutputBaseFilename=NONIVERUS_PosterTile_PrivatePreview_Setup_v0.9.0.2
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
VersionInfoVersion=0.9.0.2
VersionInfoCompany=NONIVERUS
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist_editions\NONIVERUS PosterTile Private Preview\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\LEGAL_NONIVERUS.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\distribution\THIRD_PARTY_NOTICE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

; Owner: NEVER distribute. Preview: install only on authorized recipients.
; Uninstall must not delete documents, QSettings, or user license files.

[Code]
{ Detecao de atualizacao pela mesma identidade AppId; Owner e Preview independentes. }
var
  NVPreviousVersion: String;
  NVExistingInstall: Boolean;
  NVOriginalNextText: String;

function NVFindPreviousVersion(var InstalledVersion: String): Boolean;
var
  UninstallKey: String;
begin
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{47FD65E8-338F-45CE-9F74-2DF0B0AB9C41}_is1';
  Result := RegQueryStringValue(HKLM64, UninstallKey, 'DisplayVersion', InstalledVersion);
  if not Result then
    Result := RegQueryStringValue(HKCU, UninstallKey, 'DisplayVersion', InstalledVersion);
end;

function InitializeSetup: Boolean;
begin
  NVPreviousVersion := '';
  NVExistingInstall := NVFindPreviousVersion(NVPreviousVersion);
  Result := True;
end;

procedure InitializeWizard;
begin
  NVOriginalNextText := WizardForm.NextButton.Caption;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if not NVExistingInstall then
    Exit;

  if CurPageID = wpReady then
  begin
    if ActiveLanguage = 'portuguese' then
    begin
      WizardForm.ReadyLabel.Caption :=
        'Instalacao existente detetada: versao ' + NVPreviousVersion + '.' + #13#10 +
        'O instalador vai atualizar esta edicao para a versao {#MyAppVersion}, ' +
        'mantendo a pasta da aplicacao e a licenca existente.';
      WizardForm.NextButton.Caption := '&Atualizar';
    end
    else
    begin
      WizardForm.ReadyLabel.Caption :=
        'Existing installation detected: version ' + NVPreviousVersion + '.' + #13#10 +
        'Setup will update this edition to version {#MyAppVersion}, ' +
        'keeping the application folder and existing license.';
      WizardForm.NextButton.Caption := '&Update';
    end;
  end
  else if (CurPageID = wpWelcome) or (CurPageID = wpSelectDir) or
          (CurPageID = wpSelectProgramGroup) or (CurPageID = wpSelectTasks) then
    WizardForm.NextButton.Caption := NVOriginalNextText;
end;
