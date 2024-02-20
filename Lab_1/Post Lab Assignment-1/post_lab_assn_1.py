from sense_hat import SenseHat
from time import sleep
from picamera2 import Picamera2, Preview
sense=SenseHat()
blue= (0,0,255)
yellow= (255,255,0)
red=(255,0,0)



sense.clear()
x = 3
y = 5
sense.set_pixel(x,y,(255,0,0))



while True:
    for event in sense.stick.get_events():
        print(event.direction,event.action)
        if event.action =="pressed": ## check if the joystick was pressed
            if event.direction=="up":
                y = y - 1
            elif event.direction=="down":
                y = y + 1
            elif event.direction=="left":
                x = x - 1
            elif event.direction=="right":
                x = x + 1
            elif event.direction=="middle":
                sense.clear()
                exit()
            
            x = x % 8
            y = y % 8
            sense.clear()
            sense.set_pixel(x,y,(255,0,0))
            
            # sleep(2) ## wait a while and then clear the screen
            