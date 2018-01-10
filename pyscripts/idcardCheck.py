#!/usr/bin/python

import sys
f = open(sys.argv[1])
zero = '0'


for i in f.readlines():
    tmp1 = list(i.strip('\n').split(','))
    if len(tmp1[1]) < 18:
        num = (18 - len(tmp1[1]))
        print  tmp1[0] + ',' + num * zero + tmp1[1]
    else:
        print tmp1[0] + ',' + tmp1[1]

f.close()