from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Shape():
    def __init__(self, color=(0, 0, 255)):
        self.color = color

    def createCircle(self, img, cx, cy, radius):
        cv2.circle(img, (cx, cy), radius, self.color, cv2.FILLED)


class Label(QLabel):
    def __init__(self, widget=None, text=None, size=5, fontFamily="Arial", place=(0, 0), image=None):
        super(Label, self).__init__(widget)
        self.font = QFont()
        self.text = text
        self.size = size
        self.place = place
        self.fontFamily = fontFamily
        self.imagePath = image
        self.pixmap = None
        self.initLabel()

    def initLabel(self):
        self.setText(self.text)
        self.font.setPointSize(self.size)
        self.font.setFamily(self.fontFamily)
        self.setFont(self.font)
        if self.imagePath != None:
            self.pixmap = QPixmap(self.imagePath)
            self.setPixmap(self.pixmap)
            self.resize(self.pixmap.width(), self.pixmap.height())
        self.move(self.place[0], self.place[1])
