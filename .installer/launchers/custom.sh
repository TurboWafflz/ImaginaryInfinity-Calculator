#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
echo "Creating user folder..."
mkdir $userPath
mkdir "$userPath/plugins"
mkdir "$userPath/themes"
cp "$systemPath/config.ini" "$userPath/config.ini"

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
			python3 $systemPath/iicalc.py --viewstoreplugin $plugin
		elif [ "${uriarray[2]}" == "ascii" ]; then
			python3 $systemPath/iicalc.py --installpmplugin $plugin
		else
			python3 $systemPath/iicalc.py $@
		fi
	fi
else
	python3 $systemPath/iicalc.py $@
fi