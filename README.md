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
PLEASE NOTE:
I have not tested this under 64bit Debian on a Raspberry Pi.  Some people have tried without success.  

weatherclock is designed to run on Raspberry Pi under Debian 10 (Buster) / or Debian 11 (Bullseye) (32bit OS) with pygame and Python3. weatherclock requires Debian desktop (NOT the -lite variant)

If you are unsure how to do this please see https://www.raspberrypi.org/software/raspberry-pi-desktop/  

It is expected that the OS is already installed BUT note the following:

Use
```
sudo raspi-config
```
to -
```
enable SSH support - for access to system from other machines - to change variables for example.
boot into console with auto-login  (If running Bullseye note that the default user pi is no longer created)
wait for network on boot - required to ensure internal clock is correct and for the initial read of the CumulusMX system.
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
The following variables need to be set.
Take a copy of weatherclock.py and save it somewhere safe!
```
1 - The variable weatherIP needs to be set to your CumulusMX IP address. (A prototype address 192.168.1.1:8998 is set as a template)
```
Running weatherclock
--------------------
```
python3 /home/pi/weatherclock/weatherclock.py  
```
will start the application.

This MUST be run from the console on which it is to be displayed.

To exit weatherflow press keys Z and X at the same time.

There is a crude way to auto-start it at boot - the usual cron based methods don't work out of the box and I need to work out how to set the correct enviroment for running.

The 'crude' way is to include the following lines at the end of the .bashrc file in the user home directory.  It's a hidden file but should be there!
```
# start weatherclock if not already running
{
if ! ps -ax | grep python3 | grep weatherclock.py; then
  sleep 5; /usr/bin/python3 /home/"username"/weatherclock/weatherclock.py
fi
} &> /dev/null
```

N.B. the sleep 5 command above delays the start of the program.  Although the network should be up it appears that not all the required network connections are made
by the time the application is run.

This checks to see if python is running weatherclock.  If not - then start it. If it is do nothing - allowing multiple logins for user without generating errors.  

Using Weatherclock
------------------

Weatherclock comes up wth LHS displaying a 'studio' style clock and the RHS displays the following weather information: (T)emperature, (P)ressure, (W)ind speed and direction,
(R)ainfall, Solar Power and (UV)index together with Sunrise and sunset times for the day.  The status of the link to the CumulusMX system is also displayed.

Other Operating Systems.
------------------

I have successfully run this version with Python under Windows 11 on a 64 bit Intel system.  No support offered for this but you should be able to get it to work!

It also runs successfully under UBUNTU 23.04 on 64bit Intel PC

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
