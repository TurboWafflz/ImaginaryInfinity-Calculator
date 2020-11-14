#!/usr/bin/env bash
clear
echo "ImaginaryInfinity Calculator Uninstaller"
DIR=`dirname $0`
chmod +x $DIR/${0##*/}

if [ "$(echo $PREFIX | grep -o 'com.termux')" != "" ]
then
	echo "If you are having a problem with the calculator, please start an issue at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator"
	echo "Are you sure you want to uninstall ImaginaryInfinity Calculator? (y/N)"
	read
	if [ "$yn" != "y" ]
	then
		echo "Cancelled"
		exit
	fi
	echo "The uninstaller has detected that you are using Android, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	systemPath="/data/data/com.termux/files/usr/share/iicalc/"
	binPath="/data/data/com.termux/files/usr/bin/"
	config=".installer/configDefaults/unix.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="/dev/null"
	desktopFilePath="/dev/null"
	desktopFile="iicalc.desktop"
	installDesktopFile="false"
	addMimeTypes="false"
elif [ `uname` == "Linux" ] || grep -q BSD <<< `uname`
then
	if [ `whoami` != "root" ]
	then
		echo "Restarting the uninstaller as root"
		sudo $DIR/${0##*/}
		exit
	fi
	echo "If you are having a problem with the calculator, please start an issue at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator"
	echo "Are you sure you want to uninstall ImaginaryInfinity Calculator? (y/N)"
	read yn
	if [ "$yn" != "y" ]
	then
		echo "Cancelled"
		exit
	fi
	echo "The uninstaller has detected that you are using Linux, is this correct? (Y/n)"
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
	desktopFile="iicalc.desktop"
	installDesktopFile="true"
	if [ -d "/usr/share/mime/packages" ]
	then
		addMimeTypes="true"
	else
		addMimeTypes="false"
	fi
elif [ `uname` == "Darwin" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Restarting the uninstaller as root"
		sudo $DIR/${0##*/}
		exit
	fi
	echo "If you are having a problem with the calculator, please start an issue at https://github.com/TurboWafflz/ImaginaryInfinity-Calculator"
	echo "Are you sure you want to uninstall ImaginaryInfinity Calculator? (y/N)"
	read yn
	if [ "$yn" != "y" ]
	then
		echo "Cancelled"
		exit
	fi
	echo "The uninstaller has detected that you are using MacOS, is this correct? (Y/n)"
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
	desktopFile="ImaginaryInfinity_Calculator"
	installDesktopFile="true"
	addMimeTypes="false"
else
	echo "The uninstaller does not currently support your operating system. You can install the calculator by manually specifying the required paths, however this is only recommended for experienced users."
	echo "Would you like to start manual uninstallation (y/N)?"
	read yn
	if [ "$yn" != "y" ]
	then
		exit
	fi
	echo "Where are plugins and themes that are installed system wide stored? (Ex. /usr/share/iicalc/) (Warning: This directory will be deleted)"
	read systemPath
	echo "Where are the executable files stored? (Ex. /usr/bin/)"
	read binPath
	echo "Where are the icons stored?"
	read iconPath
	installDesktopFile="false"
	addMimeTypes="false"
fi
cd $DIR
echo "Removing launcher..."
rm "$binPath/iicalc"
if [ $installDesktopFile == "true" ]
then
	rm -rf "$desktopFilePath/$desktopFile"
	echo "Removing icons..."
	rm "$iconPath/iicalc.png"
fi
if [ $addMimeTypes == "true" ]
then
	for file in $(find /usr/share/mime -name "iitheme*"); do
		rm "$file" 2>/dev/null
	done
	echo "Updating MIME type Database..."
	update-mime-database /usr/share/mime
fi
echo "Removing main Python script.."
rm "$systemPath/iicalc.py"
echo "Removing builtin plugins..."
rm -rf $systemPath
echo -e "\033[38;5;11mWarning: Removing ImaginaryInfinity Calculator does not remove the .iicalc folder in your home directory. If you want to run the portable version of ImaginaryInfinity Calculator again, you will have to delete it.\033[m"
