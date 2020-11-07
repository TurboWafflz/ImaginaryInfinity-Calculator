if (!([Security.Principal.WindowsPrinciple][Security.Principal.WindowsIndentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
clear
echo "ImaginaryInfinity Calculator Uninstaller"
DIR=$PSScriptRoot

echo "If you are having a problem with the calculator, please start an issue at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator"
$yn = Read-Host "Are you sure you want to uninstall ImaginaryInfinity Calculator? (y/N)"

if("$yn" -ne "y"){
	echo "Cancelled"
	exit
}
$systemPath="C:\Program Files (x86)\iicalc\"
$binPath=$systemPath

cd $DIR
echo "Removing launcher..."
rm "$binPath/iicalc.bat"

Invoke-Expression "C:\Windows\System32\Cscript.exe .\scripts.vbs uninstall //nologo"

echo "Removing main Python script.."
rm "$systemPath/iicalc.py"
echo "Removing builtin plugins..."
rm $systemPath -Recurse -Force
echo "\033[38;5;11mWarning: Removing ImaginaryInfinity Calculator does not remove the .iicalc folder in your home directory. If you want to run the portable version of ImaginaryInfinity Calculator again, you will have to delete it.\033[m"
