#
# Change id for your location
# Toronto : 6167865
# Tokyo : 1850147
# Osaka : 1853909
#
# Change appid - get it from https://openweathermap.org 
#
API_KEY="please update your API key here!!"
WEATHER_ID=6091104


SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
wget -O ${SCRIPTPATH}/current-data.json "http://api.openweathermap.org/data/2.5/weather?id=$WEATHER_ID&&units=metric&appid=$API_KEY"
wget -O ${SCRIPTPATH}/forecast-data.json "http://api.openweathermap.org/data/2.5/forecast?id=$WEATHER_ID&units=metric&appid=$API_KEY"
