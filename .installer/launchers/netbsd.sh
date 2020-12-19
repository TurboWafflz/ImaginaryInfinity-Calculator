#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
python="python3.8"
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
	fi
	echo "Creating user folder..."
	mkdir $userPath
	mkdir "$userPath/plugins"
	mkdir "$userPath/themes"
	cp "$systemPath/config.ini" "$userPath/config.ini"
	clear
fi

# Get URI Path if specified
uri="none"
for arg in $@; do
	if grep -q iicalc:// <<< "$arg"; then
		uri=$(echo $arg | sed -e 's/^.*iicalc:\/\///g')
		break
	fi
done
if [ "$uri" != "none" ]; then
	IFS='/' read -r -a uriarray <<< "$uri"
	if [ "${uriarray[0]}" == "plugin" ]; then
		plugin="${uriarray[1]}"
		if [ "${uriarray[2]}" == "dialog" ]; then
			$python $systemPath/iicalc.py --viewstoreplugin $plugin
		elif [ "${uriarray[2]}" == "ascii" ]; then
			$python $systemPath/iicalc.py --installpmplugin $plugin
		else
			$python $systemPath/iicalc.py $@
		fi
	fi
else
	$python $systemPath/iicalc.py $@
fi