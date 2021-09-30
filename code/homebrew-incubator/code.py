"""
TMP36z:
data -> A2

tm1637:
CLK -> 16
DIO -> 17
"""

import board
import TM1637
import microcontroller
import time
from analogio import AnalogIn

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    
TARGET_TEMP = 35
TARGET_DIR = '<TARGET DIRECTORY>'
SCRIPT_NAME = 'run_miner'

mydisplay = TM1637.TM1637(clk=board.GP16, dio=board.GP17)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

sensorPin = AnalogIn(board.A2)

time.sleep(10)

miner_status = 0

def read_temp(temp_sensor):
    temps = []
    
    for i in range(1000):
        Vin = (temp_sensor.value * 3300)/65536
        temperature = (Vin-500)/10
        temps.append(temperature)
    
    avg_temp = sum(temps)/len(temps)
    print(avg_temp)
    return avg_temp
   
if __name__ == "__main__":
   
    while True:
        
        time.sleep(1)        
        
        temperature = read_temp(sensorPin)
        tmp = round(temperature)
        mydisplay.temperature(tmp)
        time.sleep(2)
        
        
        if (temperature < TARGET_TEMP - 1 and miner_status == 0):
            kbd.send(Keycode.GUI)
            time.sleep(1)
            layout.write('cmd')
            time.sleep(1)
            kbd.send(Keycode.ENTER)
            time.sleep(1)
            layout.write('cd ')
            time.sleep(1)
            layout.write(TARGET_DIR)
            time.sleep(1)
            kbd.send(Keycode.ENTER)
            time.sleep(1)
            layout.write(SCRIPT_NAME)
            time.sleep(1)
            kbd.send(Keycode.ENTER)
            
            miner_status = 1
            

            
            
        if (temperature > TARGET_TEMP + 1 and miner_status == 1):
                kbd.press(Keycode.CONTROL, Keycode.C)
                kbd.release(Keycode.CONTROL, Keycode.C)
                time.sleep(1)
                kbd.send(Keycode.Y)
                time.sleep(1)
                kbd.send(Keycode.ENTER)
                time.sleep(1)
                layout.write('exit')
                time.sleep(1)
                kbd.send(Keycode.ENTER)
                
                
                miner_status = 0
                
                
        time.sleep(10)

