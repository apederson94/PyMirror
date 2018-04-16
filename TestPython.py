import sys, subprocess, urllib.request, json, datetime, tzlocal
from darksky import forecast
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QStaticText, QFont
from PyQt5.QtCore import Qt, QRect
 
#TODO: WEATHER
#TODO: GOOGLE CALENDAR/SCHEDULE
#TODO: TOUCH FUNCTIONS
#TODO: DAILY NEWS
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
        lowTemp = daily_data.precipType
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

        # #dates for weekly forecast
        # date_1 = datetime.date.today() + datetime.timedelta(days=1)
        # date_2 = datetime.date.today() + datetime.timedelta(days=2)
        # date_3 = datetime.date.today() + datetime.timedelta(days=3)
        # date_4 = datetime.date.today() + datetime.timedelta(days=4)
        # date_5 = datetime.date.today() + datetime.timedelta(days=5)
        # date_6 = datetime.date.today() + datetime.timedelta(days=6)

        # response = urllib.request.urlopen('https://api.darksky.net/forecast/c663651149db5b56479353e7968d6db7/35.1983,111.6513,%sT12:00:00' % date_1)
        # response = response.read().decode('utf-8')
        # json_response = json.loads(response)



        

        # #extracting 

        # self.weatherData = {
        #     "currentTemp" : currentTemp, "highTemp" : highTemp, "lowTemp" : lowTemp, 
        #     "precipType" : precipType, "precipChance" : precipChance, "windSpeed" : windSpeed,
        #     "windGust" : windGust, "sunrise" : sunrise, "sunset" : sunset,
        #     "alertTitle" : alertTitle, "alertStart" : alertStart, "alertEnd" : alertEnd
        # }



        
        
        
    
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