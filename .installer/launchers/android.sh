#!/usr/bin/env bash
systemPath="/data/data/com.termux/files/usr/share/iicalc/"
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
		gcc -v 1> /dev/null 2> /dev/null
		if [ "$?" == "0" ]
		then
			python3 -m pip install python-Levenshtein
		fi
	fi
	echo "Creating user folder..."
	mkdir $userPath
	mkdir "$userPath/plugins"
	mkdir "$userPath/themes"
	cp "$systemPath/config.ini" "$userPath/config.ini"
	clear
fi
if [ $# == 0 ]; then
	python3 $systemPath/iicalc.py
else
	while test $# -gt 0
	do
		case "$1" in
			--version) python3 $systemPath/iicalc.py --version
				;;
			-V) python3 $systemPath/iicalc.py -V
				;;
			*) python3 $systemPath/iicalc.py
		esac
		shift
	done
fi