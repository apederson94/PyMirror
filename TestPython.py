import sys, subprocess, urllib.request, json, datetime
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from darksky import forecast
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QStaticText, QFont
from PyQt5.QtCore import Qt, QRect

#TODO: WEATHER
    #FIGURE OUT PRECIP TYPE
#TODO: GOOGLE CALENDAR/SCHEDULE
    #HAVE BASIC CALENDAR FUNCTION
#TODO: TOUCH FUNCTIONS
    #MAYBE VOICE CONTROL INSTEAD?
#TODO: DAILY NEWS
    #GETSTREAM.IO FOR NEWS INTEGRATION
#TODO: GREETING

class App(QWidget):
 
    #initialization of QWidget object
    def __init__(self):
        super().__init__()
        self.title = 'Ashley\'s SmartMirror'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    #UI initiailization
    def initUI(self):
        self.initVars()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    #varaible initializations
    def initVars(self):
        self.initDimensions()
        self.initBackground()
        self.getWeather()
        self.getCalendar()

    #initializes background color to black
    def initBackground(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

    #initializes static text view for displaying data
    def initTextView(self):
        textView = QStaticText()
        self.text = 'TEXT'
        textView.setText(text)

    #retrieves calendar events
    def getCalendar(self):
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

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


    #retrieves weather from Dark Sky
    def getWeather(self):
        
        #DarkSky API key
        key = 'c663651149db5b56479353e7968d6db7'

        #retrieving local forecast
        homeWeather = forecast(key, 35.1983, -111.651)

        #extracting daily weather
        currentTemp = homeWeather.temperature
        daily_data = homeWeather.daily[0]
        highTemp = daily_data.temperatureMax
        lowTemp = daily_data.temperatureMin
        #precipType = daily_data.precipType
        precipChance = daily_data.precipProbability
        windSpeed = daily_data.windSpeed
        windGust = daily_data.windGust
        sunrise = daily_data.sunriseTime
        sunset = daily_data.sunsetTime

        #extracting weather alerts
        alerts = homeWeather.alerts[0]
        alertTitle = alerts.title
        alertStart = alerts.time
        alertEnd = alerts.expires

        #creating dailyWeather dictionary
        day = datetime.datetime.now()
        self.dailyWeather = {day.strftime('%a') : [currentTemp, highTemp, lowTemp, precipChance, windSpeed, windGust, sunrise, sunset]}
        
        #extracting weekly weather
        weeklyWeather = {}
        for i in range(1, 7):
            daily_data = homeWeather.daily[i]
            weeklyWeather.update({day.strftime('%a') : [daily_data.temperatureMax, daily_data.temperatureMin, daily_data.precipProbability]})
            day += datetime.timedelta(days=1)
        
        self.weeklyWeather = weeklyWeather
    
    #grabs primary screen dimensions from linux commands
    def initDimensions(self):
        cmd = ['xrandr']
        cmd2 = ['grep', '*']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout = subprocess.PIPE)
        p.stdout.close()

        resolution_string, junk = p2.communicate()
        resolution = resolution_string.split()[0].decode('utf-8')
        width, height = resolution.split('x')
        self.width, self.height = int(width), int(height)

    #paints events
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    #draws text
    def drawText(self, event, qp):

        #drawing main title
        qp.setPen(QColor(255, 255, 255))
        font = QFont('Helvetica', 20)
        font.setBold(True)
        qp.setFont(font)
        titleRect = QRect(self.width/2 - 140, 0, 280, 40)
        qp.drawText(titleRect, Qt.AlignLeft, self.title)
        
        #drawing Weather title
        font.setBold(False)
        font.setUnderline(True)
        qp.setFont(font)
        weatherRect = QRect(80, 100, 250, 500)
        qp.drawText(weatherRect, Qt.AlignLeft, 'Weather')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())