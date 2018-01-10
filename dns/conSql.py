#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------
# email  : gengjie@outlook.com
# Create Time: 9/30/16 13:53
# ----------------------------------------
import time
import MySQLdb
import datetime

# define mysql vars

DB_HOST = '10.9.2.100'
DB_USER = 'jie'
DB_PASS = 'jie123'
DB_NAME = 'namedmanager'


def getSql():
    """
    返回一个字典，包含status以及各个record，每个record是一个字典
    """
    data = {}
    data['status'] = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "select name,type,content,ttl,id from dns_records where id_domain=3 and type='A';"
        cursor.execute(sql)
        results = cursor.fetchall()
        records = []
        for r in results:
            record = {}
            record['id'] = r[4]
            record['name'] = r[0]
            record['type'] = r[1]
            record['value'] = r[2]
            record['ttl'] = r[3]
            record['domain'] = '7lk.com'
            record['status'] = 'enable'
            records.append(record)
        sql2 = "select name,type,content,ttl,id from dns_records_undo where id_domain=3 and type='A';"
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        for r in results2:
            urecord = {}
            urecord['id'] = r[4]
            urecord['name'] = r[0]
            urecord['type'] = r[1]
            urecord['value'] = r[2]
            urecord['ttl'] = r[3]
            urecord['domain'] = '7lk.com'
            urecord['status'] = 'disable'
            records.append(urecord)

        data['records'] = records
        data['status']['code'] = 1
        data['status']['msg'] = 'Get all records for Success.'
        cursor.close()
        con.close()
        return data

    except MySQLdb.Error, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error: %s ' % e
        return data


def add(tablename, name, type, content, ttl):
    """
    返回一个字典，包含添加词条记录的状态/是否成功
    """
    cursor = None
    con = None
    data = {}
    data['status'] = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "INSERT INTO %s (id_domain, name, type, content, ttl) values (%s,'%s', '%s','%s','%s')" % \
              (tablename, 3, name, type, content, ttl)
        cursor.execute(sql)

        con.commit()
        data['status']['code'] = 1
        data['status']['msg'] = 'Successfully add %s.7lk.com record.' % name
        return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error: %s ' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def delete(tablename, id):
    """
    返回一个字典，包含状态执行成功与否
    """
    cursor = None
    con = None
    data = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = " DELETE FROM %s WHERE id=%d " % (tablename, id)
        cursor.execute(sql)
        con.commit()
        data['status'] = {}
        data['status']['code'] = 1
        data['status']['msg'] = 'Successfully deleted  record %s.' % id
        return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error: %s ' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def update(tablename, name, type, content, ttl, id):
    """
    返回一个字典，包含code状态
    """
    cursor = None
    con = None
    data = {}
    data['status'] = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "UPDATE %s set type='%s',content='%s',ttl=%s,name='%s' where id='%s'" %\
              (tablename, type, content, ttl, name, id)
        cursor.execute(sql)
        con.commit()
        data['status']['code'] = 1
        data['status']['msg'] = 'Successfully updated %s.7lk.com records.' % name
        return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error: %s ' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def getId(tablename, name, type, content, ttl):
    """
    检查是否有此记录，返回一个字典，包含id和name
    """
    cursor = None
    con = None
    data = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = " SELECT * FROM %s WHERE name='%s' and type='%s' and id_domain=3 and content='%s' and ttl='%s' " \
              % (tablename, name, type, content, ttl)
        cursor.execute(sql)
        results = cursor.fetchall()
        records = []
        for r in results:
            record = {}
            record['id'] = r[0]
            record['name'] = r[2]
            records.append(record)

        data['record'] = {}
        data['status'] = {}
        data['record']['id'] = records[0]['id']
        data['record']['name'] = records[0]['name']
        data['status']['code'] = 1
        data['status']['msg'] = 'Get id Success.'
        return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error : %s' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def checkId(tablename, id):
    """
    检查此记录是否存在，返回一个字典，包含code状态
    """
    cursor = None
    con = None
    data = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = " SELECT * FROM %s WHERE id= '%s'" % (tablename, id)
        cursor.execute(sql)
        # print(sql)
        results = cursor.fetchall()
        records = []
        for r in results:
                record = {}
                record['id'] = r[0]
                record['name'] = r[2]
                records.append(record)

        data['record'] = {}
        data['status'] = {}

        if len(records) == 1:
            data['record']['id'] = records[0]['id']
            data['record']['name'] = records[0]['name']
            data['status']['code'] = 1
            data['status']['msg'] = 'Get id Success.'
            return data
        else:
            data['status']['code'] = 0
            data['status']['msg'] = 'record id %s not found' % id
            return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error : %s' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def dns2Undo(id, srctable='dns_records', destable='dns_records_undo',  status='disable'):
    """
    此步骤是操作是否开启，若开启，则先将此记录插入到dns_records_undo,然后在dns_records里面删除，
    反之亦然.
    """
    cursor = None
    con = None
    data = {}
    data['status'] = {}
    data['record'] = {}
    try:
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "insert into %s(id, id_domain, name, type, content, ttl, prio)  " \
              "select id, id_domain, name, type, content, ttl, prio from %s where " \
              " id = %s;" % (destable, srctable, id)
        cursor.execute(sql)
        sql2 = " DELETE FROM %s WHERE id=%s" % (srctable, id)
        cursor.execute(sql2)
        con.commit()

        data['record']['id'] = id
        data['record']['status'] = status
        data['status']['code'] = 1
        data['status']['msg'] = 'Successfully disable  record %s.' % id
        return data

    except Exception, e:
        data['status']['code'] = 0
        data['status']['msg'] = 'Error: %s ' % e
        return data

    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def updateConfig():
    cursor = None
    con = None
    try:
        nowtimestramp = int(time.time())
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "update config set value=%d where name='SYNC_STATUS_CONFIG'" % nowtimestramp
        cursor.execute(sql)
        con.commit()
    except Exception, e:
        print e
    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()


def updateSoasn(domain_id):
    cursor = None
    con = None
    try:
        today = datetime.date.today().strftime('%Y%m%d')
        con = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset='utf8')
        cursor = con.cursor()
        sql = "select soa_serial from dns_domains where id=%d;" % domain_id
        cursor.execute(sql)
        dbsoasn = str(cursor.fetchone()[0])
        dbday = dbsoasn[0:8]
        count = int(dbsoasn[8::])

        if dbday != today:
            soasn = int(today + '01')
        else:
            count += 1
            if count < 10:
                soasn = int(dbday + '0' + str(count))
            else:
                soasn = int(dbday + str(count))

        sql1 = "update dns_domains set soa_serial=%d where id=%d;" % (soasn, domain_id)
        cursor.execute(sql1)
        con.commit()
    except Exception, e:
        print e
    finally:
        if cursor and con is not None:
            cursor.close()
            con.close()

def flushDns():
    updateConfig()
    updateSoasn(3)
