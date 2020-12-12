#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
python=python3.8
if [ ! -d "$userPath" ]
then
	clear
	echo "First time setup"
	echo ""
	echo "Would you like to attempt to install required Python modules? (Y/n)"
	read yn
	if [ "$yn" != "n" ]
	then
		$python -m pip install -r "$systemPath/requirements.txt"
		gcc -v 1> /dev/null 2> /dev/null
		if [ "$?" == "0" ]
		then
			$python -m pip install python-Levenshtein
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
	$python $systemPath/iicalc.py
else
	while test $# -gt 0
	do
		case "$1" in
			--version) $python $systemPath/iicalc.py --version
				;;
			-V) $python $systemPath/iicalc.py -V
				;;
			*) $python $systemPath/iicalc.py
		esac
		shift
	done
fi