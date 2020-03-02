import bluetooth
import time
import sys
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

disp = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, dc_pin, reset_pin, cs_pin)

disp.fill(0)
disp.show()

image = Image.new('1', (disp.width, disp.height))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
ellipsis = ".    "
phase = 0

while True:
	draw.rectangle((BORDER, BORDER, disp.width - BORDER - 1, disp.height - BORDER -1), outline=0, fill=0)
	draw.text((0, 24), "sacnning" + ellipsis, font = font, fill = 255)
	disp.image(image)
	disp.show()
	
	nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)
	
	print("found %d devices" % len(nearby_devices))
	
	for addr, name in nearby_devices:
		draw.text(name)
		
		disp.image(image)
		disp.show()
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
