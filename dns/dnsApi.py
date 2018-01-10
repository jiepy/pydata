#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------
# email  : gengjie@outlook.com
# Create Time: 10/18/16 14:44
# ----------------------------------------
from flask import Flask
from flask import request
from flask import abort
import json
import conSql

app = Flask(__name__)


def checkParm():
    if not request.json or request.method.strip() != "POST":
        abort(400)


@app.route('/')
def hello_world():
    return ' Welcom dnsApi .\n'


@app.route('/list', methods=['GET'])
def get_all_list():
    return json.dumps(conSql.getSql())


@app.route('/add', methods=['POST'])
def insert_data():
    checkParm()
    add_data = request.json

    G = conSql.getId('dns_records', add_data['name'], add_data['type'], add_data['value'], add_data['ttl'])
    record = G['record']
    if record:
        G['status']['code'] = 0
        G['status']['msg'] = 'Error: %s.7lk.com exists.' % add_data.get('name')
        return json.dumps(G)
    else:
        conSql.add('dns_records', add_data.get('name'), add_data.get('type'),
                   add_data.get('value'), int(add_data.get('ttl')))

        G = conSql.getId('dns_records', add_data.get('name'), add_data.get('type'),
                         add_data.get('value'), int(add_data.get('ttl')))
        conSql.flushDns()
        G['status']['msg'] = 'Successfully add %s.7lk.com record.' % add_data.get('name')
        return json.dumps(G)


@app.route('/del', methods=['POST'])
def del_data():
    checkParm()
    del_data = request.json

    C = conSql.checkId('dns_records', del_data.get('id'))
    if C['status']['code'] == 1:
        D = conSql.delete('dns_records', del_data.get('id'))
        conSql.flushDns()
        return json.dumps(D)
    else:
        return (json.dumps(C))


@app.route('/mod', methods=['POST'])
def mod_data():
    checkParm()
    mod_data = request.json

    C = conSql.checkId('dns_records', mod_data.get('id'))
    if C['status']['code'] == 1:
        M = conSql.update('dns_records', mod_data.get('name'), mod_data.get('type'),
                          mod_data.get('value'), mod_data.get('ttl'), mod_data.get('id'))
        conSql.flushDns()
        return json.dumps(M)
    else:
        return (json.dumps(C))


@app.route('/status', methods=['POST'])
def switch():
    checkParm()
    s_data = request.json

    if not s_data.get('id') and not s_data.get('status'):
        abort(400)

    if s_data.get('status') == 'disable':
        C = conSql.checkId('dns_records', s_data.get('id'))
        if C['status']['code'] == 1:
            T = conSql.dns2Undo(s_data.get('id'))
            conSql.flushDns()
            return json.dumps(T)
        else:
            C['status']['msg'] = "record id %s not found in dns_records" % s_data.get('id')
            return json.dumps(C)

    if s_data.get('status') == 'enable':
        C = conSql.checkId('dns_records_undo', s_data.get('id'))
        if C['status']['code'] == 1:
            T = conSql.dns2Undo(s_data.get('id'), srctable='dns_records_undo', destable='dns_records', status='enable')
            T['status']['msg'] = 'Successfully enable  record %s.' % s_data.get('id')
            conSql.flushDns()
            return json.dumps(T)
        else:
            C['status']['msg'] = "record id %s not found in dns_records_undo" % s_data.get('id')
            return json.dumps(C)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)
