#! /usr/bin/env python
import pygame , sys , math, time, os, requests, json, random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,480)) # set physical screen
bg = pygame.Surface((400,480)) # Surface for clock
we = pygame.Surface((400,480)) # surface for weather information

pygame.mouse.set_visible(False) #Set true if you need to use mouse (shouldn't be needed!)

# CUSTOM SETTINGS START HERE
# Information used to get data from CumulusMX system.

# URL of your web server together with the webtags required

# Format is ip address:port/process.json?webtag1,webtag2...
# See the CumulusMX Wiki for more details
# If your station doesn't have a solar sensor than edit as required

weatherURL = "http://192.168.1.57:8998/api/tags/process.json?temp&tempTH&tempTL&tempunitnoenc&temptrend"
weatherURL = weatherURL + "&press&pressTH&pressTL&pressunit&presstrendval"
weatherURL = weatherURL + "&wlatest&wgust&currentwdir&windunit"
weatherURL = weatherURL + "&rfall&rmonth&ryear&rainunit"
weatherURL = weatherURL + "&SolarRad&UV&SunshineHours&sunrise&sunset&LightningStrikesToday"

weather = "Initial"     # define as a global
retrievesec = "0"	# define as global

updatesec = int(20)  # set to your CMX realtime update time (seconds)
timout = 1          #timeout value (secs) for GET requests
debug = False      # set True if you need to debug errors

# If using debug = True then start the application with something like
# python weatherclock.py >> error.log to gather connection error data

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0, 0, 0)
wecolour       = (0, 0, 0)
clockcolour    = (255, 0, 0)
seccolour      = (0, 255, 0)
timecolour     = (255,0,255)
weacolour      = (255, 255, 0)
calcolour      = (255, 255, 0)
tabcolour      = (255, 140, 50)
trendcolourup     = (0, 255, 0)  #GREEN
trendcolourdown   = (255, 0, 0)  #RED
trendcoloursteady = (0, 0, 255)  #BLUE
temptrendcol = trendcoloursteady
presstrendcol = trendcoloursteady
# CUSTOM SETTINGS END HERE

# Generate random int used to prevent multiple occurences requesting data at same time
delta = random.randint (1,15)

firsttime = int(1)  # Used to display weather data at first run
tout = int(0)       # used if timeout error occurs
ecode = str("---")         # request error code if defined
errtot = int(0)     # Running count of errors


# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/5)
digiclockspace = int(bg.get_height()/12)
dotsize        = int(bg.get_height()/90)
#hradius        = bg.get_height()/2.5
hradius        = int((bg.get_width()-20)/2)
secradius      = hradius - (bg.get_width()/25)
indtxtsize     = int(bg.get_height()/5)
weatxtsize     = int(bg.get_height()/8)

#  Next set of values are fixed - i.e. NOT proportinal to display sizes other than 800*480
#  If you want to have a larger screen display then these will need changing.
#  Also the two font sizes for the table display (lucida) will need changing

taby = 15
tabx = 90
tabinc = 120 # spacing for table data
tabsp = 80
datax = 30
datay = 50
tabj = 15 # justification for table headers
tabv = 15 # justification for data

# Coords of items on display
xclockpos      = int(bg.get_width()*0.5)
xcentre        = int(bg.get_width()/2)
ycentre        = int(bg.get_height()/2)
yheight        = int(bg.get_height())
xtxtpos        = int(bg.get_width()*0.6)
trendpos       = int(bg.get_width()*0.58)
txthmy         = int(ycentre-digiclockspace)
txtsecy        = int(ycentre+digiclockspace)
txtday         = int(ycentre-(2.5*digiclockspace))
txtmon         = int(ycentre+(2.5*digiclockspace))
statusmon      = int(yheight-20)        #for status and error count

# Fonts
clockfont     = pygame.font.Font(None,digiclocksize)
dayfont       = pygame.font.Font(None,int(digiclocksize/1.75))
weafont        = pygame.font.SysFont('lucida', 48)
tabfont        = pygame.font.SysFont('lucida', 32)
statfont        = pygame.font.SysFont('lucida', 24)

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


# NOW get first set of data - needed to generate headings
#tout = -1       #set timeout flag to ensure read is completed first time
#while tout < 0:
tout = -1
while tout < 0:
    x = requests.get(weatherURL, timeout = timout)
    x.encoding='utf-8-sig'
#    print(x.text)
    if x.status_code == 200:
        weather = json.loads(x.text)
        ecode = "FT"
        tout = 0         # clear timeout timeout flag
    else:
        tout = -1   # Try request later
        ecode = "N/C"
        errtot = errtot + 1        # Increment the count of errors
        time.sleep(updatesec)       # wait for a period

# OK Valid data now continue

# Generate Display table headings

h1t1 =  "Temp "  + weather["tempunitnoenc"]
h1t2 =  "High"
h1t3 =  "Low"

h11 = tabfont.render(h1t1, True, tabcolour)
h12 = tabfont.render(h1t2, True, tabcolour)
h13 = tabfont.render(h1t3, True, tabcolour)

h1t1Rect = h11.get_rect()
h1t2Rect = h12.get_rect()
h1t3Rect = h13.get_rect()

h1t1Rect.center = (tabx, taby)
h1t2Rect.center = (tabx + tabinc, taby)
h1t3Rect.center = (tabx+ 2*tabinc, taby)

# Line 2 Headings (Pressure)

h2t1 =  "Press" +" " + weather["pressunit"]
h2t2 =  "High"
h2t3 =  "Low"

h21 = tabfont.render(h2t1, True, tabcolour)
h22 = tabfont.render(h2t2, True, tabcolour)
h23 = tabfont.render(h2t3, True, tabcolour)
h2t1Rect = h21.get_rect()
h2t2Rect = h22.get_rect()
h2t3Rect = h23.get_rect()

h2t1Rect.center = (tabx, taby+tabsp)
h2t2Rect.center = (tabx + tabinc, taby+tabsp)
h2t3Rect.center = (tabx+ 2*tabinc, taby+tabsp)

# Line 3 Headings (Wind)

h3t1 =  "Wind" +" " + weather["windunit"]
h3t2 =  "Gust"
h3t3 =  "From"

h31 = tabfont.render(h3t1, True, tabcolour)
h32 = tabfont.render(h3t2, True, tabcolour)
h33 = tabfont.render(h3t3, True, tabcolour)
h3t1Rect = h31.get_rect()
h3t2Rect = h32.get_rect()
h3t3Rect = h33.get_rect()

h3t1Rect.center = (tabx, taby+2*tabsp)
h3t2Rect.center = (tabx + tabinc, taby+2*tabsp)
h3t3Rect.center = (tabx+ 2*tabinc, taby+2*tabsp)

# Line 4 Headings (Rain)

h4t1 =  "Rain" +" " + weather["rainunit"]
h4t2 =  "Month"
h4t3 =  "Year"

h41 = tabfont.render(h4t1, True, tabcolour)
h42 = tabfont.render(h4t2, True, tabcolour)
h43 = tabfont.render(h4t3, True, tabcolour)
h4t1Rect = h41.get_rect()
h4t2Rect = h42.get_rect()
h4t3Rect = h43.get_rect()

h4t1Rect.center = (tabx, taby+3*tabsp)
h4t2Rect.center = (tabx + tabinc, taby+3*tabsp)
h4t3Rect.center = (tabx+ 2*tabinc, taby+3*tabsp)

# Comment out next 12 code lines if your station doesn't have a solar sensor
# Line 5 Headings (Solar)

h5t1 =  "Sun w/m"+"\u00B2"
h5t2 =  "UVI"
h5t3 =  "Sun Hours"

h51 = tabfont.render(h5t1, True, tabcolour)
h52 = tabfont.render(h5t2, True, tabcolour)
h53 = tabfont.render(h5t3, True, tabcolour)
h5t1Rect = h51.get_rect()
h5t2Rect = h52.get_rect()
h5t3Rect = h53.get_rect()

h5t1Rect.center = (tabx, taby+4*tabsp)
h5t2Rect.center = (tabx + tabinc, taby+4*tabsp)
h5t3Rect.center = (tabx+ 2*tabinc, taby+4*tabsp)

#End of Solar Sensor section
# Line 6 Headings (Sun)

h6t1 =  "Sunrise"
h6t2 =  "Sunset"
h6t3 =  "Lightning"


h61 = tabfont.render(h6t1, True, tabcolour)
h62 = tabfont.render(h6t2, True, tabcolour)
h63 = tabfont.render(h6t3, True, tabcolour)

h6t1Rect = h61.get_rect()
h6t2Rect = h62.get_rect()
h6t3Rect = h63.get_rect()


h6t1Rect.center = (tabx, taby+5*tabsp)
h6t2Rect.center = (tabx + tabinc, taby+5*tabsp)
h6t3Rect.center = (tabx + 2*tabinc, taby+5*tabsp)

# MAIN LOOP:  KEYBOARD "z" AND "q" TOGTHER WILL EXIT THE PROGRAM

while True :

# pause a bit then repeat!

    time.sleep(0.1)
    pygame.time.Clock().tick(10)


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

# Update weather info every realtime seconds

    tout = -1			# ensure that one read is made! 
    if int(retrievesec) % updatesec == 0:
        while tout < 0: 
            x = requests.get(weatherURL, timeout = timout)
            x.encoding='utf-8-sig'
            #print(x.text)
            if x.status_code == 200:
                weather = json.loads(x.text)
                ecode = "OK"
                tout = 0         # clear timeout timeout flag
            else:
                tout = -1   # Try request later
                ecode = "N/C"
                time.sleep(updatesec)       # wait for a period

    firsttime = 0           # reset firsttime indicator

    bg.fill(bgcolour)  # redraw clock - start from scratch

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
    retrievedate = time.strftime("%e",time.localtime(time.time()))
    retrievemon = time.strftime("%b",time.localtime(time.time()))
    retrieveyr = time.strftime("%Y",time.localtime(time.time()))
    daydate = retrieveday + " " + retrievedate
    yrmon = retrievemon + " " + retrieveyr
    stat = "Status: " + ecode  + "  " + str(errtot)

    digiclockhm = clockfont.render(retrievehm,True,timecolour)
    digiclocksec = clockfont.render(retrievesec,True,timecolour)
    digiclockday = dayfont.render(daydate,True,clockcolour)
    digiclockmon = dayfont.render(yrmon,True,clockcolour)
    digiclockstat = statfont.render(stat,True,tabcolour)

    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)
    txtposday     = digiclockday.get_rect(centerx=xclockpos,centery=txtday)
    txtposmon     = digiclockmon.get_rect(centerx=xclockpos,centery=txtmon)
    txtposstat    = digiclockstat.get_rect(centerx=xclockpos+80,centery=statusmon)

    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    bg.blit(digiclockday, txtposday)
    bg.blit(digiclockmon, txtposmon)
    bg.blit(digiclockstat, txtposstat)


    screen.blit(bg, (0, 0))
    screen.blit(we, (400, 0))

    #pygame.display.update()
    pygame.display.update()
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



    # Set the trend colour for temp and pressure.
    # Rising = GREEN: Falling = RED: Steady = BLUE

    tempt = float(weather["temptrend"])
    presst = float(weather["presstrendval"])


    if tempt > 0.0:
        tcolour = trendcolourup
    elif tempt < 0.0:
        tcolour = trendcolourdown
    elif tempt == 0.0:
        tcolour = trendcoloursteady

    if presst > 0.0:
        pcolour = trendcolourup
    elif presst < 0.0:
        pcolour = trendcolourdown
    elif presst == 0.0:
        pcolour = trendcoloursteady

# NOW WE CAN CREATE THE VALUES PART OF THE TABLE
    we.fill(wecolour)       # clear surface
    #Line 1 (Temp) data

    l1t1 =  weather["temp"]
    l1t2 =  weather["tempTH"]
    l1t3 =  weather["tempTL"]

    l11 = weafont.render(l1t1, True, tcolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(l1t3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()

    l1t1Rect.center = (tabx, datay)
    l1t2Rect.center = (tabx + tabinc, datay)
    l1t3Rect.center = (tabx+ 2*tabinc, datay)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h11, h1t1Rect)
    we.blit(h12, h1t2Rect)
    we.blit(h13, h1t3Rect)

    # Line 2 (Pressure)

    l1t1 =  weather["press"]
    l1t2 =  weather["pressTH"]
    l1t3 =  weather["pressTL"]

    l11 = weafont.render(l1t1, True, pcolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(l1t3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()

    l1t1Rect.center = (tabx, datay+tabsp)
    l1t2Rect.center = (tabx + tabinc, datay+tabsp)
    l1t3Rect.center = (tabx+ 2*tabinc, datay+tabsp)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h21, h2t1Rect)
    we.blit(h22, h2t2Rect)
    we.blit(h23, h2t3Rect)

    # Line 3 (Wind)

    l1t1 =  weather["wlatest"]
    l1t2 =  weather["wgust"]
    l1t3 =  weather["currentwdir"]

    l11 = weafont.render(l1t1, True, weacolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(l1t3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()

    l1t1Rect.center = (tabx, datay+2*tabsp)
    l1t2Rect.center = (tabx + tabinc, datay+2*tabsp)
    l1t3Rect.center = (tabx+ 2*tabinc, datay+2*tabsp)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h31, h3t1Rect)
    we.blit(h32, h3t2Rect)
    we.blit(h33, h3t3Rect)

    # Line 4 (Rain)

    l1t1 =  weather["rfall"]
    l1t2 =  weather["rmonth"]
    l1t3 =  weather["ryear"]

    l11 = weafont.render(l1t1, True, weacolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(l1t3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()

    l1t1Rect.center = (tabx, datay+3*tabsp)
    l1t2Rect.center = (tabx + tabinc, datay+3*tabsp)
    l1t3Rect.center = (tabx+ 2*tabinc, datay+3*tabsp)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h41, h4t1Rect)
    we.blit(h42, h4t2Rect)
    we.blit(h43, h4t3Rect)

    # Line 5 (Solar)

    l1t1 =  weather["SolarRad"]
    l1t2 =  weather["UV"]
    l1t3 =  weather["SunshineHours"]

    l11 = weafont.render(l1t1, True, weacolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(l1t3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()

    l1t1Rect.center = (tabx, datay+4*tabsp)
    l1t2Rect.center = (tabx + tabinc, datay+4*tabsp)
    l1t3Rect.center = (tabx+ 2*tabinc, datay+4*tabsp)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h51, h5t1Rect)
    we.blit(h52, h5t2Rect)
    we.blit(h53, h5t3Rect)

    # Line 6 (Sunrise/set)

    l1t1 =  weather["sunrise"]
    l1t2 =  weather["sunset"]
    lit3 =  weather["LightningStrikesToday"]


    l11 = weafont.render(l1t1, True, weacolour)
    l12 = weafont.render(l1t2, True, weacolour)
    l13 = weafont.render(lit3, True, weacolour)

    l1t1Rect = l11.get_rect()
    l1t2Rect = l12.get_rect()
    l1t3Rect = l13.get_rect()


    l1t1Rect.center = (tabx, datay+5*tabsp)
    l1t2Rect.center = (tabx + tabinc, datay+5*tabsp)
    l1t3Rect.center = (tabx+ 2*tabinc, datay+5*tabsp)

    we.blit(l11, l1t1Rect)
    we.blit(l12, l1t2Rect)
    we.blit(h61, h6t1Rect)
    we.blit(h62, h6t2Rect)
    we.blit(l13, l1t3Rect)
    we.blit(h63, h6t3Rect)

    pygame.display.update()

