weatherclock

Weatherclock is a Raspberry Pi "Studio" style clock written in python3 using pygame with calendar and weather display on (16:9) monitors, displays and TVs.

This was designed specifically for the Raspberry Pi and Raspberry Pi 7" touch screen.

The optional weather information is retrieved from a CumulusMX system running on the local area network.

Status:
-------

weatherclock is currently stable and ready for use.

Hardware
--------
weatherclock is designed to be run on a Raspberry Pi with the Raspberry Pi 7" Touchscreen display.  It has also been tested on a 16:9 HDMI monitor


Installation requirements for Raspberry Pi
------------------------------------------

weatherclock is designed to run on Raspberry Pi under Debian 10 (Buster) pygame and Python3. weatherclock requires Debian desktop (NOT the -lite variant)

If you are unsure how to do this please see https://www.raspberrypi.org/software/raspberry-pi-desktop/  

It is expected that the OS is already installed BUT note the following:

Use
```
sudo raspi-config
```
to -
```
enable SSH support - for access to system from other machines - to change variables for example.
boot into console with auto-login
wait for network on boot - required to ensure internal clock is correct and for the initial read of the CumulusMX system (if enabled).
```
Installation of weatherclock
----------------------------

from the terminal issue the following commands:
```
sudo apt update
sudo apt upgrade
```

Change into the directory where you copied weatherclock e.g. ..
```
cd weatherclock
```
By default the weather function is disabled. To enable this the following variables need to be set.
Take a copy of weatherclock.py and save it somewhere safe!
```
1 - The variable weatherIP needs to be set to your CumulusMX IP address. (A prototype address 192.168.1.1:8998 is set as a template)
2 - The variable wdisp needs to be set to  -1 [wdisp = int(-1)] to enable display of weather data.
3 - The variable cmx needs to be set to 1 to enable display switching between Weather data and calendar data
```
Running weatherclock
--------------------
```
python3 /home/pi/weatherclock/weatherclock.py  
```
will start the application.

This MUST be run from the console on which it is to be displayed.

To exit weatherflow press keys Z and X at the same time.

weatherclock comes up in non-weather mode by default

There is a crude way to auto-start it at boot - the usual cron based methods don't work out of the box and I need to work out how to set the correct enviroment for running.

The 'crude' way is to include the following lines at the end of the .bashrc file in the pi home directory.  It's a hidden file but should be there!
```
# start weatherclock if not already running
{ if ! ps -ax | grep python3 | grep
weatherclock.py; then /usr/bin/python3 /home/pi/weatherclock/weatherclock.py
fi } &> /dev/null
```
This checks to see if python3 is running weatherclock.  If not - then start it. If it is do nothing - allowing multiple logins for user pi without generating errors.  

Using Weatherclock
------------------

By default the weatherclock comes up in basic clock mode - LHS displays a 'studio' style clock and the RHS shows day, date, month and year

When it is configured for CumulusMX connection the RHS can display the following weather information: (T)emperature, (P)ressure, (W)ind speed and direction, (R)ainfall, (UV)index together with Sunrise and sunset times for the day.  

In this configuration weatherclock starts up with the weather display on the RHS.  To switch between weather information and clock information is straight forward. Touch the screen on the RHS - and the weather information is displayed.  Touch it on the LHS and the calendar will be displayed in place of the weather.  If you are trying this on a non-touch screen then you will need to edit the following command (it's on line 11):

Change pygame.mouse.set_visible(False) to pygame.mouse.set_visible(True).  This will allow you to use a mouse to click on the relevant side of the display.

User configuration
------------------

The source file (weatherclock.py) in the download can be modified as you see fit.  Please take a copy before you change anything - it saves problems later on. I recommend using an editor that 'understands' Python.  Python3 is very 'picky' about formatting - a space in the wrong place causes problems. I used the editor ATOM (https://www.atom.io)

The usual things to change (other than the variables as explained above) are the colour definitions - these are defined as three numbers representing (Red, Green, Blue) with values between 0 (off) to 255 (full intensity). A bright yellow, for instance is (255, 255, 0).

Please feel free to play with the code - no support is offered!

NB  Requires Python3 and pygame 1.9.x and SDL 1.2

At present there is no support on Raspberry Pi Debian Buster for pygame 2.0.x and SDL 2

Acknowledgements
----------------

The clock display part of this code is based on the excellent pirsfullclock-master (https://github.com/jdgwarren/pirsclockfull) which is a Studio Clock
