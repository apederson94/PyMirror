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
        self.title = 'PyMirror'
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
        self.titleSize = self.width/64
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
        font = QFont('Helvetica', self.titleSize)
        font.setBold(True)
        titleDims = getStringDims(self.title, font)
        qp.setFont(font)
        titleRect = QRect((self.width/2) - (titleDims.width()/2), 0, titleDims.width(), titleDims.height())
        qp.drawText(titleRect, Qt.AlignLeft, self.title)
        
        #drawing Weather title
        font.setBold(False)
        font.setUnderline(True)
        titleDims = getStringDims(self.title, font)
        qp.setFont(font)
        weatherX = self.width/12
        weatherY = self.height/12
        weatherRect = QRect(weatherX, weatherY, titleDims.width(), titleDims.height())
        qp.drawText(weatherRect, Qt.AlignLeft, 'Weather')

        #setting up weather vars
        dailyWeather = self.weather[0]
        weeklyWeather = self.weather[1]
        font.setUnderline(False)
        font.setPointSize(self.titleSize/1.25)
        qp.setFont(font)
        weatherX = weatherX - self.width/24
        yoffset = self.height/24

        for event in dailyWeather:
            textDims = getStringDims(event, font)
            drawRect = QRect(weatherX, weatherY+yoffset, textDims.width(), textDims.height())
            qp.drawText(drawRect, Qt.AlignLeft, event)
            yoffset = yoffset + textDims.height()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())