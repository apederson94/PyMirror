import sys, subprocess, urllib.request, json, datetime
from oauth2client import file, client, tools
from darksky import forecast
from apiclient.discovery import build
from httplib2 import Http
from PyQt5.QtGui import QFont, QFontMetrics

#retrieves calendar events
def getCalendar():
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


#retrieves weather from Dark Sky
def getWeather():
    
    #DarkSky API key
    key = 'c663651149db5b56479353e7968d6db7'

    #retrieving local forecast
    homeWeather = forecast(key, 35.1983, -111.651)

    #extracting daily weather
    currentTemp = str(homeWeather.temperature) + "°"
    daily_data = homeWeather.daily[0]
    highTemp = str(daily_data.temperatureMax) + "°"
    lowTemp = str(daily_data.temperatureMin) + "°"
    windSpeed = str(daily_data.windSpeed) + " mph"
    windGust = str(daily_data.windGust) + " mph"
    sunrise = datetime.datetime.fromtimestamp(daily_data.sunriseTime).strftime('%I:%M') + " AM"
    sunset = datetime.datetime.fromtimestamp(daily_data.sunsetTime).strftime('%I:%M') + " PM"
    precipChance = str(daily_data.precipProbability) + "%"
    try:
        precipType = daily_data.precipType
    except:
        precipType = -1
        print('no precip type found')

    #extracting weather alerts
    try:
        alerts = homeWeather.alerts[0]
        alertTitle = alerts.title
        alertStart = alerts.time
        alertEnd = alerts.expires
    except:
        print('no alerts found')
        alertTitle = -1
        alertStart = -1
        alertEnd = -1
        
    #creating dailyWeather list
    day = datetime.datetime.now()
    dailyWeather = [currentTemp, highTemp, lowTemp, precipChance, precipType, windSpeed, windGust, sunrise, sunset]
    
    #extracting weekly weather
    weeklyWeather = []
    for i in range(1, 7):
        daily_data = homeWeather.daily[i]
        weeklyWeather.append([daily_data.temperatureMax, daily_data.temperatureMin, daily_data.precipProbability])
        day += datetime.timedelta(days=1)

    return [dailyWeather, weeklyWeather]

#grabs primary screen dimensions from linux commands
def initDimensions():
    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout = subprocess.PIPE)
    p.stdout.close()

    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0].decode('utf-8')
    width, height = resolution.split('x')
    width, height = int(width), int(height)
    return width, height

def getStringDims(text, font):
    metrics = QFontMetrics(font)
    return metrics.boundingRect(text)
