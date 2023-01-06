import numpy as np
import cv2


def drawEyePatch(image, landmarks, thickness=1,color=(0,0,0),outlineColor=(0,0,0),threadColor = (0,0,0)):
    rightPatch = [70, 53, 53, 65, 55, 193, 122, 188, 114, 120, 119, 118, 117, 111, 35, 156]
    thread = [193, 285, 295, 293, 251, 251, 293, 295, 285, 193]
    coodinates = np.array(landmarks).reshape((-1, 1, 2))
    try:
        rightPatchCoodinates = np.array([coodinates[l] for l in rightPatch]).reshape(-1, 1, 2)
        threadCoodinates = np.array([coodinates[l] for l in thread]).reshape(-1, 1, 2)
        cv2.fillPoly(image, [rightPatchCoodinates], color)
        cv2.polylines(image, [rightPatchCoodinates], True, outlineColor, thickness)
        cv2.polylines(image, [threadCoodinates], True, threadColor, thickness)
    except:
        pass
    return image

def drawLips(img, coodinates, thickness=1, color=(0, 0, 255), innerLineColor=(0, 0, 0),
             outerLineColor=(0, 0, 0), alpha=0.4):
    outerLips = [57, 185, 40, 39, 37, 0, 267, 269, 270, 409, 287, 375, 321, 405, 314, 17, 84, 181, 91, 146, 57]
    outerLips = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61]
    innerLips = [62, 78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78,
                 62]
    coodinates = np.array(coodinates).reshape((-1, 1, 2))
    overlay = img.copy()
    try:
        lipsCoodinates = np.array([coodinates[l] for l in outerLips + innerLips]).reshape(-1, 1, 2)
        outerLipsCoodinates = np.array([coodinates[l] for l in outerLips]).reshape(-1, 1, 2)
        innerLipsCoodinates = np.array([coodinates[l] for l in innerLips]).reshape(-1, 1, 2)
        cv2.fillPoly(img, [lipsCoodinates], color)

        cv2.polylines(img, [outerLipsCoodinates], True, outerLineColor, thickness)
        cv2.polylines(img, [innerLipsCoodinates], True, innerLineColor, thickness)
        overlay = cv2.addWeighted(overlay, 1 - alpha, img, alpha, 0)
        return overlay
    except:
        return img

def drawEyeBrow(image,landmarks):
    path = []


def drawMask(img, landmarks, thickness=1,color=(0,0,0),outlineColor=(0,0,0)):
    path = [93, 137, 123, 50, 36, 49, 220, 45, 4, 275, 440, 279, 266, 280, 352, 323, 361, 288, 397, 365, 379, 378,
            400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]
    coodinates = np.array(landmarks).reshape((-1, 1, 2))
    try:
        maskCoodinates = np.array([coodinates[l] for l in path]).reshape(-1, 1, 2)
        cv2.fillPoly(img, [maskCoodinates],color)
        cv2.polylines(img, [maskCoodinates], True, outlineColor, thickness)
    except:
        pass
    return img



