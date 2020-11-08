@echo off
SET systemPath=C:\Program Files (x86)\iicalc\
SET userPath=%userprofile%\.iicalc\
echo "%systemPath%\requirements.txt"
IF NOT EXIST %userPath% (
	cls
	echo First time setup
	echo.
	SET /p inst="Would you like to attempt to install required Python modules? (Y\n)"
	IF NOT "%inst%"=="n" (
		py -m pip install -r "%systemPath%\requirements.txt"
	)
	echo "Creating user folder..."
	mkdir %userPath%
	mkdir "%userPath%\plugins"
	mkdir "%userPath%\themes"
	COPY  "%systemPath%\config.ini" "%userPath%\config.ini"
	cls
)
py "%systemPath%\iicalc.py"
exit