::Windows installer by Tabulate
@echo off
::Run as admin
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
cls
echo ImaginaryInfinity Calculator Installer

::Set variables
set systemPath=C:\Program Files (x86)\iicalc\
set config=.installer\configDefaults\windows.ini
set launcher=.installer\launchers\windows.bat
set userPath=%USERPROFILE%\.iicalc\

::Check for adding desktop shortcut
set /p ads="Add desktop shortcut? [Y/n] "
IF %ads%==N (
	set ads=n
)
IF NOT %ads%==n (
	set addDesktopShortcut=true
) else (
	set addDesktopShortcut=false
)

::Make directories if not exist
echo Installing launcher...
IF NOT EXIST %systemPath% (
	mkdir %systemPath%
)
IF NOT EXIST %systemPath%\systemPlugins (
	mkdir %systemPath%\systemPlugins
)
IF NOT EXIST %userPath% (
	mkdir %userPath%
)

::Copy launcher to directory
copy %launcher% %systemPath%\iicalc.bat

::Check if systemPath in PATH
echo ;%PATH%; | find /C /I ";C:\Program Files (x86)\iicalc\;" >> temp.txt
set /p setpath=<temp.txt
del /f /q temp.txt

::If systemPath not in PATH, add it
IF %setpath%==0(
	scripts.vbs path
)

::Set doskey file for command line opening of calculator
echo iicalc=C:\Program Files (x86)\iicalc\iicalc.py>%userPath%iicalc.doskey

::Add doskey path to registry
IF NOT "%DFMT%"=="" (
	REG ADD "HKLM\Software\Microsoft\Command Processor" /v Autorun /t REG_SZ /d "%DFMT% && DOSKEY /MACROFILE=\"%USERPROFILE%\.iicalc\iicalc.doskey\"" /f
) else (
	REG ADD "HKLM\Software\Microsoft\Command Processor" /v Autorun /t REG_SZ /d "DOSKEY /MACROFILE=\"%USERPROFILE%\.iicalc\iicalc.doskey\"" /f
)

::Add desktop shortcut if selected
echo Adding desktop icon...
IF %addDesktopShortcut%==true (
	scripts.vbs desktop
)

::Add start menu entry
echo Adding start menu entry...
scripts.vbs startmenu

::Copy builtin plugins and directories
echo Installing builtin plugins...
xcopy /e system\systemPlugins\* %systemPath%\systemPlugins\
xcopy /e themes\ %systemPath%\themes\
xcopy /e templates\ %systemPath%\templates\

echo Installing main Python script...
copy main.py %systemPath%\iicalc.py
copy requirements.txt %systemPath%\requirements.txt
copy %config% %userPath%\config.ini

::Install requirements
echo Installing Python modules...
py -m pip install -r requirements.txt

cmd /k
