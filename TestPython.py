import sys, subprocess, urllib.request, json
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
        response = urllib.request.urlopen('https://api.darksky.net/forecast/c663651149db5b56479353e7968d6db7/42.3601,-71.0589')
        response = response.read().decode('utf-8')
        dictionary = dict()
        for i in range(0, len(response) - 1):
            dictionary.update({str(response[i]) : response[i+1]})
        print(dictionary)
        
    
    #grabs primary screen dimensions from linux commands
    def initDimensions(self):
        cmd = ['xrandr']
        cmd2 = ['grep', '*']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout = subprocess.PIPE)
        p.stdout.close()

        resolution_string, junk = p2.communicate()
        resolution = resolution_string.split()[0]
        resolution = str(resolution)
        width, height = resolution.split('x')
        self.width = int(width[2:])
        self.height = int(height[:len(height)-1])

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