if (!([Security.Principal.WindowsPrinciple][Security.Principal.WindowsIndentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
clear
echo "ImaginaryInfinity Calculator Installer"
$DIR=$PSScriptRoot

$yn = Read-Host "Add desktop shortcut? [Y/n] "
if($yn -eq "n"){$installDesktopFile="false"}else{$installDesktopFile="true"}
$systemPath="C:\Program Files (x86)\iicalc\"
$binPath=$systemPath
$config=".installer\configDefaults\windows.ini"
$launcher=".installer\launchers\windows.bat"

cd $DIR
echo "Installing launcher..."
cp $launcher "$binPath\iicalc.bat"
if($installDesktopFile -eq "true"){
	Invoke-Expression "C:\Windows\System32\Cscript.exe .\scripts.vbs desktop //nologo"
}

echo "Installing builtin plugins..."
mkdir $systemPath 2>$null
mkdir "$systemPath\systemPlugins" 2>$null
cp system\systemPlugins\* "$systemPath\systemPlugins\" -Recurse -force
cp "themes\" "$systemPath" -Recurse -force
cp "templates\" "$systemPath" -Recurse -force
echo "Installing main Python script.."
cp main.py "$systemPath\iicalc.py" -force
cp requirements.txt "$systemPath" -force
cp messages.txt "$systemPath" -force
cp $config "$systemPath\config.ini" -force
echo "Installing icons..."
cp ".\iicalc.ico" "$systemPath\iicalc.ico"
Invoke-Expression "C:\Windows\System32\Cscript.exe .\scripts.vbs startmenu //nologo"
echo "Installing Python modules..."
py -m pip install -r requirements.txt