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

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


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
        self.initTool()

    def initTool(self):
        self.setText(self.text)
        self.font.setPointSize(self.size)
        self.font.setFamily(self.fontFamily)
        self.setFont(self.font)
        if self.imagePath != None:
            self.setStyleSheet(f"background-image : url({self.imagePath});")
            self.pixmap = QPixmap(self.imagePath)
            self.resize(self.pixmap.width(),self.pixmap.height())
        self.move(self.place[0],self.place[1])


class Label(QLabel):
    def __init__(self,widget=None,text=None,size=5,fontFamily="Arial",place=(0,0),image=None):
        super(Label,self).__init__(widget)
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
            self.resize(self.pixmap.width(),self.pixmap.height())
        self.move(self.place[0],self.place[1])



class SnapApp(QWidget):
    def __init__(self,image=None):
        super(SnapApp, self).__init__()
        self.image = image
        self.initUI()


    def place(self,start=10,width=64,height=0,gap=2,tools=[]):
        for i in tools:
            move = (start,height)
            i.move(move[0],move[1])
            start += width+gap

    def initUI(self):
        # widget properties
        self.setGeometry(700,100,700,500)
        self.setStyleSheet('background-color:#f5facd;')
        self.setWindowTitle('SnapChat Filters')

        #views
        Label(self,text="SnapChat",size=20,place=(220,50))
        Label(self,image="snapchat.png",place=(390,35))

        t1 = ToolItem(self, image="icons/mask.png")
        t2 = ToolItem(self, image="icons/patch.png")
        t3 = ToolItem(self, image="icons/with_outline.png")
        t4 = ToolItem(self, image="icons/without_outline.png")

        tools = [t1,t2,t3,t4]
        self.place(start=200,height=200,gap=10,tools=tools)




def main():
    app = QApplication(sys.argv)
    ex = SnapApp()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()

detector = HandDetector(maxHands=1, detectionCon=0.8)
handPointer = Shape()

sf = SnapFilter()
DRAW_EYE_PATCH = False
DRAW_MASK = False
OUTLINE = False

width = 1050
height = 1000

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        hand = detector.findHands(image, draw=False)
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue



        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('SnapChatFilter', cv2.flip(image, 1))

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
