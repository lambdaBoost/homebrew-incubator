"""


tm1637:
CLK -> 16
DIO -> 17

ds18x20:
DAT -> 18
"""


import tm1637, onewire, ds18x20, time
from machine import Pin
from utime import sleep

TARGET_TEMP = 60

mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))

heater_pin = machine.Pin(20, Pin.OUT)
led_pin = machine.Pin(25, Pin.OUT)

ds_pin = machine.Pin(18)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
 
roms = ds_sensor.scan()

led_pin.value(0)

#counter intuitive - 1 opens the relay and turns off the heater
heater_pin.value(1)
heater_status = 0

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        tem = ds_sensor.read_temp(rom)
        print("temp" + str(tem))
        mydisplay.temperature(round(tem))
        time.sleep(2)
          
          
    #turn on
        if tem < (TARGET_TEMP - 2):
            heater_pin.value(0)
            print("heater on")
            led_pin.value(1)
            heater_status = 1
            
        
        #turn off
        elif tem > (TARGET_TEMP) :
            heater_pin.value(1)
            print("heater off")
            led_pin.value(0)
            heater_status = 0
            
        print(heater_pin.value())

    




