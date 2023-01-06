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
# filter import
import Filters as flt
from ToolItem import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

class Shape():
    def __init__(self, color=(0, 0, 255)):
        self.color = color

    def createCircle(self, img, cx, cy, radius):
        cv2.circle(img, (cx, cy), radius, self.color, cv2.FILLED)

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
    def __init__(self,image=None,landmarks=None):
        super(SnapApp, self).__init__()
        self.image = image
        self.landmarks = landmarks
        self.results = {}
        self.tools = list("aa")
        self.initUI()



    def place(self,start=10,width=64,height=0,gap=2):
        for i in self.tools:
            move = (start,height)
            i.move(move[0],move[1])
            start += width+gap

    def load(self):
        for t in self.tools:
            self.results[t.text] = t.call


    def initUI(self):
        # widget properties
        self.setGeometry(700,100,700,500)
        self.setStyleSheet('background-color:#f5facd;')
        self.setWindowTitle('SnapChat Filters')

        #views
        Label(self,text="SnapChat",size=20,place=(220,50))
        Label(self,image="snapchat.png",place=(390,35))

        t1 = ToolItem(self, image="icons/mask.png",text='mask')
        t2 = ToolItem(self, image="icons/patch.png",text='eyepatch')
        t3 = ToolItem(self, image="icons/lips.png",text='lips')
        # t4 = ToolItem(self, image="icons/with_outline.png")
        # t5 = ToolItem(self, image="icons/without_outline.png")

        self.tools = [t1,t2,t3]
        self.place(start=230,height=200,gap=10)








detector = HandDetector(maxHands=1, detectionCon=0.8)
# handPointer = Shape()

width = 1050
height = 1000
# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

app = QApplication(sys.argv)
snap = SnapApp()
snap.show()


with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        # hand = detector.findHands(image, draw=False)
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        landmarks = []
        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                for landmark in face.landmark:
                    x = landmark.x
                    y = landmark.y

                    shape = image.shape
                    relative_x = int(x * shape[1])
                    relative_y = int(y * shape[0])

                    landmarks.append([relative_x, relative_y])

        snap.load()
        snap.image = image
        snap.landmarks = landmarks

        if snap.results['lips']:
            lipscolor = (0, 0, 255)
            image = flt.drawLips(image, coodinates=landmarks, alpha=0.2, color=lipscolor, innerLineColor=lipscolor,
                                 outerLineColor=lipscolor)
        if snap.results['mask']:
            image = flt.drawMask(img=image,landmarks=landmarks)
        if snap.results['eyepatch']:
            image = flt.drawEyePatch(image=image,landmarks=landmarks)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('SnapChatFilter', cv2.flip(image, 1))

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
app.exec_()
