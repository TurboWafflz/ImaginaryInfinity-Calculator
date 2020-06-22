import configparser
builtin = True;
config = configparser.ConfigParser()
config.read("config.ini")
try:
	if config["startup"]["bgm"] == "true":
		import pygame
		pygame.init()
		pygame.mixer.music.load(".bgm.ogg")
		pygame.mixer.music.play(loops=-1)
except:
	pass