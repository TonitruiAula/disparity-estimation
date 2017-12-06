# -*- coding:utf-8 -*-

import sys
from tools import *
from calibrater import calibrater

if __name__ == '__main__':
    c = calibrater()
    c.calibrate(0)
    m,d = avgMtx()
    print '\nAverage mtx:\n',m
    print 'Average dist:\n',d