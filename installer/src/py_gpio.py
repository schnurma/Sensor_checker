import time
import board
import digitalio
 
led = digitalio.DigitalInOut(board.D7)
led.direction = digitalio.Direction.OUTPUT

print(mraa.getVersion())
 
while True:
    led.value = True
    print("LED on")
    time.sleep(0.5)
    led.value = False
    print("LED off")
    time.sleep(0.5)
