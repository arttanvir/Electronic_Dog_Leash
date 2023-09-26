import machine
import socket
import time
from machine import Pin
from network import LoRa
from machine import I2C
from mp_i2c_lcd1602 import LCD1602
from time import sleep_ms

i2c = I2C(1, pins=(Pin("P9"), Pin("P10")))

LCD = LCD1602(i2c)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
i = 0

led1 = Pin('P20', mode=Pin.OUT)
led2 = Pin('P21', mode=Pin.OUT)
led3 = Pin('P22', mode=Pin.OUT)
Rled1 = Pin('P8', mode=Pin.OUT)
Rled2 = Pin('P11', mode=Pin.OUT)
Rled3 = Pin('P12', mode=Pin.OUT)

button1 = Pin('P16', mode=Pin.IN)
button2 = Pin('P17', mode=Pin.IN)
button3 = Pin('P18', mode=Pin.IN)

button_active = False
response_active = False

def dogDistance():
        RSSI = lora.stats().rssi
        D = RSSI
        DRSSI = ("RSSI:", RSSI)
        
        #print(DRSSI)
        print("RSSI value:", RSSI)

        LCD.puts(DRSSI, 0, 1)
        #LCD.puts(DRSSI_str, 0, 1)
        if -41 <= D <= 1:
                Rled1.value(1)
                Rled2.value(0)
                Rled3.value(0)
                
                if -21 <= D <= 1:
                    print('Aprrox distance: 2m')
                    LCD.puts('Aprx dist:  <2m')

                elif -30 <= D <= -22:
                    print('Aprrox distance: 4m')
                    LCD.puts('Aprx dist:  4m')
                elif -41 <= D <= -31:
                    print('Aprrox distance: 6m')
                    LCD.puts('Aprx dist:  6m')

                #LCD.puts('RSSI:',D,0,1)
        elif -61 <= D <= -42:
                Rled1.value(0)
                Rled2.value(1)
                Rled3.value(0)
                if -50 <= D <= -42:
                    print('Aprrox distance: 8m')
                    LCD.puts('Aprx dist:  8m')

                elif -61 <= D <= -51:
                    print('Aprrox distance: 10m')
                    LCD.puts('Aprx dist: 10m')

                #LCD.puts('RSSI:',D,0,1)
        elif -80 <= D <= -62:
                Rled1.value(0)
                Rled2.value(0)
                Rled3.value(1)
                if -70 <= D <= -62:
                    print('Aprrox distance: 12m')
                    LCD.puts('Aprx dist: 12m')

                elif -81 <= D <= -71:
                    print('Aprrox distance: 15m')
                    LCD.puts('Aprx dist: >15m')

                #LCD.puts('RSSI:',D,0,1)
                
        time.sleep(1)

def ACK():
    received_str = s.recv(64) 
    signal= received_str.decode('utf-8')
    #print("Received value :", signal)
    print(signal)
    if(signal[:3]=='ACK'):
        AckRssi= lora.stats().rssi
        MasterRssi= int(signal[3:])
        Avg = (AckRssi + MasterRssi)/2
        print("Average RSSI :", Avg)
        D = Avg
        #dogDistance()
          

def button():
    global button_active, i
    button_active = True
    i = 0

    while button_active:
        
        if button1() == 1:
            led1.value(1)
            print("led1Stop")
            s.send("stop")
            #time.sleep(.2)
            ACK()
            time.sleep(1)
        elif button2() == 1:
            led2.value(1)
            print("led2Sit")
            s.send("sit")
            #time.sleep(.2)
            ACK()
            time.sleep(1) 
        elif button3() == 1:
            led3.value(1)
            print("led3comeback")
            s.send("comeback")
            #time.sleep(.2)
            ACK()
            time.sleep(1) 
        else:
            led1.value(0)
            led2.value(0)
            led3.value(0)
            break  # Exit the loop when no button is pressed

def response():
    global response_active, i
    response_active = True
    #i = 0

    while response_active:
        response = s.recv(64)
        if response == b'eidpy':
            #s.send('Pong')
            i = i + 1
            print('Hallo {}'.format(i))
            
            RSSI = lora.stats().rssi
            dogDistance()
        else:
            button()  # Call the button function if there's no valid response

# Condition to choose between response and button functions
Condition = True

if Condition:
    response()
else:
    button()