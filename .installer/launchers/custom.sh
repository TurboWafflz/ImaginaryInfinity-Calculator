#!/usr/bin/env bash
systemPath="/usr/share/iicalc/"
userPath="$HOME/.iicalc"
echo "Creating user folder..."
mkdir $userPath
mkdir "$userPath/plugins"
mkdir "$userPath/themes"
cp "$systemPath/config.ini" "$userPath/config.ini"
python3 $systemPath/iicalc.py $@
