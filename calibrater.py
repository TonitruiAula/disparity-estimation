# -*- coding:utf-8 -*-

import cv2
import numpy as np
import time

class calibrater:
    #初始化标定状态
    def __init__(self):
        self.cal = False

    #更新格的宽高
    def update(self,x):
        self.numWidth = cv2.getTrackbarPos('棋盘格宽','capture')
        self.numHeight = cv2.getTrackbarPos('棋盘格高','capture')

    #初始化标定
    def initCalibration(self):
        #获取格的宽高
        self.update(0)
        #清空世界坐标点和图像坐标点
        self.objpoints = [] #世界坐标点
        self.imgpoints = [] #图像坐标点
        #图片数置零
        self.imageNum = 0
        print 'Start calibrating...'

    #为标定工作拍摄图片
    def shotBoards(self):
        #获取内部的格点数目
        w = self.numWidth - 1
        h = self.numHeight - 1
        # 设置寻找亚像素角点的参数，最大循环次数30和最大误差容限0.001
        criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
        #获取标定板角点的位置
        objp = np.zeros((w*h,3), np.float32)
        objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
        ret, corners = cv2.findChessboardCorners(self.gray, (w,h),None)
        if ret == True:
            #获取亚像素角点
            cv2.cornerSubPix(self.gray,corners,(11,11),(-1,-1),criteria)
            #添加世界坐标点和图像坐标点
            self.objpoints.append(objp)
            self.imgpoints.append(corners)
            # 将角点在图像上显示
            img = self.frame.copy()
            cv2.drawChessboardCorners(img, (w,h), corners, ret)
            cv2.imshow('findCorners',img)
            self.imageNum = self.imageNum + 1
            print 'Picture shot for calibration'
        else:
            print 'Cannot find corners'

    #打印结果，tr表示是否打印外参数,sf表示是否保存内参信息至文件
    def printResult(self,tr = False,sf = True):
        print "ret:",self.ret  
        print "number of images:",self.imageNum
        print "mtx:\n",self.mtx        # 内参数矩阵  
        print "dist:\n",self.dist      # 畸变系数   distortion cofficients = (k_1,k_2,p_1,p_2,k_3)  
        if tr == True:
            print "rvecs:\n",self.rvecs    # 旋转向量   
            print "tvecs:\n",self.tvecs    # 平移向量   
        if sf == True:  #保存内参至文件
            fileName = 'results/' + time.strftime('%Y_%m_%d_%H_%M_%S')
            f = open(fileName,'w')
            f.write('ret:'+ str(self.ret) + '\nnumber of images:' + str(self.imageNum) + '\nmtx:\n')
            f.close()
            f = open(fileName,'ab')
            np.savetxt(f,self.mtx,fmt='%.6f')
            f.close()
            f = open(fileName,'a')
            f.write('\ndist:\n')
            f.close()
            f = open(fileName,'ab')
            np.savetxt(f,self.dist,fmt='%.6f')

    #标定过程
    def calibrate(self):
        #获取摄像头信息
        vc = cv2.VideoCapture(0)
        #建立窗口
        cv2.namedWindow('capture')
        cv2.createTrackbar('棋盘格宽','capture',10,30,self.update)
        cv2.createTrackbar('棋盘格高','capture',7,30,self.update)
        
        while(1):
            ret,self.frame = vc.read()  #读取当前帧
            cv2.imshow('capture',self.frame)
            # #更新棋盘格宽高
            # self.numWidth = cv2.getTrackbarPos('棋盘格宽','capture')
            # self.numHeight = cv2.getTrackbarPos('棋盘格高','capture')
            #计算灰度图
            self.gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
            #获取按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): #q键退出
                self.cal = False
                break
            elif key == ord('c'):   #c键开始/结束标定
                self.cal = not self.cal #切换状态
                #开始初始化标定
                if self.cal == True:
                    self.initCalibration()
                #结束是计算标定结果并输出
                else:
                    self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
                    self.printResult()
                    print 'Calibration finished!'
            elif key == ord('s'):   #s键拍照
                if self.cal == True:
                    self.shotBoards()                
        vc.release()
        cv2.destroyAllWindows()


c = calibrater()
c.calibrate()