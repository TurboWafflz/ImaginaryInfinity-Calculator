::Windows installer by Tabulate
@echo off
::Run as admin
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
cls
echo "ImaginaryInfinity Calculator Installer"

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

SET systemPath="C:\Program Files (x86)\iicalc\"
SET config=".installer\configDefaults\windows.ini"
SET launcher=".installer\launchers\windows.bat"
cd /d "%~dp0"
echo "Installing launcher..."
COPY  %launcher% "%systemPath%launcher.bat"
::Check if systemPath in PATH
echo ;%PATH%; | find /C /I ";C:\Program Files (x86)\iicalc\;" >> temp.txt
set /p setpath=<temp.txt
del /f /q temp.txt
::If systemPath not in PATH, add it
IF %setpath%==0(
	scripts.vbs path
)
::Set doskey file for command line opening of calculator
echo iicalc=C:\Program Files (x86)\iicalc\iicalc.bat>%systemPath%iicalc.doskey
::Add doskey path to registry
IF NOT "%DFMT%"=="" (
	REG ADD "HKLM\Software\Microsoft\Command Processor" /v Autorun /t REG_SZ /d "%DFMT% && DOSKEY /MACROFILE=\"C:\Program Files (x86)\iicalc\iicalc.doskey\"" /f
) else (
	REG ADD "HKLM\Software\Microsoft\Command Processor" /v Autorun /t REG_SZ /d "DOSKEY /MACROFILE=\"C:\Program Files (x86)\iicalc\iicalc.doskey\"" /f
)
::Add desktop shortcut if selected
IF %addDesktopShortcut%==true (
	echo "Adding desktop icon..."
	scripts.vbs desktop
)
::Add start menu entry
echo "Adding start menu entry..."
scripts.vbs startmenu
py -V > nul 2>&1 || echo "Python is not installed, to install it, go to https://python.org and download the latest version"
echo "Installing builtin plugins..."
mkdir %systemPath%
mkdir "%systemPath%\systemPlugins"
COPY  system\systemPlugins\* "%systemPath%\systemPlugins"
mkdir "%systemPath%\themes"
COPY  system\themes\* "%systemPath%\themes"
COPY  templates "%systemPath%"
echo "Installing main Python script.."
COPY  main.py "%systemPath%\iicalc.py"
COPY  requirements.txt "%systemPath%"
COPY  messages.txt "%systemPath%"
COPY  system\version.txt "%systemPath%"
COPY  %config% "%systemPath%\config.ini"
echo "Installing Python modules..."
py -m pip install -r requirements.txt