#!/bin/bash
if [ `uname` == "Linux" ]
then
	echo "The installer has detected that you are using Linux, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	if [ `whoami` != "root" ]
	then
		echo "The installer must be run as root"
		exit
	fi
	systemPath="/usr/share/iicalc/"
	userPath="$HOME/.iicalc"
	binPath="/usr/bin/"
	config=".installer/configDefaults/linux.ini"
	launcher=".installer/launchers/linux.sh"
	iconPath="/usr/share/icons"
	desktopFilePath="/usr/share/applications"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
else
	echo "The installer does not currently support your operating system"
	exit
fi
echo "Installing launcher..."
cp $launcher "$binPath/iicalc"
cp $desktopFile $desktopFilePath
chmod +x "$binPath/iicalc"
echo "Installing main Python script.."
cp main.py "$binPath/iicalc.py"
echo "Installing icons..."
cp iicalc.tiff "$iconPath"
echo "Installing builtin plugins..."
mkdir $systemPath
cp -r "plugins" "$systemPath"
cp -r "themes" "$systemPath"
cp requirements.txt "$systemPath"
cp $config "$systemPath/config.ini"
echo "Installing Python modules..."
python3 -m pip install -r requirements.txt