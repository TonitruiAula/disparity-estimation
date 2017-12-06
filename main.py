# -*- coding:utf-8 -*-

from tools import *
from calibrater import calibrater

c = calibrater()
c.calibrate(0)
m,d = avgMtx()
print '\nAverage mtx:\n',m
print 'Average dist:\n',d