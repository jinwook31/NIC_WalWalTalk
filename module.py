#!/usr/bin/python
import time

from pygame import mixer

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

mixer.init()

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
    return tmp

# play Func
def play():
    time.sleep(0.5)
    mixer.music.load('e:/LOCAL/')
    mixer.music.play()
    time.sleep(2)
    cur.excute(setPlay)

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

    state = checkVal(values. state)

    if state:
        mixer.music.load('e:/LOCAL/')
        mixer.music.play()

db.close()



