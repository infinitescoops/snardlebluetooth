import bluetooth
import time
import json
#import RPi.GPIO as GPIO
import adafruit_ssd1306
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
reset_pin = digitalio.DigitalInOut(board.D24)
cs_pin = digitalio.DigitalInOut(board.D8)
dc_pin = digitalio.DigitalInOut(board.D23)

WIDTH = 128
HEIGHT = 64
BORDER = 5

oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, dc_pin, reset_pin, cs_pin)

oled.fill(0)
oled.show()

image = Image.new('1', (oled.width, oled.height))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
ellipsis = ".    "
phase = 0

while True:
	draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER -1), outline=0, fill=0)
	draw.text((0, 24), "sacnning" + ellipsis, font = font, fill = 255)
	disp.image(image)
	disp.display()
	
	nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=true)
	
	print("found %d devices" % len(nearby_devices))
	
	for addr, name in nearby_devices:
		draw.text(%addr)
		
		disp.image(image)
		disp.display()
		time.sleep(5)
	
	phase += 1
	if phase == 1:
		ellipsis = "..   "
	elif phase == 2:
		ellipsis = "...  "
	elif phase == 3:
		ellipsis = ".... "
	else:
		ellipsis = ".    "
		phase = 0
