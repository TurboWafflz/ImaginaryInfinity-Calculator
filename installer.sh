#!/usr/bin/env bash
clear
echo "ImaginaryInfinity Calculator Installer"
DIR=`dirname $0`
chmod +x $DIR/${0##*/}

#Build deb
if [ "$1" == "--make-deb" ]
then
	rm -rf "iicalc-deb"
	mkdir -p "iicalc-deb/DEBIAN"
	mkdir -p "iicalc-deb/usr/bin"
	mkdir -p "iicalc-deb/usr/share"
	mkdir -p "iicalc-deb/usr/share/applications"
	mkdir -p "iicalc-deb/usr/share/icons"
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
		mkdir -p "iicalc-appImage/usr/bin"
		mkdir -p "iicalc-appImage/usr/share"
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
#Install for Android
elif [ "$(echo $PREFIX | grep -o 'com.termux')" != "" ]
then
	echo "The installer has detected that you are using Android, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	systemPath="/data/data/com.termux/files/usr/share/iicalc"
	binPath="/data/data/com.termux/files/usr/bin/"
	config=".installer/configDefaults/android.ini"
	launcher=".installer/launchers/android.sh"
	iconPath="/dev/null"
	desktopFilePath="/dev/null"
	desktopFile=".installer/desktopFiles/iicalc.desktop"
	installDesktopFile="false"
	pythonCommand="python3"

#Install for Linux
elif [ `uname` == "Linux" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Root access is required to install ImaginaryInfinity Calculator."
		sudo $DIR/${0##*/}
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
		sudo $DIR/${0##*/}
		exit
	fi
	echo "The installer has detected that you are using MacOS, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	systemPath="/usr/local/share/iicalc/"
	binPath="/usr/local/bin/"
	config=".installer/configDefaults/macos.ini"
	launcher=".installer/launchers/macos.sh"
	iconPath="/usr/local/share/iicalc/"
	desktopFilePath="/Applications/ImaginaryInfinity Calculator.app"
	desktopFile=".installer/desktopFiles/iicalc.app"
	installDesktopFile="true"
	pythonCommand="python3"

#Install for NetBSD
elif [ `uname` == "NetBSD" ]
then
		if [ `whoami` != "root" ]
		then
			echo "Root access is required to install ImaginaryInfinity Calculator."
			sudo $DIR/${0##*/}
			exit
		fi
		echo "The installer has detected that you are using NetBSD, is this correct? (Y/n)"
		read yn
		if [ "$yn" == "n" ]
		then
			exit
		fi
		echo "Installing required packages from pkgsrc..."
		pkg_add python38
		pkg_add py38-expat
		pkg_add readline
		pkg_add py38-readline
		echo "Installing pip..."
		python3.8 -m ensurepip
		systemPath="/usr/share/iicalc/"
		binPath="/usr/bin/"
		config=".installer/configDefaults/unix.ini"
		launcher=".installer/launchers/netbsd.sh"
		iconPath="/usr/share/icons"
		desktopFilePath="/usr/share/applications"
		desktopFile=".installer/desktopFiles/iicalc.desktop"
		installDesktopFile="true"
		pythonCommand="python3.8"
elif [ `uname` == "OpenBSD" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Root access is required to install ImaginaryInfinity Calculator."
		sudo $DIR/${0##*/}
		exit
	fi
	echo "The installer has detected that you are using OpenBSD, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	echo "Installing required packages from pkgsrc..."
	pkg_add -r python
	pip3 > /dev/null
	if [ "$?" != "0" ]
	then
		pkg_add -r curl
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python3 get-pip.py
		rm get-pip.py
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
elif [ `uname` == "FreeBSD" ]
then
	if [ `whoami` != "root" ]
	then
		echo "Root access is required to install ImaginaryInfinity Calculator."
		sudo $DIR/${0##*/}
		exit
	fi
	echo "The installer has detected that you are using FreeBSD, is this correct? (Y/n)"
	read yn
	if [ "$yn" == "n" ]
	then
		exit
	fi
	echo "Installing required packages from pkgsrc..."
	pkg install python3
	pip3 > /dev/null
	if [ "$?" != "0" ]
	then
		pkg install curl
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python3 get-pip.py
		rm get-pip.py
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
else
	echo "The installer does not currently support your operating system. You can install the calculator by manually specifying the required paths, however this is only recommended for experienced users."
	echo "Would you like to start manual installation (y/N)?"
	read yn
	if [ "$yn" != "y" ]
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
	echo "Installing icons..."
	if [ `uname` == "Darwin" ]; then
		iconSource="$DIR/iicalc.tiff"
		iconDestination="$DIR/$desktopFile"
		icon=/tmp/`basename $iconSource`
		rsrc=/tmp/icon.rsrc

		# Create icon from the iconSource
		cp $iconSource $icon

		# Add icon to image file, meaning use itself as the icon
		sips -i $icon

		# Take that icon and put it into a rsrc file
		DeRez -only icns $icon > $rsrc

		# Apply the rsrc file to
		SetFile -a C $iconDestination

		touch $iconDestination/$'Icon\r'
		Rez -append $rsrc -o $iconDestination/Icon?
		SetFile -a V $iconDestination/Icon?

		#osascript -e 'tell application "Finder" to quit'
		#osascript -e 'delay 2'
		#osascript -e 'tell application "Finder" to activate'

		rm $rsrc $icon
	else
		cp iicalc.tiff "$iconPath"
	fi

	cp -r "$desktopFile" "$desktopFilePath"
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
		echo "On MacOS, download the latest Python installer from https://www.python.org/downloads/mac-osx/"
		echo "On Android based operating systems (In Termux) run: pkg install python"
	fi
fi
#Copy files
mkdir -p "$binPath"
chmod +x "$binPath/iicalc"
echo "Installing builtin plugins..."
mkdir -p $systemPath
mkdir -p "$systemPath/systemPlugins"
cp -r system/systemPlugins/* "$systemPath/systemPlugins"
mkdir -p "$systemPath/themes"
cp -r system/themes/* "$systemPath/themes"
cp -r "templates" "$systemPath"
echo "Installing main Python script..."
cp main.py "$systemPath/iicalc.py"
cp requirements.txt "$systemPath"
cp messages.txt "$systemPath"
cp system/version.txt "$systemPath"
cp README.md "$systemPath"
cp $config "$systemPath/config.ini"
#Add custom URI scheme if supported
#if type xdg-mime > /dev/null; then
	#xdg-mime default iicalc.desktop x-scheme-handler/iicalc
#fi
#Install Python modules if installing
if [ "$buildOnly" != "true" ]
then
	"$pythonCommand" -m pip --version 1> /dev/null 2> /dev/null
	if [ "$?" != "0" ]
	then
		echo ""
		echo -e "\033[0;31mPip does not seem to be installed. Before running the calculator, please install pip.\033[0m"
		echo "On Debian based operating systems (Ubuntu, Raspbian, Debian, etc.) run: sudo apt install python3-pip"
		echo "On Red Hat based operating systems (Fedora, CentOS, Red Hat Enterprise Linux, etc.) run: sudo dnf install python3-pip"
		echo "On Alpine based operating systems (PostmarketOS, Alpine Linux, etc.) run: sudo apk add py3-pip"
		echo "On Arch based operating systems (Arch Linux, Manjaro, TheShellOS) run: sudo pacman -Syu python-pip"
		echo -e "On MacOS, download the get-pip.py installer: \033[33mcurl https://bootstrap.pypa.io/get-pip.py -o get-pip.py\033[0m and then run: \033[33mpython3 get-pip.py\033[0m"
	else
		echo "Installing Python modules..."
		"$pythonCommand" -m pip install -r requirements.txt
	fi
fi
#Finish building deb
if [ "$1" == "--make-deb" ]
then
	#Calculate MD5 Sums
	cd iicalc-deb
	find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '%P ' | xargs md5sum > "DEBIAN/md5sums"
	cd ..
	#Calculate Size
	cat "iicalc-deb/DEBIAN/control" | sed "s'Installed-Size: 0'Installed-Size: `du -s iicalc-deb/ | awk '{print $1}'`'" > "iicalc-deb/DEBIAN/control"
	cat "iicalc-deb/DEBIAN/control" | sed "s'Version: 0'Version: `cat system/version.txt`'" > "iicalc-deb/DEBIAN/control"
	#Build DEB
	dpkg -b iicalc-deb iicalc.deb
fi
#Finish building AppImage
if [ "$1" == "--make-appImage" ]
then
	if [ -f appimagetool-x86_64.AppImage ]
	then
		echo "Found appimagetool"
	else
		wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
	fi
	chmod +x ./appimagetool-x86_64.AppImage
	./appimagetool-x86_64.AppImage --appimage-extract
	mv squashfs-root appimagetool
	ARCH=x86_64 ./appimagetool/AppRun iicalc-appImage
fi
