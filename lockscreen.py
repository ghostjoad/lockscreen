#!/usr/bin/python

"""
Create a lockscreen which superimposes a blurred screenshot
and the last SMBC picture. 

Inspired from https://ma08.github.io/XKCD-Lock-using-i3lock-and-xautolock/

Dependancies : 
    -i3lock
    -xautolock
    -scrot
    -imagemagick
"""

import images
import os.path

from subprocess import Popen, PIPE, call
from os import getenv

HOME = getenv('HOME')

# Check if ~/Pictures/smbc exists
if not os.path.isdir(HOME+'/Pictures/smbc'):
    call(["mkdir","-p",HOME+"/Pictures/smbc"])

# Check if ~/Pictures/lockscreen exists
if not os.path.isdir(HOME+'/Pictures/lockscreen'):
    call(["mkdir","-p",HOME+"/Pictures/lockscreen"])

# Download the front page picture, if not already done
images.retrieve_image()

# Find the front picture among all pictures
image = Popen('ls ~/Pictures/smbc/*.png | tail -1',
                         stdout=PIPE, shell=True)

decoded_image = image.communicate()[0].decode('utf-8')

image_name = decoded_image.split('\n')[0]


# Screenshot, and superimposition of the picture
images.print_blur_screen(image_name)

to_display = HOME + '/Pictures/lockscreen/lockscreen.png'

# i3block
call(["i3lock","-i",to_display,"-t"])
