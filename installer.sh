#!/bin/bash
clear
echo "ImaginaryInfinity Calculator Installer"
DIR=`dirname $0`
if [ "$1" == "--make-deb" ]
then
	rm -rf "iicalc-deb"
	mkdir "iicalc-deb"
	mkdir "iicalc-deb/DEBIAN"
	mkdir "iicalc-deb/usr"
	mkdir "iicalc-deb/usr/bin"
	mkdir "iicalc-deb/usr/share"
	mkdir "iicalc-deb/usr/share/applications"
	mkdir "iicalc-deb/usr/share/icons"
	cp ".installer/deb/control" "iicalc-deb/DEBIAN"
	cp ".installer/deb/postinst" "iicalc-deb/DEBIAN"
	chmod +x "iicalc-deb/DEBIAN/postinst"
	systemPath="iicalc-deb/usr/share/iicalc/"
	binPath="iicalc-deb/usr/bin"
	config=".installer/configDefaults/unix.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="iicalc-deb/usr/share/icons"
	desktopFilePath="iicalc-deb/usr/share/applications"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
	installDesktopFile="true"
	buildOnly="true"

elif [ `uname` == "Linux" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Root access is required to install ImaginaryInfinity Calculator."
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
	pythonCommand="python3"

elif [ `uname` == "Darwin" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Root access is required to install ImaginaryInfinity Calculator."
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
	pythonCommand="python3"
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
	echo "What command do you use to start Python 3?"
	read pythonCommand
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
if [ "$buildOnly" != "true" ]
then
	if ! type "$pythonCommand" > /dev/null; then
		echo "Python 3 not found. You must install Python 3 before attempting to install the calculator."
		echo "On Debian based operating systems (Ubuntu, Raspbian, Debian, etc.) run: sudo apt install python3"
		echo "On Red Hat based operating systems (Fedora, CentOS, Red Hat Enterprise Linux, etc.) run: sudo dnf install python3"
		echo "On Alpine based operating systems (PostmarketOS, Alpine Linux, etc.) run: sudo apk add python3"
		echo "On Arch based operating systems (Arch Linux, Manjaro, TheShellOS) run: sudo pacman -S python"
	fi
fi
chmod +x "$binPath/iicalc"
echo "Installing builtin plugins..."
mkdir $systemPath
mkdir "$systemPath/systemPlugins"
cp -r system/systemPlugins/* "$systemPath/systemPlugins"
mkdir "$systemPath/themes"
cp -r system/themes/* "$systemPath/themes"
cp -r "templates" "$systemPath"
echo "Installing main Python script.."
cp main.py "$systemPath/iicalc.py"
cp requirements.txt "$systemPath"
cp messages.txt "$systemPath"
cp $config "$systemPath/config.ini"
echo "Installing icons..."
cp iicalc.tiff "$iconPath"
if [ "$buildOnly" != "true" ]
then
	echo "Installing Python modules..."
	python3 -m pip install -r requirements.txt
fi
if [ "$1" == "--make-deb" ]
then
	#Calculate MD5 Sums
	find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '%P ' | xargs md5sum > "iicalc-deb/DEBIAN/md5sums"
	#Calculate Size
	cat "iicalc-deb/DEBIAN/control" | sed "s'Installed-Size: 0'Installed-Size: `du -s iicalc-deb/ | awk '{print $1}'`'" > "iicalc-deb/DEBIAN/control"
	#Build DEB
	dpkg -b iicalc-deb iicalc.deb
fi