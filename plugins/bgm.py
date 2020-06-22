import simpleaudio as sa
bgm = sa.WaveObject.from_wave_file(".bgm.wav")
bgmPlay = bgm.play()