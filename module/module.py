#!/usr/bin/python
import time

from pygame import mixer, time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
db = MySQLdb.connect("118.42.88.117","root","qwer1234","NIC")
cur = db.cursor()

#mySQL Query list
update_true = "UPDATE module SET wait=1"
update_false = "UPDATE module SET wait=0"
getData = "SELECT play FROM module"
setPlay = "UPDATE module SET play=0"

mixer.pre_init(44100,-16,2,256)
mixer.init(frequency=16000, buffer=24000)

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

state = False
print('Program start.. press Ctrl-C to quit...')

# get Value Func
def getValue(num):
    tmp = mcp.read_adc(num)
    time.sleep(0.5)
    print(tmp)
    return tmp

# play Func
def play():
    time.sleep(0.5)
    mixer.music.load('/home/pi/Desktop/NIC_WalWalTalk/module/sound/here.mp3')
    mixer.music.play(loops=1)
    while mixer.music.get_busy():
        wime.Clock().tick(100)
    time.sleep(2)
    cur.excute(setPlay)
    print('play voice')

#check state
def checkVal(val, state):
    if not state and val > 500:
        time.sleep(1)
        val = getValue(1)
        if val > 500:
            cur.excute(update_true)
            return True

    elif state and val < 300:
        time.sleep(1)
        val = getValue(1)
        if val < 300:
            cur.excute(update_false)
            return False


# Main program loop.
while True:
    #read sesor value
    values = getValue(1)

    #check play value
    cur.execute(getData)
    rows=cur.fetchall()
    if '1' in rows:
        play()
        print('pet is waiting')

    state = checkVal(values, state)

    if state:
        mixer.music.load('/home/pi/Desktop/NIC_WalWalTalk/module/sound/coming.mp3')
        mixer.music.play(loops=1)
        while mixer.music.get_busy():
            time.Clock().tick(100)
        print('play voice')

db.close()
