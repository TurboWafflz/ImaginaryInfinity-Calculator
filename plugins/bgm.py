import configparser
builtin = True;
config = configparser.ConfigParser()
config.read("config.ini")
try:
	if config["startup"]["bgm"] == "true":
		import pygame
		pygame.init()
		pygame.mixer.music.load(".bgm.wav")
		pygame.mixer.music.play()
except:
	pass