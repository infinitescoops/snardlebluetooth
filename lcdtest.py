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

# Create a blank image for drawing
# Make sure to create image with mode '1' for 1-bit color
image = Image.new('1', (oled.width, oled.height))

# Get drwaing object to draw on image
draw = ImageDraw.Draw(image)


# Draw a smaller inner rectangle
draw.rectangle((BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1), outline=0, fill=0)
 
# Load default font.
font = ImageFont.load_default()
 
# Draw Some Text
text = "Hello World!"
(font_width, font_height) = font.getsize(text)
draw.text((oled.width//2 - font_width//2, oled.height//2 - font_height//2), text, font=font, fill=255)
 
# Display image
oled.image(image)
oled.show()
