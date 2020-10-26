#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
if [ ! -d "$userPath" ]
then
	clear
	echo "First time setup"
	echo ""
	echo "Would you like to attempt to install required Python modules? (Y/n)"
	read yn
	if [ "$yn" != "n" ]
	then
		python3 -m pip install -r "$systemPath/requirements.txt"
	fi
	echo "Creating user folder..."
	mkdir $userPath
	mkdir "$userPath/plugins"
	mkdir "$userPath/themes"
	cp "$systemPath/config.ini" "$userPath/config.ini"
	clear
fi
python3 $systemPath/iicalc.py
