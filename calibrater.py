# -*- coding:utf-8 -*-

import cv2
import numpy as np

def fun(x):
    pass

class calibrater:
    def __init__(self):
        self.criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
        self.numWidth = 10
        self.numHeight = 7
        self.cal = False
    

    def initCalibration(self):
        self.numWidth = cv2.getTrackbarPos('棋盘格宽','capture')
        self.numHeight = cv2.getTrackbarPos('棋盘格高','capture')
        self.objpoints = []
        self.imgpoints = []
        print 'Start calibrating...'

    def shotBoards(self):
        w = self.numWidth - 1
        h = self.numHeight - 1
        objp = np.zeros((w*h,3), np.float32)
        objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
        ret, corners = cv2.findChessboardCorners(self.gray, (w,h),None)
        if ret == True:
            cv2.cornerSubPix(self.gray,corners,(11,11),(-1,-1),self.criteria)
            self.objpoints.append(objp)
            #print u'世界坐标点\n', objpoints
            self.imgpoints.append(corners)
            # 将角点在图像上显示
            img = self.frame.copy()
            cv2.drawChessboardCorners(img, (w,h), corners, ret)
            cv2.imshow('findCorners',img)
            print 'Picture shot for calibration'
        else:
            print 'Cannot find corners'

    def printResult(self,tr = False):
        print "ret:",self.ret  
        print "mtx:\n",self.mtx        # 内参数矩阵  
        if tr == True:
            print "dist:\n",self.dist      # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)  
            print "rvecs:\n",self.rvecs    # 旋转向量  # 外参数  
            print "tvecs:\n",self.tvecs    # 平移向量  # 外参数  


    def calibrate(self):
        vc = cv2.VideoCapture(0)

        cv2.namedWindow('capture')
        cv2.createTrackbar('棋盘格宽','capture',10,30,fun)
        cv2.createTrackbar('棋盘格高','capture',7,30,fun)

        while(1):
            ret,self.frame = vc.read()
            #print ret
            cv2.imshow('capture',self.frame)
            #cv2.calibrateCamera()
            self.numWidth = cv2.getTrackbarPos('棋盘格宽','capture')
            self.numHeight = cv2.getTrackbarPos('棋盘格高','capture')
            self.gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.cal = False
                break
            # elif key == ord('a'):
            #     print u'棋盘格宽: ', numWidth
            #     print u'棋盘格高: ', numHeight
            elif key == ord('c'):
                self.cal = not self.cal
                if self.cal == True:
                    self.initCalibration()
                else:
                    self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
                    self.printResult()
                    print 'Calibration finished!'
            elif key == ord('s'):
                if self.cal == True:
                    self.shotBoards()
                
        vc.release()
        cv2.destroyAllWindows()


c = calibrater()
c.calibrate()