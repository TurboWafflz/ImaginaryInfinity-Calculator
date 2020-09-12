#!/bin/bash
clear
echo "ImaginaryInfinity Calculator Installer"
DIR=`dirname $0`

#Build deb
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
	cp ".installer/deb/prerm" "iicalc-deb/DEBIAN"
	chmod +x "iicalc-deb/DEBIAN/postinst"
	chmod +x "iicalc-deb/DEBIAN/prerm"
	systemPath="iicalc-deb/usr/share/iicalc/"
	binPath="iicalc-deb/usr/bin"
	config=".installer/configDefaults/deb.ini"
	launcher=".installer/launchers/unix.sh"
	iconPath="iicalc-deb/usr/share/icons"
	desktopFilePath="iicalc-deb/usr/share/applications"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
	installDesktopFile="true"
	buildOnly="true"

#Build AppImage
elif [ "$1" == "--make-appImage" ]
	then
		rm -rf "iicalc-appImage"
		mkdir "iicalc-appImage"
		mkdir "iicalc-appImage/usr"
		mkdir "iicalc-appImage/usr/bin"
		mkdir "iicalc-appImage/usr/share"
		cp ".installer/appImage/AppRun" "iicalc-appImage"
		chmod +x "iicalc-appImage/AppRun"
		systemPath="iicalc-appImage/usr/share/iicalc/"
		binPath="iicalc-appImage/usr/bin"
		config=".installer/configDefaults/appImage.ini"
		launcher=".installer/launchers/appImage.sh"
		iconPath="iicalc-appImage/"
		desktopFilePath="iicalc-appImage"
		desktopFile=".installer/desktopFiles/iicalc-appImage.desktop"
		cp "iicalc.png" "iicalc-appImage"
		installDesktopFile="true"
		buildOnly="true"

#Install for Linux
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

#Install for MacOS
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
cp -v $launcher "$binPath/iicalc"
#Install desktop file if requested
if [ $installDesktopFile == "true" ]
then
	cp -r $desktopFile $desktopFilePath
fi
#Warn about missing Python if installing
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
#Copy files
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
cp system/version.txt "$systemPath"
cp $config "$systemPath/config.ini"
echo "Installing icons..."
cp iicalc.tiff "$iconPath"
#Install Python modules if installing
if [ "$buildOnly" != "true" ]
then
	echo "Installing Python modules..."
	python3 -m pip install -r requirements.txt
fi
#Finish building deb
if [ "$1" == "--make-deb" ]
then
	#Calculate MD5 Sums
	find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '%P ' | xargs md5sum > "iicalc-deb/DEBIAN/md5sums"
	#Calculate Size
	cat "iicalc-deb/DEBIAN/control" | sed "s'Installed-Size: 0'Installed-Size: `du -s iicalc-deb/ | awk '{print $1}'`'" > "iicalc-deb/DEBIAN/control"
	cat "iicalc-deb/DEBIAN/control" | sed "s'Version: 0'Version: `cat system/version.txt`'" > "iicalc-deb/DEBIAN/control"
	#Build DEB
	dpkg -b iicalc-deb iicalc.deb
fi
#Finish building AppImage
if [ "$1" == "--make-appImage" ]
then
	# if [ -f appimagetool-x86_64.AppImage ]
	# then
	# 	echo "Found appimagetool"
	# else
	# 	./wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
	# fi
	# chmod +x ./appimagetool-x86_64.AppImage
	./appimagetool-x86_64.AppImage --appimage-extract
	mv squashfs-root appimagetool
	ARCH=x86_64 ./appimagetool/AppRun iicalc-appImage
fi