from network import LoRa
from machine import Pin
import socket
import time

# Please pick the region that matches where you are using the device

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
i = 0

led1 = Pin('P20', mode=Pin.OUT)
led2 = Pin('P21', mode=Pin.OUT)
led3 = Pin('P22', mode=Pin.OUT)

def sendAck():
        RSSI = lora.stats().rssi
        input_value = RSSI
        input_str ="ACK"+str(input_value)
        s.send(input_str)
        print(input_str)
        #time.sleep(.2)



def halloReply():
    global i
    while True:
        data = s.recv(64)
        
        if data == b'stop' or data == b'sit' or data == b'comeback':
            
            buttonReply(data)
            time.sleep(1)
        else:
            s.send('Hallo')
            print('Hallo{} '.format(i))
            i += 1
            time.sleep(1)

def buttonReply(data):
    global i
    while True:
        if data == b'stop':
            sendAck()
            led1.value(1)
            time.sleep(4)
            led1.value(0)
            break
        elif data == b'sit':
            sendAck()
            led2.value(1)
            time.sleep(1)
            led2.value(0)
            break
        elif data == b'comeback':
            sendAck()
            led3.value(1)
            time.sleep(1)
            led3.value(0)
            break
        else:
            led1.value(0)
            led2.value(0)
            led3.value(0)
            time.sleep(1)
            break

# Condition to determine which function to call
Condition = True

if Condition:
    halloReply()
else:
    buttonReply(None)