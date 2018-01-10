#!/usr/bin/python
# -*- coding:utf-8 -*-
###################################
#
# 检查主机的损坏磁盘
#
###################################

import paramiko
import sys

def DiskCheck(ip):
    try:
        # 建立一个sshclient对象
        ssh = paramiko.SSHClient()
        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
        # pkey = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa', password='12345')
        pkey = paramiko.RSAKey.from_private_key_file('/home/work/user1/scripts/keys/id_rsa')
        # 建立连接
        ssh.connect(hostname=ip,
                    port=22,
                    username='work',
                    pkey=pkey)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command("for i in $(df -h|grep data|awk '{print $6}'); do  touch $i/test.txt; done; df -h|grep data")
        # 结果放到stdout中，如果有错误将放到stderr中
        print(stdout.read().decode())
        print(stderr.read())
        # 关闭连接
        ssh.close()
    except Exception,e:
        print e

if __name__ =='__main__':
    if len(sys.argv) != 2:
        print 'Usage: python CheckDisk.py ip'
        sys.exit()
    print 'Host: %s' % sys.argv[1]
    print ''
    DiskCheck(sys.argv[1])
    print '-' * 80