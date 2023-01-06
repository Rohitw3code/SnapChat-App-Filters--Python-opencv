import math
import random as rd
import cv2
import mediapipe as mp
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

class ToolItem(QPushButton):
    def __init__(self,widget=None,text=None,size=5,fontFamily="Arial",place=(0,0),image=None):
        super(ToolItem,self).__init__(widget)
        self.font = QFont()
        self.text = text
        self.size = size
        self.place = place
        self.fontFamily = fontFamily
        self.imagePath = image
        self.pixmap = None
        self.call = False
        self.initTool()
    def functionCall(self):
        if self.call:
            self.call = False
        else:
            self.call = True

    def initTool(self):
        # self.setText(self.text)
        self.font.setPointSize(self.size)
        self.font.setFamily(self.fontFamily)
        self.setFont(self.font)
        if self.imagePath != None:
            self.setStyleSheet(f"background-image : url({self.imagePath});")
            self.pixmap = QPixmap(self.imagePath)
            self.resize(self.pixmap.width(),self.pixmap.height())
        self.move(self.place[0],self.place[1])
        self.clicked.connect(lambda :self.functionCall())
