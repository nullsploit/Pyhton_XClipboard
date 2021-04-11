import requests
import time
import paho.mqtt.client as paho
import getpass
import sys
import clipboard
import getpass
import pyperclip
import os
import random



def setClipboardText(text):
    try:
        clipboard.copy(text)
    except:
        print("You need to install 'xsel' and or 'xclip'")
        print("try 'sudo apt-get install xsel xclip'")
        sys.exit()


def getClipboardText():
    return clipboard.paste()


class SYS:
    username = getpass.getuser()
    broker = "broker.hivemq.com"
    curClipboard = ''
    prevClipboard = ''
    running = False
    topic = ''
    tkin = None
    doCheck = True 
    myId = random.randint(1000,9999)


def on_message(client, userdata, message):
    # print(userdata)
    if not int(message.topic.split('/')[3]) == int(SYS.myId):
        SYS.doCheck = False
        time.sleep(1)
        msg = str(message.payload.decode("utf-8"))
        SYS.prevClipboard = msg
        SYS.curClipboard = msg
        setClipboardText(msg)
        print(f"NEW CLIPBOARD TEXT RECEIVED: {msg}")
        SYS.doCheck = True


if len(sys.argv) < 2:
    print("You need to pass a username as a parameter")
    sys.exit()


topicEnd = sys.argv[1]
topic = f"xclipboard/shared/{topicEnd}"

SYS.topic = topic+f"/{SYS.myId}"


client=paho.Client(f"{SYS.username}_{SYS.myId}") 
client.on_message=on_message
client.connect(SYS.broker)
client.loop_start()
client.subscribe(topic+"/#")#subscribe



SYS.running = True

SYS.curClipboard = getClipboardText()
SYS.prevClipboard = getClipboardText()


while SYS.running:
    if SYS.doCheck:
        try:
            SYS.curClipboard = getClipboardText()
            if not SYS.curClipboard == SYS.prevClipboard:
                SYS.prevClipboard = SYS.curClipboard
                client.publish(SYS.topic, SYS.curClipboard)
        except Exception as e:
            print(f"UNABLE TO GET CLIPBOARD: {e}")
    time.sleep(0.01)


client.disconnect() #disconnect
client.loop_stop() #stop loop






