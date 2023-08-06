import cv2
from cv2 import aruco
import math

class ArucoDetctor:
    def __init__(self, type = aruco.DICT_ARUCO_ORIGINAL):
        self.arucoDict = aruco.getPredefinedDictionary(type)
        self.parameters = aruco.DetectorParameters_create()

    def __call__(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.arucoDict, parameters=self.parameters)

        if ids is None:
            return None, None

        return corners, ids

    def GetAngle(self, coner) -> float:
        centerX = int((coner[0][0] + coner[2][0]) * 0.5)
        centerY = int((coner[0][1] + coner[2][1]) * 0.5)

        rad = math.atan2(centerY - coner[0][1], centerX - coner[0][0])
        dir = (rad * 180) / math.pi
        dir -= 45
        if dir < -180:
            dir += 360

        return dir