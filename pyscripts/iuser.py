#!/usr/bin/python

import pymysql
import time


'''

CREATE TABLE `os_user` (
  `user` varchar(20) NOT NULL,
  `haspass` char(5) NOT NULL,
  `uid` int(10) NOT NULL,
  `gid` int(10) NOT NULL,
  `descuser` varchar(100) NOT NULL,
  `homedir` varchar(100) NOT NULL,
  `loginshell` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `unique_var` (`user`,`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


'''

try:
    conn = pymysql.connect(host='127.0.0.1',unix_socket='/tmp/mysql.sock',\
                           user='root',passwd='123456',db='pydb')
    cur = conn.cursor()
    f = open('passwd')

    try:
        for i in f.readlines():
            Tmplist = list(i.strip('\n').split(':'))
            sql = 'INSERT INTO os_user \
                  (user,haspass,uid,gid,descuser,homedir,loginshell) values \
                  (\'%s\',\'%s\',%s,%s,\'%s\',\'%s\',\'%s\')' % \
                  (Tmplist[0],Tmplist[1],Tmplist[2],Tmplist[3],Tmplist[4],Tmplist[5],Tmplist[6])
            cur.execute(sql)
            time.sleep(1)
            conn.commit()
            print 'Create user %s Successful..' % Tmplist[0]
    except pymysql.err.IntegrityError as e:
         print 'User %s exits.' % Tmplist[0]
         print 'Please check, Exit...'
    except Exception as e:
         print 'Error : %s ' % e

except Exception as e:
     print 'Error : %s ' % e


finally:
    cur.close()
    conn.close()
    f.close()