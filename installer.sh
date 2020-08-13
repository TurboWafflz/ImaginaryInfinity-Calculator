#!/bin/bash
clear
echo "ImaginaryInfinity Calculator Installer"
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
	binPath="/usr/bin/"
	config=".installer/configDefaults/unix.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="/usr/share/icons"
	desktopFilePath="/usr/share/applications"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
	installDesktopFile="true"
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
	binPath="/usr/bin/"
	config=".installer/configDefaults/unix.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="/usr/share/iicalc/"
	desktopFilePath="/Applications/"
	desktopFile=".installer/desktopFiles/ImaginaryInfinity_Calculator"
	installDesktopFile="true"
else
	echo "The installer does not currently support your operating system. You can install the calculator by manually specifying the required paths, however this is only recommended for experienced users."
	echo "Would you like to start manual installation (y/N)?"
	read yn
	if [ $yn != "y" ]
	then
		exit
	fi
	echo "Where should plugins and themes that are installed system wide be stored? (Ex. /usr/share/iicalc/)"
	read systemPath
	echo "Where should executable files be stored? (Ex. /usr/bin/)"
	read binPath
	echo "Where should icons be stored?"
	read iconPath
	installDesktopFile="false"
	cp .installer/launchers/unix.sh .installer/launchers/custom.sh
	launcher=".installer/launchers/custom.sh"
	cat "$launcher" | sed "s'systemPath=\"/usr/share/iicalc/\"'systemPath=$systemPath'" > $launcher

fi
cd $DIR
echo "Installing launcher..."
cp $launcher "$binPath/iicalc"
if [ $installDesktopFile == "true" ]
then
	cp -r $desktopFile $desktopFilePath
fi
chmod +x "$binPath/iicalc"
echo "Installing main Python script.."
cp main.py "$binPath/iicalc.py"
echo "Installing builtin plugins..."
mkdir $systemPath
cp -r "plugins" "$systemPath"
cp -r "themes" "$systemPath"
cp -r "templates" "$systemPath"
cp requirements.txt "$systemPath"
cp $config "$systemPath/config.ini"
echo "Installing icons..."
cp iicalc.tiff "$iconPath"
echo "Installing Python modules..."
python3 -m pip install -r requirements.txt