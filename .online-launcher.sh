touch .start
python3 -m pip install -r requirements.txt
while [ -f ".start" ]
do
  rm .start
  clear
  echo "Loading latest version..."
  git pull https://github.com/TurboWafflz/ImaginaryInfinity-Calculator master > .update.log
  touch .onlineMode
  python3 ./main.py online
  rm .onlineMode
done
