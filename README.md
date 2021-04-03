# weather-station-paper-display
Raspberry Pi weather station with e-paper.

# Required hardware
## Raspberry Pi
https://www.raspberrypi.org/products/raspberry-pi-4-model-b/

## e-Paper HAT
https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT

# How to install

## 1.Run the install script under the wether-station-paper-display

```
install_epd_lib.sh
```

This script will download e-paper driver.
https://github.com/waveshare/e-Paper


## 2. Download font files
Download these fonts and place it. or just change the path in the script.
```
/usr/share/fonts/
```
* Weather icon font (https://erikflowers.github.io/weather-icons/)
* 04 Font (https://www.dafont.com/04b-03.font)

## 3. set up cron

crontab -e

```
@reboot /home/pi/weather-station/wrapper.sh
``` 


# Example

![v1](https://github.com/kotamorishi/wether-station-paper-display/raw/main/example_images/v1.jpg)



*weather
