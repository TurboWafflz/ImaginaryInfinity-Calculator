#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
echo "Creating user folder..."
mkdir $userPath
mkdir "$userPath/plugins"
mkdir "$userPath/themes"
cp "$systemPath/config.ini" "$userPath/config.ini"
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