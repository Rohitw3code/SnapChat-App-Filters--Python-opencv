# filter import
from snap import Filters as flt
from snap.Filters import *
from snap.ToolItem import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils.widgets import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


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


class SnapApp(QWidget):
    def __init__(self, image=None, landmarks=None):
        super(SnapApp, self).__init__()
        self.image = image
        self.landmarks = landmarks
        self.results = {}
        self.tools = list("aa")
        self.initUI()

    def place(self, start=10, width=64, height=0, gap=2):
        for i in self.tools:
            move = (start, height)
            i.move(move[0], move[1])
            start += width + gap

    def load(self):
        for t in self.tools:
            self.results[t.text] = t.call

    def initUI(self):
        # widget properties
        self.setGeometry(700, 100, 1000, 500)
        self.setStyleSheet('background-color:#f5facd;')
        self.setWindowTitle('SnapChat Filters')

        # views
        Label(self, text="SnapChat", size=20, place=(200, 50))
        Label(self, image="icons/snapchat.png", place=(410, 35))

        t1 = ToolItem(self, image="icons/mask.png", text='mask')
        t2 = ToolItem(self, image="icons/patch.png", text='eye_patch')
        t3 = ToolItem(self, image="icons/lips.png", text='lips')
        t4 = ToolItem(self, image="icons/eyelashes.png", text='eye_lash')
        t5 = ToolItem(self, image="icons/iris.png", text='iris')
        t6 = ToolItem(self, image="icons/sclera.png", text='sclera')

        # Filter tool
        Label(self, text="Filter Tool", size=18, place=(550, 70))

        self.spin = QSpinBox(self)
        self.spin.setGeometry(550, 150, 80, 40)
        self.spin.setRange(0, 9)
        self.spin.setPrefix("Alpha ")
        self.spin.setSizeIncrement(10, 10)

        self.tools = [t1, t2, t3, t4, t5, t6]
        self.place(start=50, height=200, gap=10)


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

lips = Lips()

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
            # image = flt.drawLips(image=image, coodinates=landmarks, alpha=0.2, color=lipscolor, innerLineColor=lipscolor,
            #                      outerLineColor=lipscolor)
            lips.image = image
            lips.landmarks = landmarks
            lips.color = lipscolor
            image = lips.drawLips()
        if snap.results['sclera']:
            image = flt.drawSclera(image, landmarks, alpha=0.5, color=(0, 0, 255))
        if snap.results['mask']:
            image = flt.drawMask(image=image, landmarks=landmarks)
        if snap.results['eye_lash']:
            image = flt.drawEyeLash(image=image, landmarks=landmarks)
        if snap.results['iris']:
            image = flt.drawIris(image, landmarks, alpha=1, color=(238, 169, 126))
        if snap.results['eye_patch']:
            pass
            # image = flt.drawEyePatch(image=image, landmarks=landmarks,alpha=0.5)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('SnapChatFilter', cv2.flip(image, 1))

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
app.exec_()
