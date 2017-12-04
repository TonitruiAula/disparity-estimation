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
        self.ret = 0
        self.mtx = np.zeros((3,3))
        self.dist = np.zeros((1,3))
        self.rvecs = np.zeros((1,3))
        self.tvecs = np.zeros((1,3))
        self.cal = False
    
    def calCalibrate(self):
        w = self.numWidth - 1
        h = self.numHeight - 1

        objp = np.zeros((w*h,3), np.float32)
        objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
        objpoints = [] # 在世界坐标系中的三维点
        imgpoints = [] # 在图像平面的二维点
        gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (w,h),None)
        if ret == True:
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
            objpoints.append(objp)
            #print u'世界坐标点\n', objpoints
            imgpoints.append(corners)
            # 将角点在图像上显示
            #print u'图像坐标点\n', imgpoints
            img = self.frame.copy()
            cv2.drawChessboardCorners(img, (w,h), corners, ret)
            #ccv2.imshow('findCorners',img)
            #cv2.imwrite('corner.png',img)
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            # print "ret:",ret  
            # print "mtx:\n",mtx        # 内参数矩阵  
            # print "dist:\n",dist      # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)  
            # print "rvecs:\n",rvecs    # 旋转向量  # 外参数  
            # print "tvecs:\n",tvecs    # 平移向量  # 外参数  
        else:
            print 'Cannot find corners'


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
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.cal = False
                break
            # elif key == ord('a'):
            #     print u'棋盘格宽: ', numWidth
            #     print u'棋盘格高: ', numHeight
            elif key == ord('c'):
                self.cal = True
                if self.cal == True:
                    # print "ret:",self.ret  
                    print "mtx:\n",self.mtx        # 内参数矩阵  
                    # print "dist:\n",self.dist      # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)  
                    # print "rvecs:\n",self.rvecs    # 旋转向量  # 外参数  
                    # print "tvecs:\n",self.tvecs    # 平移向量  # 外参数  
                #self.cal = not self.cal
                
            if self.cal:
                self.calCalibrate()
        vc.release()
        cv2.destroyAllWindows()


c = calibrater()
c.calibrate()