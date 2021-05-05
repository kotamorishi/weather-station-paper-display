# weather-station-paper-display
Raspberry Pi weather station with e-paper.

![v1](https://github.com/kotamorishi/weather-station-paper-display/raw/main/example_images/v1.jpg)

# Required hardware
## Raspberry Pi
https://www.raspberrypi.org/products/raspberry-pi-4-model-b/

## e-Paper HAT
https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT

# How to install

## 1.Enable SPI interface on your Raspberry Pi.
```
sudo raspi-config
```
- 3 Interface Options
- P4 SPI (Enable it)

## 2.Download and prepare to use.
```
git clone https://github.com/kotamorishi/weather-station-paper-display
```



## 3.Run the install script under the weather-station-paper-display

```
install_epd_lib.sh
```

This script will download e-paper driver.
https://github.com/waveshare/e-Paper


## 4. Download font files
Download follwing fonts and place it. or just change the path in the script.
```
/usr/share/fonts/
```
* Weather icon font (https://erikflowers.github.io/weather-icons/)
* 04 Font (https://www.dafont.com/04b-03.font)
* RPG system font (https://www.dafont.com/rpgsystem.font)

Unzip and place it.(required sudo permission)
```
'/usr/share/fonts/RPGSystem.ttf'
'/usr/share/fonts/weathericons.ttf'
'/usr/share/fonts/04B_03.ttf'
```
## 5.Update your API Key and weather ID

Sign up for OpenWeatherMap and generate key from here

https://home.openweathermap.org/api_keys


Once you've got an API Key, copy and paste it in the download.sh
```
API_KEY="TYPE_YOUR_API_KEY_HERE"
WEATHER_ID=6167865
```

Don't forget to update WEATHER_ID too. 

## 6. set up cron

crontab -e

```
@reboot /home/pi/weather-station/wrapping-paper.sh
``` 



