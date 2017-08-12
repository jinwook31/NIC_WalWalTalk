#!/usr/bin/python
from pygame import mixer, time

mixer.pre_init(44100, -16, 2, 256)
mixer.init(frequency=16000, buffer=24000)
#pygame.init()
mixer.music.load('/home/pi/Desktop/NIC_WalWalTalk/module/sound/here.mp3')
mixer.music.play(loops=1)

while mixer.music.get_busy():
    time.Clock().tick(100)

