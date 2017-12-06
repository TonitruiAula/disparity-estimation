# -*- coding:utf-8 -*-

import cv2
import numpy as np
import time
import os
import glob
from calibrater import calibrater

#计算存放在./results/bin文件夹里的标定内参和畸变参数的平均值,
#weight表示是否按照图片数加权计算平均，默认为True
def avgMtx(weight = True):
    c = calibrater()
    amtx = np.zeros((3,3))
    adist = np.zeros((1,5))
    aerror = 0
    fname = glob.glob('./results/bin/*.npz')
    imageNum = 0
    for f in fname:
        c.loadMtx(f,False)
        c.calError()
        if weight == True:
            imageNum += c.imageNum
            amtx += c.mtx * c.imageNum
            adist += c.dist * c.imageNum
            aerror += c.total_error * c.imageNum
        else:
            amtx += c.mtx
            adist += c.dist
            aerror += c.total_error
    if weight == True:
        amtx = amtx / imageNum
        adist = adist / imageNum
        aerror = aerror / imageNum
    else:
        amtx = amtx / len(fname)
        adist = adist / len(fname)
        aerror = aerror / len(fname)
    return [amtx,adist,aerror,len(fname)]

#.npz转.txt
def npz2txt(filename):
    c = calibrater()
    c.loadMtx(filename)
    c.calError()
    filename = './results/text' + filename[13:-4] + '.txt'
    f = open(filename,'w')
    f.write('ret:'+ str(c.ret) + '\nnumber of images:' + str(c.imageNum) + '\nmtx:\n')
    f.close()
    f = open(filename,'ab')
    np.savetxt(f,c.mtx,fmt='%.6f')
    f.close()
    f = open(filename,'a')
    f.write('\ndist:\n')
    f.close()
    f = open(filename,'ab')
    np.savetxt(f,c.dist,fmt='%.6f')
    f = open(filename,'a')
    f.write('\ntotal-error:' + str(c.total_error) + '\n')
    f.close()

#将存放在./results/bin文件夹里的二进制文件全部转为文本文件并放入对应的text文件夹
def npzall2txt():
    fname = glob.glob('./results/bin/*.npz')
    for f in fname:
        npz2txt(f)
