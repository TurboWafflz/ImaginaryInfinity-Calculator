if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
 if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
  $CommandLine = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
  Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList $CommandLine
  Exit
 }
}

clear
echo "ImaginaryInfinity Calculator Uninstaller"
$DIR=$PSScriptRoot

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
rm "C:\Windows\iicalc.bat" 2>$null

echo "Removing desktop shortcut..."
$DesktopPath = [Environment]::GetFolderPath("Desktop")
rm "$DesktopPath\ImaginaryInfinity Calculator.lnk" 2>$null
rm "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\iicalc\" -Recurse -Force 2>$null

echo "Removing main Python script.."
rm "$systemPath/iicalc.py" 2>$null
echo "Removing builtin plugins..."
rm $systemPath -Recurse -Force 2>$null
Write-Host "Warning: Removing ImaginaryInfinity Calculator does not remove the .iicalc folder in your home directory. If you want to run the portable version of ImaginaryInfinity Calculator again, you will have to delete it." -fore yellow
