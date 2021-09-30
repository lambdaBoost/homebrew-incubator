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

mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))


ds_pin = machine.Pin(18)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
 
roms = ds_sensor.scan()

if __name__ == "__main__":

    while True:
      ds_sensor.convert_temp()
      time.sleep_ms(750)
      for rom in roms:
        temp = round(ds_sensor.read_temp(rom))
        #print(temp)
        mydisplay.temperature(temp)
      time.sleep(2)




