# -*- coding:utf-8 -*-

import cv2
import numpy as np
import time
import os
import glob
from calibrater import calibrater

#计算存放在./results/bin文件夹里的标定内参和畸变参数的平均值
def avgMtx():
    c = calibrater()
    amtx = np.zeros((3,3))
    adist = np.zeros((1,5))
    fname = glob.glob('./results/bin/*.npy')
    for f in fname:
        c.loadMtx(f,False)
        amtx += c.mtx
        adist += c.dist
    amtx = amtx / len(fname)
    adist = adist / len(fname)
    return [amtx,adist]
