import os
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import requests
from font_fredoka_one import FredokaOne
import datetime

# Set up the display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")


if inky_display.resolution not in ((212, 104), (250, 122)):
    w, h = inky_display.resolution
    raise RuntimeError("This example does not support {}x{}".format(w, h))

inky_display.set_border(inky_display.BLACK)

# Uncomment the following if you want to rotate the display 180 degrees
# inky_display.h_flip = True
# inky_display.v_flip = True

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)


def check_ping(hostname):
  response = os.system("ping -c 5 " + hostname)
    # and then check the response...
  if response == 0:
    pingstatus = "+UP"
  else:
    pingstatus = "-DOWN"

  return pingstatus

response = requests.get('https://ipinfo.io/ip')

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")

message = f'{formatted_time}\n' + f"RPI-4-RM: {check_ping('rpi4rm')}  @{response.text} \n" + f"RPI-4-PM: {check_ping('rpi4pm')}\n" + f"Workstn: {check_ping('workstation')}\n" +f"gcp-vm: {check_ping('gcp-vm')}\n" + f"ocp-vm: {check_ping('ocp-vm')}\n"

font = ImageFont.truetype(FredokaOne, 15)

w, h = font.getsize(message)
x = 0
y = 0 

draw.text((x, y), message, inky_display.BLACK, font)
inky_display.set_image(img)
inky_display.show()
