#!/usr/bin/env python
# -*- coding:utf-8 -*-
####################################################################
# Filename: logcount.py
# Date: 2019/01/09
# Desc: 统计nginx日志10分钟内的499,5xx状态码数量
# ver : 0.1.0
####################################################################
import re
import sys
import json
import time
import subprocess


def logname(name, logdir='/home/work/logs/nginx/'):
    ''' 传入日志名称，返回日志全路径'''
    mylog = logdir + name
    return mylog


def filterlog(logfile, st, end):
    ''' 根据开始和结束时间过滤日志文件, return str'''

    # awkCmd = """ awk -F "\\"|+|T" '{t=sprintf("%s %s", $4, $5); if(t>="2018-01-08 \
    # 19:49:45" && t<="2018-01-08 19:50:45" && $0~/"status":(5..|499)/){print $0}}' """

    awkCmd = """ awk -F "\\"|+|T" '{t=sprintf("%s %s", $4, $5); if(t>=\""""
    start_time = st
    awkAnd = """\" && t<=\""""
    end_time = end
    awkCmd2 = """\" && $0~/"status":(5..|499)/){print $0}}' """

    filterCmd = awkCmd + start_time + awkAnd + end_time + awkCmd2 + logfile
    p = subprocess.Popen(filterCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout


def cleanlog(loglist):
    ''' 清洗日志，取出uri和status, return 列表'''
    datalist = ['a']
    for line in loglist:
        if len(line) > 0:
            jdata = json.loads(line)
            if 499 < jdata["status"] < 600:
                jdata["status"] = '5xx'
            data = str(jdata["uri"]) + '@' + str(jdata["status"])
            datalist.append(data)

    return datalist


def counter(countstr):
    ''' 传入清洗过的列表转换的str，计算数量, return 字典'''
    err5 = re.findall(r'@5xx', countstr)
    err499 = re.findall(r'@499', countstr)
    mydict = {}
    mydict['5xx'] = len(err5)
    mydict['499'] = len(err499)
    # print("[code 5xx:%d ],[code 499:%d]"%(len(err5),len(err499)))

    return mydict


def main(logfile, min=10):
    '''使用方法： salt af-xxx.uc logcount.main logfile='tmp.log' min=10
           logfile  - 指定nginx的日志文件名称，[必须参数]
           min='10' - 默认时间是取从执行命令时间开始计算10分钟内的日志，[可选参数]'''
    # 时间处理，获取当前时间和*分钟前的时间
    countSec = min * 60
    nowTime = (time.time())
    agoTime = (time.time() - countSec)
    starTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(agoTime)))
    endTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nowTime)))

    # 获取日志文件名称
    logFile = logname(logfile)

    # 根据时间过滤日志
    flog = filterlog(logFile, starTime, endTime)

    # 清洗日志
    p = cleanlog(flog.split('\n'))

    # 转换成字符串，正则匹配计算
    astr = '\n'.join(p)
    result = counter(astr)

    # 添加标记信息
    timestr = starTime + ' ~ ' + endTime
    result['logfile'] = logfile
    result['timerange'] = timestr

    return result


if __name__ == "__main__":
    # 脚本测试
    p = main('tmp.log', 20)
    print
    p
