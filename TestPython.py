import sys, subprocess, urllib.request, json, datetime
from HelperFunctions import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QStaticText, QFont
from PyQt5.QtCore import Qt, QRect

#TODO: ANDROID APP FOR INTEGRATION/CUSTOMIZATION
    #OAUTH FOR GOOGLE CALENDAR & ETC
    #MAYBE SOME DAY HAVE CUSTOMIZATION OF DATA SHOWN
#TODO: SCHEDULE
    #HAVE BASIC CALENDAR FUNCTION
#TODO: VOICE CONTROL/TOUCH FUNCTIONS
    #DO SOME SORT OF EASY INTERACTION FEATURE
    #ANDROID APP MAY BE ABLE TO TAKE OVER THIS FUNCTIONALITY
#TODO: DAILY NEWS
    #GETSTREAM.IO FOR NEWS INTEGRATION
#TODO: GREETING? MAYBE?  FIGURE OUT THE TITLE SPOT. MAYBE CUSTOMIZED IN ANDROID APP?

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
        self.width, self.height = initDimensions()
        self.initBackground()
        self.weather = getWeather()
        self.calEvents = getCalendar()

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