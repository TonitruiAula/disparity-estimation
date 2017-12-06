# -*- coding:utf-8 -*-

import sys
from tools import *
from calibrater import calibrater

if __name__ == '__main__':
    #相机标定
    c = calibrater()
    c.calibrate(0)
    #标定结束之后计算平均结果
    m,d,e,n = avgMtx()
    print '\nTotal number of data:' + str(n)
    print 'Average mtx:\n',m
    print 'Average dist:\n',d    
    print 'Average re-projection error:\n',e