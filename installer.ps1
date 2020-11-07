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
cp system\version.txt "$systemPath" -force
cp .\README-online "$systemPath" -force
cp $config "$systemPath\config.ini" -force

echo "Installing icons..."
cp ".\iicalc.ico" "$systemPath\iicalc.ico"
Invoke-Expression "C:\Windows\System32\Cscript.exe .\scripts.vbs startmenu //nologo"

py -V > $null
if($? -eq $false){
	$yn = Read-Host "Python is not installed. You must install Python to run the calculator Install it now? [Y/n] "
	if($yn -ne "n"){
		echo "Downloading installer..."
		[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
		Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -OutFile ".\python-3.9.0.exe"
		echo "Installing Python, this make take a bit..."
		.\python-3.9.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
	}
}

echo "Installing Python modules..."
py -m pip install -r requirements.txt