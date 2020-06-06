#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if [ -f $DIR/main.py ]
then
	cd $DIR
	touch .start
	while [ -f ".start" ]
	do
		rm .start
		clear
		python3 $DIR/main.py
	done

else
	echo "Could not find main.py. (Did you move the launcher script?)"
fi
