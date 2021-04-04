# -*- coding:utf-8 -*-
import sys
import os
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
picdir = 'pic'
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
libdir = '/home/pi/wether-station-paper-display/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
from PIL import Image, ImageFont, ImageDraw, ImageOps

import time
import datetime
from datetime import datetime
import subprocess
import json
import os
import sys
import math
from gpiozero import Button

# monitor sleep setting
sleepStart = 2 # Sleep starts at 2AM
sleepEnd = 7   # Sleep ends at 7AM

# sudo -H pip install --upgrade luma.oled

# 2.7 inch paper dispaly has 4 buttons, whiches are assinged GPIO 5, 6, 13, 19
def handleBtnPress():
    print("Hello, World! You can trigger whatever here.")
btn = Button(5)
btn.when_pressed = handleBtnPress

# Settings - please update following.
delay = 3
refresh_interval = 600 # refresh every 600 seconds(10 minuites)

ttf = '/usr/share/fonts/RPGSystem.ttf'
iconttf = '/usr/share/fonts/weathericons.ttf'

hello32Font = ImageFont.truetype('/usr/share/fonts/04B_03.ttf', 32)
helloFont = ImageFont.truetype('/usr/share/fonts/04B_03.ttf', 16)
hello8Font = ImageFont.truetype('/usr/share/fonts/04B_03.ttf', 8)
font32 = ImageFont.truetype(ttf, 32)
font24 = ImageFont.truetype(ttf, 24)
font16 = ImageFont.truetype(ttf, 16)

iconFontSmall = ImageFont.truetype(iconttf, 24)
iconFont = ImageFont.truetype(iconttf, 32)
iconFontMid = ImageFont.truetype(iconttf, 64)
iconFontLarge = ImageFont.truetype(iconttf, 96)

iconMap = {
    '01d':u'', # clear sky
    '01n':u'',
    '02d':u'', # few clouds
    '02n':u'',
    '03d':u'', # scattered clouds
    '03n':u'',
    '04d':u'', # broken clouds
    '04n':u'',
    '09d':u'', # shower rain
    '09n':u'',
    '10d':u'', # rain
    '10n':u'',
    '11d':u'', # thunderstorm
    '11n':u'',
    '13d':u'', # snow
    '13n':u'',
    '50d':u'', # fog
    '50n':u'',

    'clock0':u'', # same as 12
    'clock1':u'',
    'clock2':u'',
    'clock3':u'',
    'clock4':u'',
    'clock5':u'',
    'clock6':u'',
    'clock7':u'',
    'clock8':u'',
    'clock9':u'',
    'clock10':u'',
    'clock11':u'',
    'clock12':u''
}

#empty structure
class forecastInfo:
    pass


def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def internet_on():
    return True


def main():
    print("Weather station started")
    now = datetime.now()
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)
    time.sleep(1)
    
    PaperImage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(PaperImage)
    draw.text((40, 40), 'HELLO.', font=helloFont, fill = 0)
    draw.text((40, 90), 'I AM WEATHER STATION.', font=helloFont, fill = 0)
    #draw.text((10,130), u'', font=iconFont, fill=0)
    draw.text((5, 165), 'V 1.0', font=hello8Font, fill = 0)
    draw.text((110, 165), 'RETRIEVING WEATHER INFORMATION...', font=hello8Font, fill = 0)

    epd.display(epd.getbuffer(PaperImage))
    basedir = os.path.dirname(os.path.realpath(__file__))
    icondir = os.path.join(basedir, 'icons')

    time.sleep(10)

    #epd.sleep() # better to do with this.

    started_time = time.time() - refresh_interval

    while True:
        print("loop start")
        elapsed_time = time.time() - started_time

        #epd = epd2in7.EPD()
        epd.init()
        #epd.Clear(0xFF)

        # if current time is 2AM or later, dim the screen. I have no idea it will burn or not.
        now = datetime.now()
        if((now.hour >= sleepStart) and (now.hour < sleepEnd)):
            print("sleep monitor")
            epd.Clear(0xFF)
            epd.sleep() # better to do with this.
            time.sleep(600)
            continue



        PaperImage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(PaperImage)
        basedir = os.path.dirname(os.path.realpath(__file__))
        icondir = os.path.join(basedir, 'icons')

        if(elapsed_time >= refresh_interval):
            started_time = time.time()
            subprocess.check_output(os.path.join(basedir, 'download.sh'), shell=True)
            time.sleep(10)

        with open(os.path.join(basedir, 'current-data.json')) as conditions_data_file:
                conditions_data = json.load(conditions_data_file)
            
        with open(os.path.join(basedir, 'forecast-data.json')) as forecast_data_file:
            forecast_data = json.load(forecast_data_file)

        #city_name = conditions_data[u'name']
        city_name = 'Toronto'
        temp_cur = conditions_data[u'main'][u'temp']
        temp_cur_feels = conditions_data[u'main'][u'feels_like']
        icon = str(conditions_data[u'weather'][0][u'icon'])
        description = conditions_data[u'weather'][0][u'description']
        humidity = conditions_data[u'main'][u'humidity']
        epoch = int(conditions_data[u'dt'])
        utime = time.strftime('%H:%M', time.localtime(epoch))

        forecasts = []
        finfo = forecastInfo()
        finfo.time     = "Now" #city_name
        finfo.temp     = temp_cur
        finfo.humidity = humidity
        finfo.timePfx = ''
        #finfo.bmp      = logo
        finfo.icon     = icon
        finfo.description = description
        forecasts.append(finfo)

        draw.text((5, 0), now.strftime("%B %-d"), font =font32, fill = 0)
        draw.text((220, 0), now.strftime("%a"), font =font32, fill = 0)
        # 04 font
        #draw.text((10, 0), now.strftime("%B %-d").upper(), font =hello32Font, fill = 0)
        #draw.text((210, 0), now.strftime("%a").upper(), font =hello32Font, fill = 0)
        
        # temp
        draw.text((5, 35), "TEMPERATURE", font =hello8Font, fill = 0)
        draw.text((10, 42), "%2.1fc" % temp_cur, font =font32, fill = 0)
        draw.text((5, 75), "FEELS LIKE", font =hello8Font, fill = 0)
        draw.text((10, 80), "%2.1fc" % temp_cur_feels, font =font32, fill = 0)
        
        # icon
        draw.text((140, 30), iconMap[icon], font =iconFontMid, fill = 0)
        
        # weather desc
        draw.text((110, 35), description.upper(), font =hello8Font, fill = 0)

        draw.line((95, 50, 95, 100), fill = 0)
        #draw.line((0, 125, 295, 125), fill = 0)

        # forecast draw : fi = forecast index (every 3 hours)
        for fi in range(4):
            finfo = forecastInfo()
            finfo.time_dt  = forecast_data[u'list'][fi][u'dt']
            finfo.time     = time.strftime('%-I', time.localtime(finfo.time_dt))
            finfo.ampm     = time.strftime('%p', time.localtime(finfo.time_dt))
            #finfo.time     = time.strftime('%-I', time.localtime(finfo.time_dt))
            finfo.timePfx  = time.strftime('%p', time.localtime(finfo.time_dt))
            finfo.temp     = forecast_data[u'list'][fi][u'main'][u'temp']
            finfo.humidity = forecast_data[u'list'][fi][u'main'][u'humidity']
            finfo.icon     = forecast_data[u'list'][fi][u'weather'][0][u'icon'] # show the first wether condition...?
            finfo.description = forecast_data[u'list'][fi][u'weather'][0][u'description'] # show the first wether condition...?
            #finfo.bmp      = Image.open(os.path.join(icondir,  finfo.icon[0:2] + ".bmp"))
            #forecasts.append(finfo)
            columnWidth = 65
            if(fi > 0):
                draw.line(((fi * columnWidth), 145, (fi * columnWidth), 180), fill = 0)

            draw.text((3 + (fi * columnWidth), 130), finfo.time, font =helloFont, fill = 0)
            draw.text((8 + (fi * columnWidth), 145), finfo.ampm, font =hello8Font, fill = 0)
            draw.text((20 + (fi * columnWidth), 160), ("%2.1f" % finfo.temp), font=helloFont , fill = 0)
            draw.text((25 + (fi * columnWidth), 125), iconMap[finfo.icon], font =iconFontSmall, fill = 0)
            #draw.text((5 + (fi * columnWidth), 110), str(finfo.temp), font =font8, fill = 0)
            #draw.text((5 + (fi * columnWidth), 140), str(finfo.humidity) + '%', font =font8, fill = 0)
        

        #draw.text((160,8), "AS OF " + utime, font =hello8Font, fill = 0)
        epd.display(epd.getbuffer(PaperImage))
        epd.sleep() # better to do with this.
        time.sleep(600)
        
   

if __name__ == "__main__":
    main()
