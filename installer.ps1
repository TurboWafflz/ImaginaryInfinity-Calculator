if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
 if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
  $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
  Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine
  Exit
 }
}

clear
echo "ImaginaryInfinity Calculator Installer"
$DIR=$PSScriptRoot

$yn = Read-Host "Add desktop shortcut? [Y/n] "
$yn = $yn.ToLower()
if($yn -eq "n"){$installDesktopFile="false"}else{$installDesktopFile="true"}
$systemPath="C:\Program Files (x86)\iicalc\"
$binPath="C:\Program Files (x86)\iicalc\"
$config=".installer\configDefaults\windows.ini"
$launcher=".installer\launchers\windows.bat"

cd $DIR
if($installDesktopFile -eq "true"){
	$WshShell = New-Object -comObject WScript.Shell
	$DesktopPath = [Environment]::GetFolderPath("Desktop")
	$Shortcut = $WshShell.CreateShortcut("$DesktopPath\ImaginaryInfinity Calculator.lnk")
	$Shortcut.TargetPath = "%comspec%"
	$Shortcut.Arguments = '/c start "" CALL "C:\Windows\iicalc.bat" --shortcut'
	$Shortcut.Description = "ImaginaryInfinity Calculator"
	$Shortcut.IconLocation = "C:\Program Files (x86)\iicalc\iicalc.ico"
	$Shortcut.Save()
}

mkdir $systemPath 2>$null
mkdir "$systemPath\systemPlugins" 2>$null
mkdir "$systemPath\docs" 2>$null
echo "Installing launcher..."
cp $launcher "C:\Windows\iicalc.bat" -force
echo "Installing builtin plugins..."
cp system\systemPlugins\* "$systemPath\systemPlugins\" -Recurse -force
cp "system\themes\" "$systemPath" -Recurse -force
cp "templates\" "$systemPath" -Recurse -force
cp system\docs\* "$systemPath\docs\" -Recurse -force
echo "Installing main Python script.."
cp main.py "$systemPath\iicalc.py" -force
cp requirements.txt "$systemPath" -force
cp messages.txt "$systemPath" -force
cp system\version.txt "$systemPath" -force
cp .\README.md "$systemPath\docs\iicalc.md" -force
cp $config "$systemPath\config.ini" -force

echo "Installing icons..."
cp ".\iicalc.ico" "$systemPath\iicalc.ico"
mkdir "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\iicalc\" 2>$null
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\iicalc\ImaginaryInfinity Calculator.lnk")
$Shortcut.TargetPath = "%comspec%"
$Shortcut.Arguments = '/c start "" CALL "C:\Windows\iicalc.bat" --shortcut'
$Shortcut.Description = "ImaginaryInfinity Calculator"
$Shortcut.IconLocation = "C:\Program Files (x86)\iicalc\iicalc.ico"
$Shortcut.Save()

if (-Not (Get-Command 'py' -errorAction SilentlyContinue)){
	$yn = Read-Host "Python is not installed. You must install Python to run the calculator Install it now? [Y/n] "
	$yn = $yn.ToLower()
	if($yn -ne "n"){
		echo "Downloading installer..."
		[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
		Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -OutFile ".\python-3.9.0.exe"
		echo "Installing Python, please rerun the installer once completed by running .\installer.ps1"
		Read-Host "[Press enter to continue]"
		.\python-3.9.0.exe InstallAllUsers=0 PrependPath=1 Include_test=0
	}else{
		echo "Please install python https://python.org"
		Read-Host "[Press enter to continue]"
	}
}else{
	rm .\python-3.9.0.exe -Force 2>$null
	echo "Installing Python modules..."
	py -m pip install -r requirements.txt
	Read-Host "Installation complete. Press enter to continue."
}