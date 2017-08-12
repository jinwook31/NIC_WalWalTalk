#!/usr/bin/python
import time as t

from pygame import mixer,time

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

port_num = 6
state = False
print('Program start.. press Ctrl-C to quit...')

# get Value Func
def getValue(num):
    tmp = mcp.read_adc(num)
    t.sleep(0.5)
    return tmp

# play Func
def play():
    t.sleep(0.5)
    mixer.music.load('/home/pi/Desktop/NIC_WalWalTalk/module/sound/here.mp3')
    mixer.music.play(loops=1)
    while mixer.music.get_busy():
        time.Clock().tick(100)
    t.sleep(1)
    cur.excute(setPlay)
    db.commit()
    print('playing voice')

#check state
def checkVal(val, state, port):
    if not state and val > 700:
        t.sleep(1)
        val = getValue(port)
        if val > 700:
            print(update_true)
            cur.execute(update_true)
            db.commit()
            return True
    elif state and val < 300:
        t.sleep(1)
        val = getValue(port)
        if val < 300:
            print(update_false)
            cur.execute(update_false)
            db.commit()
            return False


# Main program loop.
while True:
    #read sesor value(pre_task)
    value = getValue(port_num)
    print(value)
    t.sleep(1)

    #check mySQL play value
    cur.execute(getData)
    rows = cur.fetchall()
    if '1' in rows:
        play()
        print('pet is waiting')

    #check sesor value
    state = checkVal(value, state, port_num)
    if state:
        mixer.music.load('/home/pi/Desktop/NIC_WalWalTalk/module/sound/coming.mp3')
        mixer.music.play(loops=1)
        while mixer.music.get_busy():
            time.Clock().tick(100)
        print('playing voice')

db.close()
