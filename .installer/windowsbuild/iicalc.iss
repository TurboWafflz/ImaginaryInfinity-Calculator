#define MyAppName "ImaginaryInfinity Calculator"

#define VerFile FileOpen("system/version.txt")
#define MyAppVersion FileRead(VerFile)
#expr FileClose(VerFile)
#undef VerFile

#define MyAppURL "https://turbowafflz.gitlab.io/iicalc.html"
#define MyAppExeName "iicalc.bat"
#define MyAppAssocName MyAppName + " Theme"
#define MyAppAssocExt ".iitheme"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

#pragma parseroption -p-

; If the file is found by calling FindFirst without faHidden, it's not hidden
#define FileParams(FileName) \
    Local[0] = FindFirst(FileName, 0), \
    (!Local[0] ? "; Attribs: hidden" : "")

#define FileEntry(Source, DestDir) \
    "Source: \"" + Source + "\"; DestDir: \"" + DestDir + "\"" + \
    FileParams(Source) + "\n"

#define ProcessFile(Source, DestDir, FindResult, FindHandle) \
    FindResult \
        ? \
            Local[0] = FindGetFileName(FindHandle), \
            Local[1] = Source + "\\" + Local[0], \
            (Local[0] != "." && Local[0] != ".." \
                ? (DirExists(Local[1]) \
                      ? ProcessFolder(Local[1], DestDir + "\\" + Local[0]) \
                      : FileEntry(Local[1], DestDir)) \
                : "") + \
            ProcessFile(Source, DestDir, FindNext(FindHandle), FindHandle) \
        : \
            ""

#define ProcessFolder(Source, DestDir) \
    Local[0] = FindFirst(Source + "\\*", faAnyFile), \
    ProcessFile(Source, DestDir, Local[0], Local[0])

#pragma parseroption -p+

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{228DEFE7-5B19-419F-8086-566ECFC72A81}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\Program Files (x86)\iicalc
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=.\LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=iicalc
SetupIconFile=.\iicalc.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: ".installer\launchers\windows.bat"; DestDir: "C:\Windows"; DestName: "iicalc.bat"
#emit ProcessFolder("system\systemPlugins\", "{app}\systemPlugins")
;Source: "system\systemPlugins\*"; DestDir: "{app}\systemPlugins"; Flags: ignoreversion recursesubdirs createallsubdirs
#emit ProcessFolder("system\themes\", "{app}\themes")
#emit ProcessFolder("system\docs\", "{app}\docs")
;Source: "system\themes\*"; DestDir: "{app}\themes"; Flags: ignoreversion recursesubdirs createallsubdirs
#emit ProcessFolder("templates\", "{app}")
Source: "README.md"; DestDir: "{app}\docs\iicalc.md
Source: "messages.txt"; DestDir: "{app}"
Source: "requirements.txt"; DestDir: "{app}"
Source: "system\version.txt"; DestDir: "{app}"
Source: "main.py"; DestDir: "{app}"; DestName: "iicalc.py"
Source: ".installer\configDefaults\windows.ini"; DestDir: "{app}"; DestName: "config.ini"
Source: "iicalc.ico"; DestDir: "{app}"
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{cmd}"; IconFilename: "{app}\iicalc.ico"; Parameters: "/c start """" CALL ""C:\Windows\iicalc.bat"" --shortcut"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{cmd}"; IconFilename: "{app}\iicalc.ico"; Parameters: "/c start """" CALL ""C:\Windows\iicalc.bat"" --shortcut"; Tasks: desktopicon

[Run]
;Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
Filename: "{cmd}"; Parameters: "/c start """" CALL ""C:\Windows\iicalc.bat"" --shortcut"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}"; Flags: uninsalwaysuninstall

[Messages]
ConfirmUninstall=If you are having a problem with %1, please start an issue at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator.%n%nAre you sure you want to uninstall %1?

[Code]
var
  DownloadPage: TDownloadWizardPage;
  ProgressPage: TOutputProgressWizardPage;
  ErrorCode: Integer;
  PythonInstalled: Boolean;
  Result1: Boolean;
  Python: string;
//  InstallReqs: Boolean;
//  reqs: string;

function CheckPython() : Boolean;
var
  PythonFileName : string;
begin
  PythonFileName := FileSearch('py.exe', GetEnv('PATH'));
   Result := (PythonFileName <> '');
end;

function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Successfully downloaded file to {tmp}: %s', [FileName]));
  Result := True;
end;

procedure InitializeWizard;
begin
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), @OnDownloadProgress);
  ProgressPage := CreateOutputProgressPage('I','');
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
//  InstallReqs := True;
  Result := '';
  PythonInstalled := CheckPython();
  if not PythonInstalled then
  begin
    Result1 := MsgBox('This tool requires Python 3 to run, but it was not detected. Do you want to install it now ?', mbConfirmation, MB_YESNO) = IDYES;
    if Result1 then
    begin
      DownloadPage.Clear;
      DownloadPage.Add('https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe', 'python.exe', '');
      DownloadPage.Show;
      try
        try
          DownloadPage.Download;
        except
          SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
          Result := 'Error, Terminating...';
//          InstallReqs := False;
        end;
      finally
        DownloadPage.Hide;
      end;
      Python:='"'+Expandconstant('{tmp}\python.exe')+'"'
      Exec('cmd.exe ','/c '+Python+' InstallAllUsers=0 PrependPath=1 Include_test=0','', SW_HIDE,ewWaituntilterminated, Errorcode);
      if not (Errorcode = 0) then begin
        Result := 'Error installing python. Exit code ' + IntToStr(Errorcode);
//        InstallReqs := False;
      end;
//    end else;
//      InstallReqs := False;
    end;
//  if InstallReqs then begin
//    try
//      ProgressPage.SetText('Installing requirements...', '');
//      ProgressPage.SetProgress(0, 100);
//      ProgressPage.ProgressBar.Style := npbstMarquee;
//      ExtractTemporaryFile('requirements.txt');
//      ProgressPage.Show;
//      try
//        reqs := ExpandConstant('{tmp}\requirements.txt');
//        Exec('python.exe ','-m pip3 install -r ' + reqs, '', SW_HIDE,ewWaituntilterminated, Errorcode);
//        if not (Errorcode = 0) then begin
//          MsgBox('Error installing python. Exit code ' + IntToStr(Errorcode), mbInformation, MB_OK);
//        end;
//      except
//        MsgBox(GetExceptionMessage, mbInformation, MB_OK);
//      end;

//    finally
//      ProgressPage.Hide;
//      ProgressPage.Free;
//    end;

  end;
end;