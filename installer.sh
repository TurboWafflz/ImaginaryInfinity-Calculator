#!/bin/bash
DIR=`dirname $0`
if [ `uname` == "Linux" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Restarting the installer as root"
		sudo $DIR/installer.sh
		exit
	fi
	echo "The installer has detected that you are using Linux, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	systemPath="/usr/share/iicalc/"
	userPath="$HOME/.iicalc"
	binPath="/usr/bin/"
	config=".installer/configDefaults/unix.ini"
	launcher=".installer/launchers/linux.sh"
	iconPath="/usr/share/icons"
	desktopFilePath="/usr/share/applications"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
elif [ `uname` == "Darwin" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Restarting the installer as root"
		sudo $DIR/installer.sh
		exit
	fi
	echo "The installer has detected that you are using MacOS, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	systemPath="/usr/share/iicalc/"
	userPath="$HOME/.iicalc"
	binPath="/usr/bin/"
	config=".installer/configDefaults/linux.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="/usr/share/iicalc/"
	desktopFilePath="/Applications/"
	desktopFile=".installer/desktopFiles/ImaginaryInfinity_Calculator"
else
	echo "The installer does not currently support your operating system"
	exit
fi
cd $DIR
echo "Installing launcher..."
cp $launcher "$binPath/iicalc"
cp -r $desktopFile $desktopFilePath
chmod +x "$binPath/iicalc"
echo "Installing main Python script.."
cp main.py "$binPath/iicalc.py"
echo "Installing builtin plugins..."
mkdir $systemPath
cp -r "plugins" "$systemPath"
cp -r "themes" "$systemPath"
cp requirements.txt "$systemPath"
cp $config "$systemPath/config.ini"
echo "Installing icons..."
cp iicalc.tiff "$iconPath"
echo "Installing Python modules..."
python3 -m pip install -r requirements.txt