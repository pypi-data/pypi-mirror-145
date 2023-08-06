from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from inspect import signature
from logging import exception
from types import coroutine

import cv2
from cv2 import aruco
import time
import os
import threading
import enum
import pkg_resources

import urllib
import numpy as np

import os.path

from RoboCam.face_detector import FaceDetector
from RoboCam.face_landmark import FaceLandmark
from RoboCam.face_recognizer import FaceRecognizer
from RoboCam.aruco_detector import ArucoDetctor
from RoboCam.sketch_recognizer import SketchRecognizer
from RoboCam.number_recognizer import NumberRecognizer
from tensorflow.python.eager.execute import convert_to_mixed_eager_tensors
class CameraEvents(enum.Enum):
    RECV_DETECTED_FACE_COUNT = 1
    RECV_DETECTED_FACE_NAME = 2
    RECV_DETECTED_FACE_RECT = 3
    RECV_LEFT_IRIS_POINT = 4
    RECV_LEFT_EYEBROW_POINT = 5
    RECV_RIGHT_IRIS_POINT = 5
    RECV_RIGHT_EYEBROW_POINT = 6
    RECV_NOSE_POINT = 7
    RECV_MOUSE_POINT = 8
    RECV_JAW_POINT = 9
    RECV_ARUCO_ID = 10
    RECV_ARUCO_IDS = 11
    RECV_ARUCO_CENTER_POINTS = 12
    RECV_ARUCO_RECT_POINTS = 13
    RECV_ARUCO_ANGLE = 14
    RECV_SKETCH_NAME = 15
    RECV_NUMBERS = 16

class RoboCam():
    def __init__(self):
        self.streamFlag = False
        self.streamInitFlag = False
        self.eventHandlerDic = {}
        self.stream = None
        self.isConnected = False

        self.mosaicFlag = False
        self.mosaicRate = 0

        self.rotateFlag = False
        self.rotateAngle = 0

        self.flipLRFlag = False
        self.flipUDFlag = False
        self.raw_img = None

        # face detector
        self.faceDetectFlag = False
        self.drawFaceAreaFlag = True
        self.drawLandmarkFlag = True

        self.faceDetectInitFlag = False
        self.faceDetectedList = []
        self.prevFaceDetectedList = []

        self.faceLandmarkInitFlag = False
        self.faceLandmarkList = []
        self.prevFaceLandmarkList = []

        self.faceRecognizeInitFlag = False
        self.faceRecognizedList = []
        self.prevFaceRecognizedList = []

        self.RegisterdColor = (0,0,255)
        self.UnregisterdColor = (255,0,0)

        # aruco detector
        self.arucoDetectFlag = False
        self.arucoDetectInitFlag = False
        self.drawArucoFlag = True
        self.drawArucoIdFlag = True

        self.arucoDetectedCorners = []
        self.prevArucoDetectedCorners = []

        self.arucoDetectedIds = []
        self.prevArucoDetectedIds = []

        # sketch detector
        self.sketchDetectFlag = False
        self.sketchDetectInitFlag = False
        self.drawSketchFlag = True

        self.sketchRecognizedList = []
        self.prevSketchRecognizedList = []

        self.sketchDetectedList = []
        self.prevSketchDetectedList = []

        # number recognizer
        self.numberDetectInitFlag = False
        self.numberDetectFlag = False
        self.drawNumberFlag = True

        self.numberRecognizedStr = ''
        self.numberDetectedList = []
        self.prevNumberDetectedList = []

        print("camera module ready")

    def SetEventHandler(self, event:CameraEvents, func):
        if event in self.eventHandlerDic:
            print("Event ", event, " already exist lisntener")
        else:
            self.eventHandlerDic[event] = func

    def RemoveEventHandler(self, event:CameraEvents):
        if event in self.eventHandlerDic:
            del self.eventHandlerDic[event]
            print("Event ", event, " is removed")
        else:
            print("Event ", event, " not exist lisntener")
        
    def CameraStreamInit(self, width:int = 512, height:int = 512):
        if self.CameraStreamInit is True:
            print("Camera stream is aready initialized.")
            return

        url = 'http://192.168.4.1:81/stream'
           
        while True:
            try:
                self.stream = urllib.request.urlopen(url)
                self.isConnected = True
                break
            except:
                time.sleep(0.5)
                print('no cam yet')
                continue

        self.camWidth = width
        self.camHeight = height

        self.CameraStreamInit = True
        print("camera stream ready")

        dataSenderTH = threading.Thread(target=self.__dataSender)
        dataSenderTH.daemon = True
        dataSenderTH.start()
        time.sleep(0.1)

        print("camera event module ready")
        
    def LeftRightFlipMode(self, flag:bool):
        self.flipLRFlag = flag
    
    def UpDownFlipMode(self, flag:bool):
        self.flipUDFlag = flag
        
    def MosaicMode(self, rate:int = 0):
        self.mosaicRate = rate

        if self.mosaicRate == 0:
            self.mosaicFlag = False
        else:
            self.mosaicFlag = True

    def RotateMode(self, angle:int = 90):
        self.rotateAngle += int(angle)

        if self.rotateAngle % 360 == 0:
            self.rotateFlag = False
        else:
            self.rotateFlag = True

    def DrawFaceArea(self, flag:bool):
        self.drawFaceAreaFlag = flag

    def DrawFaceLandmark(self, flag:bool):
        self.drawLandmarkFlag = flag

    def DrawArucoArea(self, flag:bool):
        self.drawArucoFlag = flag

    def DrawArucoId(self, flag:bool):
        self.drawArucoIdFlag = flag

    def DrawSketchArea(self, flag:bool):
        self.drawSketchFlag = flag

    def DrawNumberArea(self, flag:bool):
        self.drawNumberFlag = flag

    def CameraStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__cameraStreamTh)
        th.deamon = True
        th.start()

    def __cameraStreamTh(self):
        bytes = b''
        org = (20,20)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = None
        while self.streamFlag:

            try:
                bytes += self.stream.read(64)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes = bytes[b+2:]
                    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    frame = cv2.resize(frame, (self.camWidth, self.camHeight))

                    if self.flipLRFlag == True:
                        frame = cv2.flip(frame, 1)

                    if self.flipUDFlag == True:
                        frame = cv2.flip(frame, 0)

                    if self.mosaicFlag == True:
                        frame = cv2.resize(frame, (self.camWidth//self.mosaicRate, self.camHeight//self.mosaicRate))
                        frame = cv2.resize(frame, (self.camWidth, self.camHeight))

                    if self.rotateFlag == True:
                        m1 = cv2.getRotationMatrix2D((self.camWidth/2, self.camHeight/2), self.rotateAngle, 1)
                        frame = cv2.warpAffine(frame, m1, (self.camWidth, self.camHeight))

                    self.raw_img = frame.copy()

                    if self.faceDetectFlag == True:
                        if self.drawFaceAreaFlag:
                            self.__overlay_bounding_boxes(frame)
                        if self.drawLandmarkFlag:
                            self.__overlay_landmark_shapes(frame)
                    
                    if self.arucoDetectFlag == True:
                        if self.drawArucoFlag == True:
                            self.__overlay_aruco_boxes(frame)
                    
                    if self.sketchDetectFlag == True:
                        if self.drawSketchFlag == True:
                            self.__overlay_sketch_boxes(frame)
    
                    if self.numberDetectFlag == True:
                        if self.drawNumberFlag == True:
                            self.__overlay_number_boxes(frame)

                    cv2.imshow('i', frame)
                    cv2.waitKey(1)
            except Exception as e:
                print("STREAM : " , e)
                continue
        print ("Stream stopped")

    def __overlay_bounding_boxes(self, frame):
        color = self.UnregisterdColor
        if np.any(self.faceDetectedList) == False:
            if np.any(self.prevFaceDetectedList) == False:
                return
            else:
                cnt = 0
                for detected in self.prevFaceDetectedList:
                    if self.GetFaceName(cnt) == 'Human':
                        color = self.UnregisterdColor
                    else:
                        color = self.RegisterdColor
                    cv2.rectangle(frame, (int(detected[0]), int(detected[1])), (int(detected[2]), int(detected[3])), color, 3)
                    cnt += 1
        else:
            cnt = 0
            for detected in self.faceDetectedList:
                if self.GetFaceName(cnt) == 'Human':
                    color = self.UnregisterdColor
                else:
                    color = self.RegisterdColor
                cv2.rectangle(frame, (int(detected[0]), int(detected[1])), (int(detected[2]), int(detected[3])), color, 3)
            self.faceDetectedList = []

    def __overlay_landmark_shapes(self, frame):
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) == False:
                return
            else:
                faceIdx = 0
                for faces in self.prevFaceLandmarkList:
                    pointIdx = 0
                    for point in faces:
                        cv2.circle(frame, (int(point[0]),int(point[1])), 3, (255,0,255), -1)

                        if pointIdx != 0 and pointIdx != 17 and pointIdx != 22 and pointIdx != 27 and pointIdx != 36 and pointIdx != 42 and pointIdx != 48 and pointIdx != 60:
                            cv2.line(frame, (self.prevFaceLandmarkList[faceIdx][pointIdx][0], self.prevFaceLandmarkList[faceIdx][pointIdx][1]), (self.prevFaceLandmarkList[faceIdx][pointIdx-1][0], self.prevFaceLandmarkList[faceIdx][pointIdx-1][1]), (255,255,0), 1)
                        pointIdx += 1
                    cv2.line(frame, (self.prevFaceLandmarkList[faceIdx][41][0], self.prevFaceLandmarkList[faceIdx][41][1]), (self.prevFaceLandmarkList[faceIdx][36][0], self.prevFaceLandmarkList[faceIdx][36][1]), (255,255,0), 1)
                    cv2.line(frame, (self.prevFaceLandmarkList[faceIdx][47][0], self.prevFaceLandmarkList[faceIdx][47][1]), (self.prevFaceLandmarkList[faceIdx][42][0], self.prevFaceLandmarkList[faceIdx][42][1]), (255,255,0), 1)
                    cv2.line(frame, (self.prevFaceLandmarkList[faceIdx][59][0], self.prevFaceLandmarkList[faceIdx][59][1]), (self.prevFaceLandmarkList[faceIdx][48][0], self.prevFaceLandmarkList[faceIdx][48][1]), (255,255,0), 1)
                    cv2.line(frame, (self.prevFaceLandmarkList[faceIdx][67][0], self.prevFaceLandmarkList[faceIdx][67][1]), (self.prevFaceLandmarkList[faceIdx][60][0], self.prevFaceLandmarkList[faceIdx][60][1]), (255,255,0), 1)
                    faceIdx += 1
        else:
            faceIdx = 0
            for faces in self.faceLandmarkList:
                pointIdx = 0
                for point in faces:
                    cv2.circle(frame, (int(point[0]),int(point[1])), 3, (255,0,255), -1)

                    if pointIdx != 0 and pointIdx != 17 and pointIdx != 22 and pointIdx != 27 and pointIdx != 36 and pointIdx != 42 and pointIdx != 48 and pointIdx != 60:
                        cv2.line(frame, (self.faceLandmarkList[faceIdx][pointIdx][0], self.faceLandmarkList[faceIdx][pointIdx][1]), (self.faceLandmarkList[faceIdx][pointIdx-1][0], self.faceLandmarkList[faceIdx][pointIdx-1][1]), (255,255,0), 1)
                    pointIdx += 1
                cv2.line(frame, (self.faceLandmarkList[faceIdx][41][0], self.faceLandmarkList[faceIdx][41][1]), (self.faceLandmarkList[faceIdx][36][0], self.faceLandmarkList[faceIdx][36][1]), (255,255,0), 1)
                cv2.line(frame, (self.faceLandmarkList[faceIdx][47][0], self.faceLandmarkList[faceIdx][47][1]), (self.faceLandmarkList[faceIdx][42][0], self.faceLandmarkList[faceIdx][42][1]), (255,255,0), 1)
                cv2.line(frame, (self.faceLandmarkList[faceIdx][59][0], self.faceLandmarkList[faceIdx][59][1]), (self.faceLandmarkList[faceIdx][48][0], self.faceLandmarkList[faceIdx][48][1]), (255,255,0), 1)
                cv2.line(frame, (self.faceLandmarkList[faceIdx][67][0], self.faceLandmarkList[faceIdx][67][1]), (self.faceLandmarkList[faceIdx][60][0], self.faceLandmarkList[faceIdx][60][1]), (255,255,0), 1)
                faceIdx += 1
            self.faceLandmarkList = []
    
    def __overlay_aruco_boxes(self,frame):
        duplicateId = []
        color = self.RegisterdColor
        if self.arucoDetectedIds is None:
            if self.prevArucoDetectedIds is None:
                return
            else:
                idx = 0
                for corners in self.prevArucoDetectedCorners:
                    id = self.prevArucoDetectedIds[idx]
                    if id in duplicateId:
                        color = self.UnregisterdColor
                    else:
                        color = self.RegisterdColor
                        duplicateId.append(id)
                    
                    cv2.polylines(frame, np.array([corners[0]], np.int32), True, color, 3)

                    x = int((corners[0][0][0] + corners[0][2][0]) / 2)
                    y = int((corners[0][0][1] + corners[0][2][1]) / 2)

                    if self.drawArucoIdFlag == True:
                        s = 'id='+str(id)
                        cv2.putText(frame, s, (x,y), cv2.FONT_HERSHEY_COMPLEX,1, (0,255,0), 1)

                    idx += 1
        else:
            idx = 0
            for corners in self.arucoDetectedCorners:
                id = self.arucoDetectedIds[idx]

                if id in duplicateId:
                    color = self.UnregisterdColor
                else:
                    color =self.RegisterdColor
                    duplicateId.append(id)
                
                cv2.polylines(frame, np.array([corners[0]], np.int32), True, color, 3)

                x = int((corners[0][0][0] + corners[0][2][0]) / 2)
                y = int((corners[0][0][1] + corners[0][2][1]) / 2)

                if self.drawArucoIdFlag == True:
                    s = 'id='+str(id)
                    cv2.putText(frame, s, (x,y), cv2.FONT_HERSHEY_COMPLEX,1, (0,255,0), 1)
                idx+=1
                
        
        self.arucoDetectedCorners = []
        self.arucoDetectedIds = []

    def __overlay_sketch_boxes(self, frame):
        color = self.UnregisterdColor
        if np.any(self.sketchDetectedList) == False:
            if np.any(self.prevFaceDetectedList) == False:
                return
            else:
                cnt = 0
                for detected in self.prevSketchDetectedList:
                    if self.GetSketchName(cnt) == 'Sketch':
                        color = self.UnregisterdColor
                    else:
                        color = self.RegisterdColor

                    cv2.line(frame, (detected[0][0], detected[0][1]), (detected[1][0],detected[1][1]), color, 3)
                    cv2.line(frame, (detected[1][0], detected[1][1]), (detected[2][0],detected[2][1]), color, 3)
                    cv2.line(frame, (detected[2][0], detected[2][1]), (detected[3][0],detected[3][1]), color, 3)
                    cv2.line(frame, (detected[3][0], detected[3][1]), (detected[0][0],detected[0][1]), color, 3)
        else:
            cnt = 0
            for detected in self.sketchDetectedList:
                if self.GetSketchName(cnt) == 'Sketch':
                    color = self.UnregisterdColor
                else:
                    color = self.RegisterdColor

                cv2.line(frame, (detected[0][0], detected[0][1]), (detected[1][0],detected[1][1]), color, 3)
                cv2.line(frame, (detected[1][0], detected[1][1]), (detected[2][0],detected[2][1]), color, 3)
                cv2.line(frame, (detected[2][0], detected[2][1]), (detected[3][0],detected[3][1]), color, 3)
                cv2.line(frame, (detected[3][0], detected[3][1]), (detected[0][0],detected[0][1]), color, 3)
            self.sketchDetectedList = []

    def __overlay_number_boxes(self, frame):
        color = self.UnregisterdColor
        if np.any(self.numberDetectedList) == False:
            if np.any(self.prevNumberDetectedList) == False:
                return
            else:
                for detected in self.prevNumberDetectedList:
                    cv2.line(frame, (detected[0][0], detected[0][1]), (detected[1][0],detected[1][1]), color, 3)
                    cv2.line(frame, (detected[1][0], detected[1][1]), (detected[2][0],detected[2][1]), color, 3)
                    cv2.line(frame, (detected[2][0], detected[2][1]), (detected[3][0],detected[3][1]), color, 3)
                    cv2.line(frame, (detected[3][0], detected[3][1]), (detected[0][0],detected[0][1]), color, 3)
        else:
            for detected in self.numberDetectedList:
                cv2.line(frame, (detected[0][0], detected[0][1]), (detected[1][0],detected[1][1]), color, 3)
                cv2.line(frame, (detected[1][0], detected[1][1]), (detected[2][0],detected[2][1]), color, 3)
                cv2.line(frame, (detected[2][0], detected[2][1]), (detected[3][0],detected[3][1]), color, 3)
                cv2.line(frame, (detected[3][0], detected[3][1]), (detected[0][0],detected[0][1]), color, 3)
            self.numberDetectedList = []

    def CameraStreamOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return

        if self.faceDetectFlag:
            self.faceDetectFlag = False
            print("Facedetector Off")

        self.streamFlag = False
        self.cam.release()
        time.sleep(1)

        print("Camera off")
    
    def FacedetectorInit(self):
        if self.faceDetectInitFlag is False:
            self.faceD = FaceDetector()
            self.faceDetectInitFlag = True
        
        if self.faceLandmarkInitFlag is False:
            self.landD = FaceLandmark()
            self.faceLandmarkInitFlag = True
        
        if self.faceRecognizeInitFlag is False:
            self.faceR = FaceRecognizer()
            self.faceRecognizeInitFlag = True

        print("Facedetector initialized")
    
    def FacedetectorStart(self):

        if self.faceDetectInitFlag is False:
            print("Facedetector is not initialized")
            return

        if self.faceDetectFlag == True:
            print("Facedetector is already working.")
            return
        self.faceDetectFlag = True

        th = threading.Thread(target=self.__facedetect)
        th.deamon = True
        th.start()

    def __facedetect(self):
        while self.faceDetectFlag:
            if self.raw_img is None:
                time.sleep(0.1)
                print('no input frame yet')
                continue
            try:
                self.faceDetectedList = self.faceD(self.raw_img)
                self.prevFaceDetectedList = self.faceDetectedList.copy()
                if np.any(self.faceDetectedList) == False:
                    self.faceLandmarkList = []
                    self.prevFaceLandmarkList = []

                    self.faceRecognizedList = []
                    self.prevFaceRecognizedList = []
                    continue

                self.faceLandmarkList = self.landD.batch_call (self.raw_img, self.faceDetectedList.copy())
                self.prevFaceLandmarkList = self.faceLandmarkList.copy()

                self.faceRecognizedList = self.faceR(self.raw_img, self.faceDetectedList.copy())
                self.prevFaceRecognizedList = self.faceRecognizedList.copy()
            except Exception as e:
                print("Detect : " , e)
                continue
            
            time.sleep(0.05)

    def FacedetectorStop(self):
        if self.faceDetectFlag == False :
            print("Facedetector is already stopped.")
            return

        self.faceDetectFlag = False
        time.sleep(1)

        print("Facedetector off")
        
    def FaceCapture(self, name:str, path:str=pkg_resources.resource_filename(__package__,"res/face/")):
        if bool(name) == False:
            print("Name parameter is Empty.")
            return

        if os.path.isdir(path) is False:
            os.mkdir(path)

        if self.faceDetectFlag is False:
            print("Facedetector did not run")
            return

        while True:
            if np.any(self.faceDetectedList) == False:
                print("Doesn't have a any face in Frame")
                continue
            
            bbox = (0,self.faceDetectedList.copy()[0])
            result = self.faceR.SaveFace(self.raw_img,bbox,name)
            if result == 0:
                print(name + " is saved")
                break

    def TrainFaceData(self, facePath:str =pkg_resources.resource_filename(__package__,"res/face/")):
        if os.path.isdir(facePath) is False:
            print(facePath +" is not directory.")
            return

        faceD = FaceDetector()
        self.faceR.registerd.clear()

        filenames = os.listdir(facePath)
        for filename in filenames:
            name = os.path.basename(filename)
            image = cv2.imread(facePath + filename, cv2.IMREAD_ANYCOLOR)
            facedetectedList = faceD(image)

            if np.any(facedetectedList) == False:
                print("Doesn't have a any face in Frame")
                continue
            
            name = name.split('_')[0]
            bbox = (0, facedetectedList[0])
            self.faceR.TrainModel(image, bbox, name)

    def DeleteFaceData(self, name:str, facePath:str='.res/face/'):
        if os.path.isdir(facePath) is False:
            print(facePath +" is not directory.")
            return

        self.faceR.RemoveFace(name, facePath)

        print(name + 'is deleted')

    def GetFaceCount(self) -> int:        
        if np.any(self.faceDetectedList) == False:
            if np.any(self.prevFaceDetectedList) == False:
                return 0
            else:
                return self.prevFaceDetectedList.size()
        else:
            return self.faceDetectedList.size()

    def GetFaceRects(self) -> np.ndarray:
        if np.any(self.faceDetectedList) == False:
            if np.any(self.prevFaceDetectedList) == False:
                return np.ndarray([])
            else:
                return self.prevFaceDetectedList
        else:
            return self.faceDetectedList
            
    def GetFaceNames(self) -> np.ndarray:
        if len(self.faceRecognizedList) == 0:
            if len(self.prevFaceRecognizedList) != 0:
                return self.prevFaceRecognizedList
        else:
            return self.faceRecognizedList

    def GetFaceName(self, id) -> str:
        ret = ''

        try:
            if self.faceRecognizedList.size == 0:
                if self.prevFaceRecognizedList.size == 0:
                    return ret
                else:
                    if id < len(self.prevFaceRecognizedList):
                        ret = self.prevFaceRecognizedList[id]
            else:
                if id < len(self.faceRecognizedList):
                    ret = self.faceRecognizedList[id]
        except Exception as e:
            print(e , "  " , type(self.faceRecognizedList))
            ret =''

        return ret
    
    def GetLeftIrisPoint(self) -> np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = (self.prevFaceLandmarkList[0][36][0] + self.prevFaceLandmarkList[0][39][0])/2
                y = (self.prevFaceLandmarkList[0][36][1] + self.prevFaceLandmarkList[0][39][1])/2   
        else:
            x = (self.faceLandmarkList[0][36][0] + self.faceLandmarkList[0][39][0])/2
            y = (self.faceLandmarkList[0][36][1] + self.faceLandmarkList[0][39][1])/2 
        return np.array([x,y])

    def GetLeftEyebrowPoint(self) ->np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = self.prevFaceLandmarkList[0][19][0]
                y = self.prevFaceLandmarkList[0][19][1]
        else:
            x = self.faceLandmarkList[0][19][0]
            y = self.faceLandmarkList[0][19][1]
        return np.array([x,y])

    def GetRightIrisPoint(self) ->np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = (self.prevFaceLandmarkList[0][42][0] + self.prevFaceLandmarkList[0][45][0])/2
                y = (self.prevFaceLandmarkList[0][42][1] + self.prevFaceLandmarkList[0][45][1])/2   
        else:
            x = (self.faceLandmarkList[0][42][0] + self.faceLandmarkList[0][45][0])/2
            y = (self.faceLandmarkList[0][42][1] + self.faceLandmarkList[0][45][1])/2 
        return np.array([x,y])

    def GetRightEyebrowPoint(self) ->np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = self.prevFaceLandmarkList[0][24][0]
                y = self.prevFaceLandmarkList[0][24][1]
        else:
            x = self.faceLandmarkList[0][24][0]
            y = self.faceLandmarkList[0][24][1]
        return np.array([x,y])

    def GetNosePoint(self) -> np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = self.prevFaceLandmarkList[0][33][0]
                y = self.prevFaceLandmarkList[0][33][1]
        else:
            x = self.faceLandmarkList[0][33][0]
            y = self.faceLandmarkList[0][33][1]
        return np.array([x,y])
        
    def GetMousePoint(self) -> np.array:
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = (self.prevFaceLandmarkList[0][48][0] + self.prevFaceLandmarkList[0][54][0])/2
                y = (self.prevFaceLandmarkList[0][48][1] + self.prevFaceLandmarkList[0][54][1])/2   
        else:
            x = (self.faceLandmarkList[0][48][0] + self.faceLandmarkList[0][54][0])/2
            y = (self.faceLandmarkList[0][48][1] + self.faceLandmarkList[0][54][1])/2 
        return np.array([x,y])

    def GetJawPoint(self):
        x = 0
        y = 0
        if np.any(self.faceLandmarkList) == False:
            if np.any(self.prevFaceLandmarkList) != False:
                x = self.prevFaceLandmarkList[0][8][0]
                y = self.prevFaceLandmarkList[0][8][1]
        else:
            x = self.faceLandmarkList[0][8][0]
            y = self.faceLandmarkList[0][8][1]
        return np.array([x,y])

    def GetArucoId(self) -> int:
        if self.arucoDetectedIds is None or len(self.arucoDetectedIds) is 0:
            if self.prevArucoDetectedIds is None or len(self.prevArucoDetectedIds) is 0:
                return
            else:
                return self.prevArucoDetectedIds[0]
        else:
            return self.arucoDetectedIds[0]

    def GetArucoIds(self) -> list:
        if self.arucoDetectedIds is None or len(self.arucoDetectedIds) is 0:
            if self.prevArucoDetectedIds is None or len(self.prevArucoDetectedIds) is 0:
                return
            else:
                return self.prevArucoDetectedIds
        else:
            return self.arucoDetectedIds

    def GetArucoCenterPoint(self) -> list:
        x = 0
        y = 0
        if self.arucoDetectedIds is None or len(self.arucoDetectedIds) is 0:
            if self.prevArucoDetectedIds is None or len(self.prevArucoDetectedIds) is 0:
                pass
            else:
                x = int((self.prevArucoDetectedCorners[0][0][0][0] + self.prevArucoDetectedCorners[0][0][2][0]) / 2)
                y = int((self.prevArucoDetectedCorners[0][0][0][1] + self.prevArucoDetectedCorners[0][0][2][1]) / 2)
        else:
            if self.arucoDetectedCorners is None or len(self.arucoDetectedCorners) is 0:
                pass

            x = int((self.arucoDetectedCorners[0][0][0][0] + self.arucoDetectedCorners[0][0][2][0]) / 2)
            y = int((self.arucoDetectedCorners[0][0][0][1] + self.arucoDetectedCorners[0][0][2][1]) / 2)

        return [x,y]

    def GetArucoRectPoint(self) -> list:
        ret = []
        if self.arucoDetectedCorners is None or len( self.arucoDetectedCorners) is 0:
            if self.prevArucoDetectedCorners is None or len(self.prevArucoDetectedCorners) is 0:
                pass
            else:
                ret = self.prevArucoDetectedCorners[0][0]
        else:
            ret = self.arucoDetectedCorners[0][0]
        return ret

    def GetArucoAngle(self)->float:
        if self.arucoDetectedIds is None or len(self.arucoDetectedIds) is 0:
            if self.prevArucoDetectedIds is None or len(self.prevArucoDetectedIds) is 0:
                pass
            else:
                return self.arucoD.GetAngle(self.prevArucoDetectedCorners[0][0])
        else:
            return self.arucoD.GetAngle(self.arucoDetectedCorners[0][0])

    def GetSketchName(self, id:int = 0)->str:
        ret = ''

        try:
            if self.sketchDetectedList.size == 0:
                if self.prevSketchDetectedList.size == 0:
                    return ret
                else:
                    if id < len(self.prevSketchDetectedList):
                        ret = self.prevSketchDetectedList[id]
            else:
                if id < len(self.sketchDetectedList):
                    ret = self.sketchDetectedList[id]
        except Exception as e:
            print(e , "  " , type(self.sketchDetectedList))
            ret =''

        return ret
    
    def GetRecognizedNumbers(self)->str:
        if self.numberRecognizedStr:
            return self.numberRecognizedStr

    def __dataSender(self):
        while True:
            if CameraEvents.RECV_DETECTED_FACE_COUNT in self.eventHandlerDic:
                count = self.GetFaceCount()
                self.eventHandlerDic[CameraEvents.RECV_DETECTED_FACE_COUNT](count)
            if CameraEvents.RECV_DETECTED_FACE_RECT in self.eventHandlerDic:
                rects = self.GetFaceRects()
                self.eventHandlerDic[CameraEvents.RECV_DETECTED_FACE_RECT](rects)
            if CameraEvents.RECV_DETECTED_FACE_NAME in self.eventHandlerDic:
                names = self.GetFaceNames()
                self.eventHandlerDic[CameraEvents.RECV_DETECTED_FACE_NAME](names)
            if CameraEvents.RECV_LEFT_IRIS_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_LEFT_IRIS_POINT](self.GetLeftIrisPoint())
            if CameraEvents.RECV_LEFT_EYEBROW_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_LEFT_EYEBROW_POINT](self.GetLeftEyebrowPoint())
            if CameraEvents.RECV_RIGHT_IRIS_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_RIGHT_IRIS_POINT](self.GetRightIrisPoint())
            if CameraEvents.RECV_RIGHT_EYEBROW_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_RIGHT_EYEBROW_POINT](self.GetRightEyebrowPoint())
            if CameraEvents.RECV_NOSE_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_NOSE_POINT](self.GetNosePoint())
            if CameraEvents.RECV_MOUSE_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_MOUSE_POINT](self.GetMousePoint())
            if CameraEvents.RECV_JAW_POINT in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_JAW_POINT](self.GetJawPoint())
            if CameraEvents.RECV_ARUCO_ID in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_ARUCO_ID](self.GetArucoId())
            if CameraEvents.RECV_ARUCO_IDS in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_ARUCO_IDS](self.GetArucoIds())
            if CameraEvents.RECV_ARUCO_CENTER_POINTS in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_ARUCO_CENTER_POINTS](self.GetArucoCenterPoint())
            if CameraEvents.RECV_ARUCO_RECT_POINTS in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_ARUCO_RECT_POINTS](self.GetArucoRectPoint())
            if CameraEvents.RECV_ARUCO_ANGLE in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_ARUCO_ANGLE](self.GetArucoAngle())
            if CameraEvents.RECV_SKETCH_NAME in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_SKETCH_NAME](self.GetSketchName())
            if CameraEvents.RECV_NUMBERS in self.eventHandlerDic:
                self.eventHandlerDic[CameraEvents.RECV_NUMBERS](self.GetRecognizedNumbers())
            time.sleep(0.15)

    def ArucoDetectorInit(self):
        if self.arucoDetectInitFlag is False:
            self.arucoD = ArucoDetctor()
            self.arucoDetectInitFlag = True
            self.drawArucoFlag = True

        print("Aruco detector initialized")
    
    def ArucoDetectorStart(self):
        if self.arucoDetectInitFlag is False:
            print("Aruco detector is not initialized")
            return

        if self.arucoDetectFlag == True:
            print("Aruco detector is already working.")
            return
        self.arucoDetectFlag = True

        th = threading.Thread(target=self.__arucodetect)
        th.deamon = True
        th.start()

    def ArucodetectorStop(self):
        if self.arucoDetectFlag == False :
            print("Aruco detector is already stopped.")
            return

        self.arucoDetectFlag = False
        time.sleep(1)

        print("Aruco detector off")

    def __arucodetect(self):
        while self.arucoDetectFlag:
            if self.raw_img is None:
                time.sleep(0.0)
                print('no input frame yet')
                continue
            try:
                coners, ids = self.arucoD(self.raw_img)
                
                if ids is not None:
                    self.arucoDetectedCorners = list(coners)
                    self.arucoDetectedIds = ids.ravel()
                    self.prevArucoDetectedCorners = self.arucoDetectedCorners.copy()
                    self.prevArucoDetectedIds = self.arucoDetectedIds.copy()
                else:
                    self.prevArucoDetectedCorners = None
                    self.prevArucoDetectedIds = None

            except Exception as e:
                print("Aruco detector error : " , e)
                continue

            time.sleep(0.05)

    def SketchDetectorInit(self):
        if self.sketchDetectInitFlag is False:
            self.sketchR = SketchRecognizer()
            self.sketchDetectInitFlag = True

        print("Sketch detector initialized")
    
    def SketchDetectorStart(self):
        if self.sketchDetectInitFlag is False:
            print("Sketch detector is not initialized")
            return

        if self.sketchDetectFlag == True:
            print("Sketch detector is already working.")
            return
        self.sketchDetectFlag = True

        th = threading.Thread(target=self.__sketchdetect)
        th.deamon = True
        th.start()

    def __sketchdetect(self):
        while self.sketchDetectFlag:
            if self.raw_img is None:
                time.sleep(0.0)
                print('no input frame yet')
                continue
            try:
                self.sketchRecognizedList, self.sketchDetectedList = self.sketchR(self.raw_img)
                self.prevSketchRecognizedList = self.sketchRecognizedList.copy()
                self.prevSketchDetectedList = self.sketchDetectedList.copy()

                if len(self.sketchRecognizedList) == 0:
                    time.sleep(0.0)
                    continue
            except Exception as e:
                print("Sketch detector error : " , e)
                continue
            
            time.sleep(0.05)

    def SketchDetectorStop(self):
        if self.sketchDetectFlag == False :
            print("Sketch detector is already stopped.")
            return

        self.sketchDetectFlag = False
        time.sleep(1)

        print("Sketch detector off")
        
    def SketchCapture(self, name:str, path:str=pkg_resources.resource_filename(__package__,"res/sketch/")):
        if bool(name) == False:
            print("Name parameter is Empty.")
            return

        if os.path.isdir(path) is False:
            os.mkdir(path)

        if self.sketchDetectFlag is False:
            print("Sketchdetector did not run")
            return

        while True:
            if len(self.sketchRecognizedList) == 0:
                print("Doesn't have a any sketch in Frame")
                time.sleep(0.0)
                continue
            
            result = self.sketchR.SaveSketch(self.raw_img,name)
            if result == 0:
                print(name + " is saved")
                break

    def TrainSketchData(self, sketchPath:str = pkg_resources.resource_filename(__package__,"res/sketch/")):
        if os.path.isdir(sketchPath) is False:
            print(sketchPath +" is not directory.")
            return
        
        orbDescriptors = []
        nameIndexList = []
        nameIntList = []

        sketchD = SketchRecognizer()
        filenames = os.listdir(sketchPath)
        for filename in filenames:
            name = os.path.basename(filename)
            image = cv2.imread(sketchPath+filename, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (150,150))
            _, des = sketchD.orbDetector.detectAndCompute(image, None)
            name = name.split('_')[0]

            if not(name in nameIndexList):
                nameIndexList.append(name)
            nameIntList.append(nameIndexList.index(name))
            orbDescriptors.append(des)
        
        self.sketchR.TrainModel(nameIndexList, nameIntList, orbDescriptors)

    def DeleteSketchData(self, name:str, sketchPath:str=pkg_resources.resource_filename(__package__,"res/sketch/")):

        if os.path.isdir(sketchPath) is False:
            print(sketchPath +" is not directory.")
            return

        self.sketchR.RemoveSketch(name, sketchPath)

        print(name + 'is deleted')

    def NumberRecognizerInit(self):
        if self.numberDetectInitFlag is False:
            self.numberR = NumberRecognizer()
            self.numberDetectInitFlag = True
        
        print("Number recognizer initialized")
    def NumberRecognizerStart(self):
        if self.numberDetectInitFlag is False:
            print("Number recognizer is not initialized")
            return

        if self.numberDetectFlag == True:
            print("Number recognizer is already working.")
            return
        self.numberDetectFlag = True

        th = threading.Thread(target=self.__numberdetect)
        th.deamon = True
        th.start()

    def __numberdetect(self):
        while self.numberDetectFlag:
            if self.raw_img is None:
                time.sleep(0.0)
                print('no input frame yet')
                continue
            try:
                self.numberRecognizedStr,self.numberDetectedList = self.numberR(self.raw_img)
                self.prevNumberDetectedList = self.numberDetectedList.copy()
            except Exception as e:
                print("Number recognizer error : " , e)
                continue
            
            time.sleep(0.05)
    
    def NumberRecognizerStop(self):
        if self.numberDetectFlag == False :
            print("Number recognizer is already stopped.")
            return

        self.numberDetectFlag = False
        time.sleep(1)

        print("Number recognizer off")