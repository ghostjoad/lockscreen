# SMBC-Lockscreen

Based on i3block, creates a lockscreen by superimposing the last
[SMBC](http://www.smbc-comics.org) picture and a blurred screenshot
of the desktop.

## Usage

Add 

    xautolock -time 10 -detectsleep -locker "path-to-lockscreen/lockscreen.py" &
to ``.xinitrc``.

## Description

``images.py`` contains the functions used to download, scale, and 
superimpose SMBC pictures and desktop screenshot.

``lockscreen.py`` finds the last SMBC in the list, and displays
the merged picture with ``i3lock``.
