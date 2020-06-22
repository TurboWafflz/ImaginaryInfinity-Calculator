import configparser
builtin = True;
config = configparser.ConfigParser()
config.read("config.ini")
try:
	if config["startup"]["bgm"] == "true":
		import simpleaudio as sa
		bgm = sa.WaveObject.from_wave_file(".bgm.wav")
		bgmPlay = bgm.play()
except:
	pass