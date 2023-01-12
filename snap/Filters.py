import numpy as np
import cv2


class EyePatch():
    def __init__(self, image, landmarks, thickness=1, color=(0, 0, 0), outlineColor=(0, 0, 0), threadColor=(0, 0, 0),
                 alpha=1):
        self.image = image
        self.landmarks = landmarks
        self.thickness = thickness
        self.color = color
        self.outlineColor = outlineColor
        self.threadColor = threadColor
        self.alpha = alpha

    def drawEyePatch(self):
        rightPatch = [70, 53, 53, 65, 55, 193, 122, 188, 114, 120, 119, 118, 117, 111, 35, 156]
        thread = [193, 285, 295, 293, 251, 251, 293, 295, 285, 193]
        coodinates = np.array(self.landmarks).reshape((-1, 1, 2))
        try:
            rightPatchCoodinates = np.array([coodinates[l] for l in rightPatch]).reshape(-1, 1, 2)
            threadCoodinates = np.array([coodinates[l] for l in thread]).reshape(-1, 1, 2)
            cv2.fillPoly(self.image, [rightPatchCoodinates], self.color)
            cv2.polylines(self.image, [rightPatchCoodinates], True, self.outlineColor, self.thickness)
            cv2.polylines(self.image, [threadCoodinates], True, self.threadColor, self.thickness)
        except:
            pass
        overlay = self.image.copy()
        overlay = cv2.addWeighted(overlay, 1 - self.alpha, self.image, self.alpha, 0)
        return overlay


# def drawEyePatch(image, landmarks, thickness=1, color=(0, 0, 0), outlineColor=(0, 0, 0), threadColor=(0, 0, 0),
#                  alpha=1):
#     rightPatch = [70, 53, 53, 65, 55, 193, 122, 188, 114, 120, 119, 118, 117, 111, 35, 156]
#     thread = [193, 285, 295, 293, 251, 251, 293, 295, 285, 193]
#     coodinates = np.array(landmarks).reshape((-1, 1, 2))
#     try:
#         rightPatchCoodinates = np.array([coodinates[l] for l in rightPatch]).reshape(-1, 1, 2)
#         threadCoodinates = np.array([coodinates[l] for l in thread]).reshape(-1, 1, 2)
#         cv2.fillPoly(image, [rightPatchCoodinates], color)
#         cv2.polylines(image, [rightPatchCoodinates], True, outlineColor, thickness)
#         cv2.polylines(image, [threadCoodinates], True, threadColor, thickness)
#     except:
#         pass
#     overlay = image.copy()
#     overlay = cv2.addWeighted(overlay, 1 - alpha, image, alpha, 0)
#     return overlay


class Lips():
    def __init__(self, image=None, landmarks=None, thickness=1, color=(0, 0, 255), innerLineColor=(0, 0, 0),
                 outerLineColor=(0, 0, 0), alpha=0.4):
        self.image = image
        self.landmarks = landmarks
        self.thickness = thickness
        self.color = color
        self.innerLineColor = innerLineColor
        self.outerLineColor = outerLineColor
        self.alpha = alpha

    # def drawLips(image, coodinates, thickness=1, color=(0, 0, 255), innerLineColor=(0, 0, 0),
    #              outerLineColor=(0, 0, 0), alpha=0.4):

    def drawLips(self):
        outerLips = [57, 185, 40, 39, 37, 0, 267, 269, 270, 409, 287, 375, 321, 405, 314, 17, 84, 181, 91, 146, 57]
        outerLips = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61]
        innerLips = [62, 78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78,
                     62]
        coodinates = np.array(self.landmarks).reshape((-1, 1, 2))
        overlay = self.image.copy()
        try:
            lipsCoodinates = np.array([coodinates[l] for l in outerLips + innerLips]).reshape(-1, 1, 2)
            outerLipsCoodinates = np.array([coodinates[l] for l in outerLips]).reshape(-1, 1, 2)
            innerLipsCoodinates = np.array([coodinates[l] for l in innerLips]).reshape(-1, 1, 2)
            cv2.fillPoly(self.image, [lipsCoodinates], self.color)

            cv2.polylines(self.image, [outerLipsCoodinates], True, self.outerLineColor, self.thickness)
            cv2.polylines(self.image, [innerLipsCoodinates], True, self.innerLineColor, self.thickness)
            overlay = cv2.addWeighted(overlay, 1 - self.alpha, self.image, self.alpha, 0)
            return overlay
        except:
            return self.image


def drawEyeLash(image, landmarks, color=(0, 0, 0), alpha=1, thickness=1):
    right = [(33, 247), (161, 30), (160, 29), (159, 27), (158, 28), (157, 56), (173, 190)]
    left = [(398, 414), (384, 286), (385, 258), (386, 257), (387, 259), (388, 260), (466, 467)]
    cood = np.array(landmarks).reshape((-1, 1, 2))
    for i, j in right:
        try:
            start = (cood[i][0][0], cood[i][0][1])
            end = (cood[j][0][0], cood[j][0][1])
            cv2.line(image, start, end, color, thickness)
        except:
            pass

    for i, j in left:
        try:
            start = (cood[i][0][0], cood[i][0][1])
            end = (cood[j][0][0], cood[j][0][1])
            cv2.line(image, start, end, color, 1)
        except:
            pass
    overlay = image.copy()
    overlay = cv2.addWeighted(overlay, 1 - alpha, image, alpha, 0)
    return overlay


def drawIris(image, landmarks, color=(255, 0, 0), alpha=1, radius=5):
    rightIris = [160, 158, 153, 144]
    leftIris = [385, 387, 373, 380]
    cood = np.array(landmarks).reshape((-1, 1, 2))
    rcx, rcy = 0, 0
    for i in rightIris:
        try:
            rcx += cood[i][0][0]
            rcy += cood[i][0][1]
        except:
            pass

    lcx, lcy = 0, 0
    for i in leftIris:
        try:
            lcx += cood[i][0][0]
            lcy += cood[i][0][1]
        except:
            pass
    overlay = image.copy()

    rcx, rcy = int(rcx / 4), int(rcy / 4)
    lcx, lcy = int(lcx / 4), int(lcy / 4)
    cv2.circle(image, (rcx, rcy), radius, color, cv2.FILLED)
    cv2.circle(image, (lcx, lcy), radius, color, cv2.FILLED)
    overlay = cv2.addWeighted(overlay, 1 - alpha, image, alpha, 0)
    return overlay


def drawSclera(image, landmarks, color=(255, 255, 255), alpha=1):
    rightPath = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7, 33]
    leftPath = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382, 362]
    coodinates = np.array(landmarks).reshape((-1, 1, 2))
    overlay = image.copy()
    try:
        sright = np.array([coodinates[l] for l in rightPath]).reshape(-1, 1, 2)
        cv2.fillPoly(image, [sright], color)
        cv2.polylines(image, [sright], True, color, 1)
    except:
        pass
    try:
        sleft = np.array([coodinates[l] for l in leftPath]).reshape(-1, 1, 2)
        cv2.fillPoly(image, [sleft], color)
        cv2.polylines(image, [sleft], True, color, 1)
    except:
        pass
    overlay = cv2.addWeighted(overlay, 1 - alpha, image, alpha, 0)
    return overlay


def drawMask(image, landmarks, thickness=1, color=(0, 0, 0), outlineColor=(0, 0, 0), alpha=1):
    path = [93, 137, 123, 50, 36, 49, 220, 45, 4, 275, 440, 279, 266, 280, 352, 323, 361, 288, 397, 365, 379, 378,
            400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]

    path = [93, 137, 123, 50, 36, 209, 198, 236, 3, 195, 248, 456, 420, 429, 266, 280, 352, 323, 361, 288, 397, 365,
            379, 378,
            400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]

    coodinates = np.array(landmarks).reshape((-1, 1, 2))
    try:
        maskCoodinates = np.array([coodinates[l] for l in path]).reshape(-1, 1, 2)
        cv2.fillPoly(image, [maskCoodinates], color)
        cv2.polylines(image, [maskCoodinates], True, outlineColor, thickness)
    except:
        pass
    overlay = image.copy()
    overlay = cv2.addWeighted(overlay, 1 - alpha, image, alpha, 0)
    return overlay
