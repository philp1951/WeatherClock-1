#! /usr/bin/env python
import pygame , sys , math, time, os, requests, json, random
from pygame.locals import *

# set to point display to the attached TFT Touch Screen if fitted - uncoment to select this option
# Need to uncomment to run on Raspberry Pi with touch screen

#os.environ['SDL_VIDEODRIVER']="directfb"

pygame.init()

# ONLY ONE OF THESE TWO LINES SHOULD BE UNCOMMENTED!!

#bg = pygame.display.set_mode()         # Uncomment this line for Raspberry Pi
bg = pygame.display.set_mode((800,480)) # Uncomment this line for Windows 10 - edit screen size if desired

pygame.mouse.set_visible(False)

# CUSTOM SETTINGS START HERE
# Information used to get data from CumulusMX system.
# set wdisp = 1 to enable CumulusMX support, -1 to disable
# Default is weather display

wdisp = int(1)

# this section is used to set the IP address of the system.
# select both weathertags and weatherIP IF you are geting data directly
# from you local CumulusMX system
#NB YOU WILL NEED TO EDIT THE ADDRESS TO REFLECT YOUR SYSTEM

# Series of webtags to retrieve from CumulusMX
# If your station does NOT have a UV sensor remove the &UV from the end of the next variable
# and comment out lines with the variable "wuv" in them - a total of 5 lines.  Search for "wuv" and comment out the lines

weathertags = "temp&rfall&wlatest&currentwdir&press&tempunit&rainunit&pressunit&windunit&temptrend&presstrendval&sunrise&sunset&UV"
weatherIP = "http://192.168.1.17:8998/api/tags/process.json?"  # CHANGE address to point to your CumulusMX system

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0,   0,   0  )
clockcolour    = (255, 0, 0)
seccolour      = (0, 255, 0)
timecolour     = (255,0,255)
weacolour      = (255, 255, 0)
calcolour      = (255, 255, 0)
trendcolourup     = (0, 255, 0)  #GREEN
trendcolourdown   = (255, 0, 0)  #RED
trendcoloursteady = (0, 0, 255)  #BLUE
# CUSTOM SETTINGS END HERE

# Generate random int used to prevent multiple occurences requesting data at same time

delta = random.randint (1,15)

# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/5)
digiclockspace = int(bg.get_height()/12)
dotsize        = int(bg.get_height()/90)
hradius        = bg.get_height()/2.5
secradius      = hradius - (bg.get_height()/26)
indtxtsize     = int(bg.get_height()/5)
weatxtsize     = int(bg.get_height()/8)

# Coords of items on display
xclockpos      = int(bg.get_width()*0.2875)
xcentre        = int(bg.get_width()/2)
ycentre        = int(bg.get_height()/2)
yheight        = int(bg.get_height())
xtxtpos        = int(bg.get_width()*0.6)
trendpos       = int(bg.get_width()*0.58)
txthmy         = int(ycentre-digiclockspace)
txtsecy        = int(ycentre+digiclockspace)
txtday         = int(ycentre-(2.5*digiclockspace))
txtmon         = int(ycentre+(2.5*digiclockspace))

# Y position for datat line (8 in total)
yt1         =    int(yheight*0.01)
yt2         =    int(yheight*0.14)
yt3         =    int(yheight*0.28)
yt4         =    int(yheight*0.42)
yt5         =    int(yheight*0.56)
yt6         =    int(yheight*0.7)
yt7         =    int(yheight*0.84)

# Fonts
clockfont     = pygame.font.Font(None,digiclocksize)
dayfont       = pygame.font.Font(None,int(digiclocksize/2))
indfont       = pygame.font.Font(None,indtxtsize)
weafont       = pygame.font.Font(None,weatxtsize)


# Form the full CumulusMX request URL

weatherURL = weatherIP+weathertags

# Parametric Equations of a Circle to get the markers
# 90 Degree offset to start at 0 seconds marker
# Equation for second markers
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycentre-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycentre-(int(hradius*(math.sin(math.radians((shy)+90)))))

# NOW get data

if wdisp > 0:
    x = requests.get(weatherURL, timeout=2)
    if x.status_code == 200:
            # process JSON data if valid
            weather = x.json()
            wwind = "Wind "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
            wtemp = "Temp  "+weather["temp"] +  " \u00B0" + weather["tempunit"][6:]
            wrain = "Rain  "+weather["rfall"] + " " + weather["rainunit"]
            wpress = "Press  "+weather["press"] + " " + weather["pressunit"]
            wuv = "UV  "+ weather["UV"]
            wsup = "Sunrise " + weather["sunrise"]
            wsdown = "Sunset  " + weather["sunset"]
            tempt = float(weather["temptrend"])
            presst = float(weather["presstrendval"])
    if x.status_code != 200:
            wwind = " "
            wtemp = "NO WEATHER!"
            wrain = str(x.status_code)
            wpress = " "
            wuv = " "
            wsup = " "
            wdown = " "

# Main loop:  Keyboard "z" and "x" togther will exit the program

while True :
    pygame.display.update()

    bg.fill(bgcolour)

    # Retrieve seconds and turn them into integers
    sectime = int(time.strftime("%S",time.localtime(time.time())))

    # To get the dots in sync with the seconds
    secdeg  = (sectime+1)*6

    # Draw second markers
    smx=smy=0
    #prx=pry=secdeg-6

    while smx < secdeg:
       pygame.draw.circle(bg,seccolour,(paraeqsmx(smx),paraeqsmy(smy)),dotsize)
       if secdeg > 0:
           pygame.draw.circle(bg,bgcolour,(paraeqsmx(0),paraeqsmy(0)),dotsize)
       smy += 6  # 6 Degrees per second
       smx += 6

    # Draw hour markers
    shx=shy=0
    while shx < 360:
        pygame.draw.circle(bg,clockcolour,(paraeqshx(shx),paraeqshy(shy)),dotsize)
        shy += 30  # 30 Degrees per hour
        shx += 30

    # Retrieve time for digital clock
    retrievehm = time.strftime("%H:%M",time.localtime(time.time()))
    retrievesec = time.strftime("%S",time.localtime(time.time()))
    retrieveday = time.strftime("%a",time.localtime(time.time()))
    retrievedate = time.strftime("%d",time.localtime(time.time()))
    retrievemon = time.strftime("%b",time.localtime(time.time()))
    retrieveyr = time.strftime("%Y",time.localtime(time.time()))
    daydate = retrieveday + " " + retrievedate
    yrmon = retrievemon + " " + retrieveyr

    digiclockhm = clockfont.render(retrievehm,True,timecolour)
    digiclocksec = clockfont.render(retrievesec,True,timecolour)
    digiclockday = dayfont.render(daydate,True,clockcolour)
    digiclockmon = dayfont.render(yrmon,True,clockcolour)

#Update weather info every 30 seconds - offset by random number between 0 and 15

    if int(retrievesec) == (30+delta) or int(retrievesec) == (0 + delta) and wdisp > 0:
        x = requests.get(weatherURL, timeout = 2)
        if x.status_code == 200:
            # process JSON data if valid
            weather = x.json()
            wwind = "Wind "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
            wtemp = "Temp  "+weather["temp"] + " \u00B0" + weather["tempunit"][6:]
            wrain = "Rain  "+weather["rfall"] + " " + weather["rainunit"]
            wpress = "Press  "+weather["press"] + " " + weather["pressunit"]
            wuv = "UV  "+ weather["UV"]
            wsup = "Sunrise " + weather["sunrise"]
            wsdown = "Sunset  " + weather["sunset"]
            tempt = float(weather["temptrend"])
            presst = float(weather["presstrendval"])
        if x.status_code != 200:
            wwind = " "
            wtemp = "NO WEATHER!"
            wrain = str(x.status_code)
            wpress = " "
            wuv = " "
            wsup = " "
            wdown = " "

    # Set up data for right hand side of screen (weather)

    if wdisp > 0:
        ind1txt = dayfont.render(wtemp,True,weacolour)
        ind2txt = dayfont.render(wpress,True,weacolour)
        ind3txt = dayfont.render(wwind,True,weacolour)
        ind4txt = dayfont.render(wrain,True,weacolour)
        ind5txt = dayfont.render(wuv,True,weacolour)
        ind6txt = dayfont.render(wsup,True,weacolour)
        ind7txt = dayfont.render(wsdown,True,weacolour)
        txt1pos = (xtxtpos,yt1)
        txt2pos = (xtxtpos,yt2)
        txt3pos = (xtxtpos,yt3)
        txt4pos = (xtxtpos,yt4)
        txt5pos = (xtxtpos,yt5)
        txt6pos = (xtxtpos,yt6)
        txt7pos = (xtxtpos,yt7)

    # Align it
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)
    txtposday     = digiclockday.get_rect(centerx=xclockpos,centery=txtday)
    txtposmon     = digiclockmon.get_rect(centerx=xclockpos,centery=txtmon)


    # Render the text
    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    bg.blit(digiclockday, txtposday)
    bg.blit(digiclockmon, txtposmon)
    bg.blit(ind1txt, txt1pos)
    bg.blit(ind2txt, txt2pos)
    bg.blit(ind3txt, txt3pos)
    bg.blit(ind4txt, txt4pos)
    if wdisp > 0:
        bg.blit(ind5txt, txt5pos)
        bg.blit(ind6txt, txt6pos)
        bg.blit(ind7txt, txt7pos)

# Now draw trend dots

    if tempt > 0.0:
        tcolour = trendcolourup
    elif tempt < 0.0:
        tcolour = trendcolourdown
    elif tempt == 0.0:
        tcolour = trendcoloursteady
    pygame.draw.circle(bg,tcolour,(trendpos,int(yt1+(weatxtsize/4))),dotsize)

    if presst > 0.0:
        tcolour = trendcolourup
    elif presst < 0.0:
        tcolour = trendcolourdown
    elif presst == 0.0:
        tcolour = trendcoloursteady

    pygame.draw.circle(bg,tcolour,(trendpos,int(yt2+(weatxtsize/4))),dotsize)

# pause a bit then repeat!

    time.sleep(0.04)
    pygame.time.Clock().tick(25)

#Check for ending codes

    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Pressing z and q to exit
        if event.type == KEYDOWN:
            if event.key == K_z and K_q:
                pygame.quit()
                sys.exit()
