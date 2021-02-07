weatherclock

Weatherclock is a Raspberry Pi "Studio" style clock written in python3 using pygame with calendar and weather display on (16:9) monitors, displays and TVs.

This was designed specifically for the Raspberry Pi.

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

Use raspi-config to -

enable SSH support
boot into console with auto-login
wait for network on boot - required to ensure internal clock is correct and for the initial read of the CumulusMX system.

Booting into console mode allows the display to use the whole screen (important for smaller displays).

Installation of weatherclock
----------------------------

issue the following commands:

 sudo apt update
 sudo apt upgrade

The following command will ensure that the necessary Python tools are installed

 sudo apt install python-setuptools

Change into the directory where you copied weatherclock e.g. ..

 cd weatherclock

By default the weather function is disabled. To enable this function two variables need to be set.
Take a copy of weatherclock.py and save it somewhere safe!
1 - The variable weatherIP needs to be set to your CumulusMX IP address. (A prototype address 192.168.1.17:8998 is set as a template)
2 - The variable wdisp need to be set to  -1 [wdisp = int(-1)] to enable display.


Then build the application...

 sudo python3 setup install

This will create all the required files

Running weatherclock
--------------------

 /usr/local/bin/weatherclock.py   

will start the application.

This MUST be run from the console on which it is to be displayed.

To exit weatherflow press keys Z and X at the same time.


User configuration
------------------

The source file (weatherclock.py) in the download can be modified as you see fit.  Please take a copy before you change anything - it saves problems later on. I recommend using an editor that 'understands' Python.  Python3 is very 'picky' about formatting - a space in the wrong place causes problems. I used the editor ATOM (https://www.atom.io)

The usual things to change (other than the weatherIP and wdisp variables as explained above) are the colour definitions - these are defined as three numbers representing (Red, Green, Blue) with values between 0 (off) to 255 (full intensity). A bright yellow, for instance is (255, 255, 0).

Please feel free to play with the code - no support is offered!

Acknowledgements
----------------

The clock display part of this code is based on the excellent pirsfullclock-master (https://github.com/jdgwarren/pirsclockfull) which is a "true" Studio Clock
