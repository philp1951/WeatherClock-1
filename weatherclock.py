#! /usr/bin/env python
import pygame , sys , math, time, os, requests, json
from pygame.locals import *

# set to point display to the attached TFT Touch Screen if fitted
os.environ['SDL_VIDEODRIVER']="fbcon"

pygame.init()
bg = pygame.display.set_mode()

pygame.mouse.set_visible(False)

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
weatxtsize     = int(bg.get_height()/10)
indboxy        = int(bg.get_height()/6)
indboxx        = int(bg.get_width()/2.5)

# Coords of items on display
xclockpos      = int(bg.get_width()*0.2875)
ycenter        = int(bg.get_height()/2)
xtxtpos        = int(bg.get_width()*0.75)
xindboxpos     = int(xtxtpos-(indboxx/2))
ind1y          = int((ycenter*0.4)-(indboxy/2))
ind2y          = int((ycenter*0.8)-(indboxy/2))
ind3y          = int((ycenter*1.2)-(indboxy/2))
ind4y          = int((ycenter*1.6)-(indboxy/2))
txthmy         = int(ycenter-digiclockspace)
txtsecy        = int(ycenter+digiclockspace)

# Fonts
clockfont     = pygame.font.Font(None,digiclocksize)
indfont       = pygame.font.Font(None,indtxtsize)
weafont       = pygame.font.Font(None,weatxtsize)

# Indicator text - used to display daat on RHS of display

ind1txt       = indfont.render("MMMM",True,bgcolour)
ind2txt       = indfont.render("MMMM",True,bgcolour)
ind3txt       = indfont.render("MMMM",True,bgcolour)
ind4txt       = indfont.render("MMMM",True,bgcolour)
wwind         = "N"

# Indicator positions
txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=ycenter*0.4)
txtposind2 = ind2txt.get_rect(centerx=xtxtpos,centery=ycenter*0.8)
txtposind3 = ind3txt.get_rect(centerx=xtxtpos,centery=ycenter*1.2)
txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.6)

# Weather URL information used to get data from CumulusMX system
# requires IP address of CumulusMX system and list of items (webtags) to retrieve
# SEE CUMULUS Wiki for full list of webtags available  edit next two lines
# to reflect your system

weatherIP = "192.168.1.17:8998"
weathertags = "temp&rfall&wlatest&currentwdir&press&tempunitnodeg&rainunit&pressunit&windunit"

# Form the full URL

weatherURL = "http://"+weatherIP+"/api/tags/process.json?"+weathertags

# Parametric Equations of a Circle to get the markers
# 90 Degree offset to start at 0 seconds marker
# Equation for second markers
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))

#x = requests.get("http://192.168.1.17:8998/api/tags/process.json?temp&rfall&wlatest&currentwdir&press")

x = requests.get(weatherURL)
if x.status_code == 200:
            # process JSON data if valid
    weather = x.json()
    wwind = "W "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
    wtemp = "T "+weather["temp"] + " " + " \xb0" + weather["tempunitnodeg"]
    wrain = "R "+weather["rfall"] + " " + weather["rainunit"]
    wpress = "P "+weather["press"] + " " + weather["pressunit"]
else:
    wwind = " "
    wtemp = "NO WEATHER!"
    wrain = " "
    wpress = " "

# Main loop:  Keyboard "q" and "t" togther quits program
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
    ind1txt = indfont.render(retrieveday,True,calcolour)
    ind2txt = indfont.render(retrievedate,True,calcolour)
    ind3txt = indfont.render(retrievemon,True,calcolour)
    ind4txt = indfont.render(retrieveyr,True,calcolour)

#Update weather info every 30 seconds
    if int(retrievesec) == 30 or int(retrievesec) == 0:
        x = requests.get(weatherURL)
        #x = requests.get("http://192.168.1.17:8998/api/tags/process.json?temp&rfall&wlatest&currentwdir&press")
        if x.status_code == 200:
            # process JSON data if valid response
            weather = x.json()
            # Format display text
            wwind = "W "+ weather["wlatest"] + " "+ weather["windunit"] + " " + weather["currentwdir"]
            wtemp = "T "+weather["temp"] + " " + " \xb0" + weather["tempunitnodeg"]
            wrain = "R "+weather["rfall"] + " " + weather["rainunit"]
            wpress = "P "+weather["press"] + " " + weather["pressunit"]
        else:
            wwind = " "
            wtemp = "NO WEATHER!"
            wrain = " "
            wpress = " "

    #  Set up data for right hand side of screen
    #  Can be date or weather etc
    # Default is weather

    ind1txt = weafont.render(wtemp,True,weacolour)
    ind2txt = weafont.render(wpress,True,weacolour)
    ind3txt = weafont.render(wwind,True,weacolour)
    ind4txt = weafont.render(wrain,True,weacolour)

    if int(retrievesec) > 14  and int(retrievesec) < 30:
        ind1txt = indfont.render(retrieveday,True,calcolour)
        ind2txt = indfont.render(retrievedate,True,calcolour)
        ind3txt = indfont.render(retrievemon,True,calcolour)
        ind4txt = indfont.render(retrieveyr,True,calcolour)

    if int(retrievesec) > 44 and int(retrievesec) < 59:
        ind1txt = indfont.render(retrieveday,True,calcolour)
        ind2txt = indfont.render(retrievedate,True,calcolour)
        ind3txt = indfont.render(retrievemon,True,calcolour)
        ind4txt = indfont.render(retrieveyr,True,calcolour)

    # Align it
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)


    # Render the text
    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    bg.blit(ind1txt, txtposind1)
    bg.blit(ind2txt, txtposind2)
    bg.blit(ind3txt, txtposind3)
    bg.blit(ind4txt, txtposind4)

    time.sleep(0.04)
    pygame.time.Clock().tick(25)
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Pressing q+t to exit
        if event.type == KEYDOWN:
            if event.key == K_z and K_q:
                pygame.quit()
                sys.exit()
