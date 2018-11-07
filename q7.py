

import network
import time
import gc
import math
#import uos

import tsys01,ms5837
import sdcard, os

from machine import Pin
from machine import SPI
from machine import I2C

filename='dataout1.csv'

MYFILE_DIV=10

led = Pin(13,Pin.OUT)

#SCL=21 # Green BR cable
#SDA=19 # White BR cable

SCL=14 # Green BR cable
SDA=2 # White BR cable


i2c = I2C(-1, Pin(SCL), Pin(SDA))

p=ms5837.MS5837(model='MODEL_30BA',i2c=i2c)
t=tsys01.TSYS01(i2c)

p.init()


sck=Pin(16)
mosi=Pin(4)
miso=Pin(17)
cs = Pin(15, Pin.OUT)
spi2=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)

sd = sdcard.SDCard(spi2, cs)
os.mount(sd,'/sd')
#output=os.listdir('/sd')
#print(output)

#f=open('/sd/data.txt','a')

#sd = sdcard.SDCard(spi2, cs)
#os.mount(sd,'/sd')
#output=os.listdir('/sd')
#print(output)

#f=open('/sd/data.txt','a')

DISPLAY=True

if DISPLAY:
    import ssd1306
    from machine import I2C
    #i2c_display = I2C(-1, Pin(SCL), Pin(SDA))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()

if DISPLAY:
    oled.fill(0)
    oled.text("Starting up ...",0,0)
    oled.show()
   
f=open('/sd/'+filename,'w')
data_str="counter,temp_acc,temp,pressure,depth"
f.write(data_str+"\n")
f.close()
    
while True:
    try:
        #measure
        #temp=23.3
        temp_acc=t.getTemp()
        temp,pressure,depth=p.get_measurement()
        
        #f=open("./"+filename,'a')
        f=open('/sd/'+filename,'a')
        data_str="%d,%.3f,%.3f,%.3f,%.3f" % (counter,temp_acc,temp,pressure,depth)
        print(data_str)
        f.write(data_str+"\n")
        f.flush()
        f.close()
        

        if DISPLAY:
            oled.fill(0)
            
            linenum=0
            linestep=9
            
            oled.text(ip[0]+":8081",0,linenum)
            
            linenum+=linestep
            display_text="i=%d" % counter
            oled.text(display_text,0,linenum)
            
            linenum+=linestep
            display_text="ta:%.1f tb:%.1f" % (temp_acc,temp)
            oled.text(display_text,0,linenum)
            
            linenum+=linestep
            display_text="p:%.3f" % pressure
            oled.text(display_text,0,linenum)
            
            linenum+=linestep
            display_text="d:%.4f" % depth
            oled.text(display_text,0,linenum)
            
            linenum+=linestep
            display_text="fn:%s" % filename
            oled.text(display_text,0,linenum)
            
            oled.show()
        counter += 1
    except Exception as e:
            print(str(e))
    gc.collect()



