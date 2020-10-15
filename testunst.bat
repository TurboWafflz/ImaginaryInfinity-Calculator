@echo off

cls
echo "ImaginaryInfinity Calculator Uninstaller"
echo "If you are having a problem with the calculator, please start an issue at https:/\github.com\TurboWafflz\ImaginaryInfinity-Calculator"
SET /p uninst="Are you sure you want to uninstall ImaginaryInfinity Calculator? (y\N)"
IF %uninst%=="Y" (
	SET uninst=y
)
IF NOT %uninst%=="y" (
	echo "Cancelled"
	exit
)
SET systemPath=C:\Program Files (x86)\iicalc\
SET config=.installer\configDefaults\windows.ini
SET launcher=.installer\launchers\windows.bat
cd /d "%~dp0"
echo "Removing launcher..."
DEL  "%binPath%\iicalc"
scripts.vbs uninstall
echo "Removing main Python script.."
DEL  "%systemPath%\iicalc.py"
echo "Removing builtin plugins..."
DEL /S %systemPath%