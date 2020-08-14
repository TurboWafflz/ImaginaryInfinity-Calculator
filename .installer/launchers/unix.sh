#!/bin/bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
if [ ! -d "$userPath" ]
then
	echo "Creating user folder..."
	mkdir $userPath
	mkdir "$userPath/plugins"
	mkdir "$userPath/themes"
	cp "$systemPath/config.ini" "$userPath/config.ini"
fi
python3 $systemPath/iicalc.py