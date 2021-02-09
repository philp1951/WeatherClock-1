#! /usr/bin/env python
import pygame , sys , math, time, os, requests, json
from pygame.locals import *

# set to point display to the attached TFT Touch Screen if fitted
os.environ['SDL_VIDEODRIVER']="directfb"

pygame.init()
bg = pygame.display.set_mode()

pygame.mouse.set_visible(False)

# CUSTOM SETTINGS START HERE
# Information used to get data from CumulusMX system.
# set wdisp = 1 to enable CumulusMX support, -1 to disable
# set cmx = 1 to enable weather display switching, -1 to disable
# Default is no weather display

wdisp = int(-1)
cmx = int(-1)

# this is the IP address of the CumulusMX system.

weatherIP = "192.168.1.1:8998"


# Series of webtags to retrieve from CumulusMX
# If your station does NOT have a UV sensor remove the &UV from the end of the next variable
# and comment out lines with the variable "wuv" in them - a total of 4 lines.

weathertags = "temp&rfall&wlatest&currentwdir&press&tempunitnodeg&rainunit&pressunit&windunit&sunrise&sunset&UV"

# CUSTOM SETTINGS END HERE

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0,   0,   0  )
clockcolour    = (255, 0, 0)
seccolour      = (0, 255, 0)
timecolour     = (255,0,255)
weacolour      = (255, 255, 0)
calcolour      = (255, 255, 0)

# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/3.5)
digiclockspace = int(bg.get_height()/10.5)
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
xtxtpos        = int(bg.get_width()*0.55)
txthmy         = int(ycentre-digiclockspace)
txtsecy        = int(ycentre+digiclockspace)

# Fonts
clockfont     = pygame.font.Font(None,digiclocksize)
indfont       = pygame.font.Font(None,indtxtsize)
weafont       = pygame.font.Font(None,weatxtsize)


# Form the full CumulusMX request URL

weatherURL = "http://"+weatherIP+"/api/tags/process.json?"+weathertags

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

if wdisp > 0:
    x = requests.get(weatherURL)
    if x.status_code == 200:
            # process JSON data if valid
            weather = x.json()
            wwind = "W "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
            wtemp = "T "+weather["temp"] + " " + " \xb0" + weather["tempunitnodeg"]
            wrain = "R "+weather["rfall"] + " " + weather["rainunit"]
            wpress = "P "+weather["press"] + " " + weather["pressunit"]
            wuv = "UV "+weather["UV"]
            wsup = "Sunrise " + weather["sunrise"]
            wsdown = "Sunset " + weather["sunset"]
    else:
            wwind = " "
            wtemp = "NO WEATHER!"
            wrain = " "
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
    retrievedate = time.strftime("%-d",time.localtime(time.time()))
    retrievemon = time.strftime("%b",time.localtime(time.time()))
    retrieveyr = time.strftime("%Y",time.localtime(time.time()))
    daydate = retrieveday + " " + retrievedate

    digiclockhm = clockfont.render(retrievehm,True,timecolour)
    digiclocksec = clockfont.render(retrievesec,True,timecolour)

#Update weather info every 30 seconds
    if int(retrievesec) == 30 or int(retrievesec) == 0 and wdisp > 0:
        x = requests.get(weatherURL)
        if x.status_code == 200:
            # process JSON data if valid
            weather = x.json()
            wwind = "W "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
            wtemp = "T  "+weather["temp"] + " " + " \xb0" + weather["tempunitnodeg"]
            wrain = "R  "+weather["rfall"] + " " + weather["rainunit"]
            wpress = "P  "+weather["press"] + " " + weather["pressunit"]
            wuv = "UV  "+ weather["UV"]
            wsup = "Sunrise " + weather["sunrise"]
            wsdown = "Sunset  " + weather["sunset"]
        else:
            wwind = " "
            wtemp = "NO WEATHER!"
            wrain = " "
            wpress = " "
            wuv = " "
            wsup = " "
            wdown = " "

    #  Set up data for right hand side of screen
    #  Can be date or weather

    if wdisp < 0:
        ind1txt = indfont.render(retrieveday,True,calcolour)
        ind2txt = indfont.render(retrievedate,True,calcolour)
        ind3txt = indfont.render(retrievemon,True,calcolour)
        ind4txt = indfont.render(retrieveyr,True,calcolour)
        ind5txt = indfont.render(" ",True,calcolour)
        txt1pos = (xtxtpos,int(yheight*0.05))
        txt2pos = (xtxtpos,int(yheight*0.3))
        txt3pos = (xtxtpos,int(yheight*0.55))
        txt4pos = (xtxtpos,int(yheight*0.8))

    if wdisp > 0:
        ind1txt = weafont.render(wtemp,True,weacolour)
        ind2txt = weafont.render(wpress,True,weacolour)
        ind3txt = weafont.render(wwind,True,weacolour)
        ind4txt = weafont.render(wrain,True,weacolour)
        ind5txt = weafont.render(wuv,True,weacolour)
        ind6txt = weafont.render(wsup,True,weacolour)
        ind7txt = weafont.render(wsdown,True,weacolour)
        txt1pos = (xtxtpos,int(yheight*0.01))
        txt2pos = (xtxtpos,int(yheight*0.14))
        txt3pos = (xtxtpos,int(yheight*0.28))
        txt4pos = (xtxtpos,int(yheight*0.42))
        txt5pos = (xtxtpos,int(yheight*0.56))
        txt6pos = (xtxtpos,int(yheight*0.7))
        txt7pos = (xtxtpos,int(yheight*0.84))

    # Align it
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)


    # Render the text
    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    bg.blit(ind1txt, txt1pos)
    bg.blit(ind2txt, txt2pos)
    bg.blit(ind3txt, txt3pos)
    bg.blit(ind4txt, txt4pos)
    if wdisp > 0:
        bg.blit(ind5txt, txt5pos)
        bg.blit(ind6txt, txt6pos)
        bg.blit(ind7txt, txt7pos)

    time.sleep(0.04)
    pygame.time.Clock().tick(25)
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Pressing z and q to exit
        if event.type == KEYDOWN:
            if event.key == K_z and K_q:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN and cmx > 0:
            # Flip RHS of screen to other option
            if pygame.mouse.get_pos()[0] > xcentre: wdisp = int(1)
            if pygame.mouse.get_pos()[0] <= xcentre: wdisp = int(-1)
