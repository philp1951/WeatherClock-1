weatherclock

Version 1.4.1

Weatherclock is a Raspberry Pi "Studio" style clock written in python3 using pygame with day/date and weather information.

The main changes to this version are: the use of multiple pygame surfaces to create the display and the method of retrieving weather information.

This was designed specifically for the Raspberry Pi and Raspberry Pi 7" touch screen although it will work on systems running Python3 (e.g. Windows 10 and Ubuntu)

The weather information is retrieved from a webserver that is populated by a CumulusMX system using the Extra Web files section of the CumulusMX system

It may be run under Python 3 on other systems - it has been extensively tested on Windows 10 (It is developed on a Windows 10 system).

Status:
-------

weatherclock is stable and ready for use but no support is offered.

Hardware
--------
weatherclock is designed to be run on a Raspberry Pi with the Raspberry Pi 7" Touchscreen display.  
It can be also set to run on Windows 10 under Python 3.x


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
Running weatherclock
--------------------

For Raspberry Pi
```
python3 /home/pi/weatherclock/weatherclock.py  
```
will start the application.

This MUST be run from the console on which it is to be displayed.

There is a crude way to auto-start it at boot - the usual cron based methods don't work out of the box and I need to work out how to set the correct environment for running.

The 'crude' way is to include the following lines at the end of the .bashrc file in the pi home directory.  It's a hidden file but should be there!
```
# start weatherclock if not already running
{
if ! ps -ax | grep python3 | grep weatherclock.py; then
  /usr/bin/python3 /home/pi/weatherclock/weatherclock.py
fi
} &> /dev/null
```
When you login using pi as the user name this checks to see if python3 is running weatherclock.  If not - then start it. If it is do nothing - allowing multiple logins for user pi without generating errors.  Setting auto login to console using raspi-config should auto start weatherclock at boot time.

For Windows systems (e.g. Windows 10, Ubuntu 20.04 etc) it will run from the Python 3.x environment.  From a terminal go to the relevant directory and start Python3 with the correct file.  E.G

```
>Python3 weatherclock.py  
```
or however your system runs python3

To exit weatherflow press keys Z and X at the same time.

Using Weatherclock
------------------
The LHS of the screen will display a "studio" style clock with a central display showing Day date and time with seconds being 'illuminated' dots.

The RHS will display the following weather information: Temperature, Pressure, Wind speed and direction, Rainfall, Solar  together with Sunrise and Sunset times for the day.  

The temperature an pressure values have trend colours associated with them. They indicate the following:
    RED     Falling value
    GREEN   Rising value
    BLUE    Steady value

User configuration
------------------
The distribution includes a file called realtimeclockT.txt.  This should be copied to your system that runs CumulusMX and your Extra Web Files section updated to include processing of this file in real time and copying it to your webserver.  You can call the processed file anything you want - but make sure you edit the weatherURL parameter in the code accordingly - see paragraph below.

The source files (weatherclock.py) in the download can be modified as you see fit (AT YOUR OWN RISK!!) Please take a copy before you change anything - it saves problems later on. I recommend using an editor that 'understands' Python.  Python3 is very 'picky' about formatting - a space in the wrong place causes problems. I used ATOM (https://www.atom.io)  At present it is a non-trivial task to scale the display up as some of the formatting for the weather information is dependant on the font used.  But 800*480 works well on Windows 10 / Un^X systems!


The main change is to the line
```
weatherURL = "https://your.web.server/yourrealtimeclock.txt"
```
This should be changed to point to your web server and realtimeclock file as described above.

You may wish to change the following line to reflect the actual real time update timer of your CumulusMX system.

```
updatesec = int(15)
```
The default above will re-read yourrealtimeclock.txt (or whatever you call it) file every 15 seconds.  

```
timout = int(1)
```
Time out value (in seconds) for the GET request. The supplied value should be sufficient for most networks.

The values under ERROR on the display indicates the last error code and number of error.  

The usual things to change (other than the variables as explained above) are the colour definitions - these are defined as three numbers representing (Red, Green, Blue) with values between 0 (off) to 255 (full intensity). A bright yellow, for instance is (255, 255, 0).

Please feel free to play with the code - no support is offered!

NB  Requires Python3 and pygame 1.9.x and SDL 1.2

At present there is no support on Raspberry Pi Debian Buster for pygame 2.0.x and SDL 2

Acknowledgements
----------------

The clock display part of this code is based on the excellent pirsfullclock-master (https://github.com/jdgwarren/pirsclockfull) which is a Studio Clock
