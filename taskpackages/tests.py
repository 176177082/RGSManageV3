# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.test import TestCase
# Create your tests here.

import os
import sys
import psycopg2

reload(sys)
sys.setdefaultencoding('utf8')


def get_user_data(tablename):
    # 获取用户表数据
    conn = psycopg2.connect(dbname="mmanageV2.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    SELECTSQL = u"select * from %s order by id" % tablename
    cur.execute(SELECTSQL)
    while True:
        data = cur.fetchone()
        if data:
            print data
            # 向users_user表中插入字段
            user_insert(data, "users_user")
        else:
            conn.close()
            return


def user_insert(data, tablename):
    """users_user表数据的迁移"""
    # users_users
    conn = psycopg2.connect(dbname="mmanageV3.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    # sql = "insert into %s (id, username, password, is_superuser, is_staff, is_active, isadmin) values (%d, '%s', '%s', %r, %r, %r, %r)" %(tablename, data[0],data[4], data[1], data[3], data[8], data[9], data[11])
    sql = u"insert into %s (id, username, password,is_superuser, is_staff, is_active,date_joined,isadmin) values (%d, '%s', '%s',%r,%r, %r,%r, %r)" % (
        tablename, data[0], data[4], data[1], data[3], data[8], data[9], str(data[10]), data[11])
    # print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackage_data(tablename):
    # 获取主任务包表数据
    conn = psycopg2.connect(dbname="mmanageV2.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    data_list = cur.fetchall()
    print data_list
    for data in data_list:
        # data = cur.fetchone()
        data = list(data)
        print data
        forginkey_id = data[10]
        cur.execute(u"select username from users_users where id = %d" % forginkey_id)
        username = cur.fetchone()[0]
        data[10] = username
        print data
        taskpackage_insert(data)

    conn.close()


def taskpackage_insert(data):
    """taskpackages_taskpackage表数据的迁移"""
    conn = psycopg2.connect(dbname="mmanageV3.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = u"insert into taskpackages_taskpackage (id,name,owner,exowner,mapnums,file,status,describe,createtime,updatetime,isdelete) values (%d,'%s','%s','%s','%s',%r,%r, '%s',%r, %r,%r)" % (
        data[0], data[1], data[10], data[2], data[3], data[4], data[5], data[9], str(data[7]), str(data[8]), data[6])
    cur.execute(sql)
    sql_son = u"insert into taskpackages_taskpackageson (id,taskpackage_name,user_username,version,file,describe,createtime,updatetime,isdelete) values (%d,'%s','%s','%s',%r,'%s',%r,%r,%r)" % (
        data[0], data[1], data[10], 'v0.0', data[4], data[9], str(data[7]), str(data[8]), data[6])
    cur.execute(sql_son)
    conn.commit()
    conn.close()


def get_taskpackageson_data(tablename):
    # 获取子任务包表数据
    conn = psycopg2.connect(dbname="mmanageV2.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    data_list = cur.fetchall()
    for data in data_list:
        data = list(data)
        print data
        taskpackage_id = data[-1]
        cur.execute(u"select name from taskpackages_taskpackage where id = %d" % taskpackage_id)
        taskpackage_name = cur.fetchone()[0]
        data[8] = taskpackage_name

        user_id = data[7]
        cur.execute(u"select username from users_users where id = %d" % user_id)
        username = cur.fetchone()[0]
        data[7] = username

        taskpackageson_insert(data)

    conn.close()


def taskpackageson_insert(data):
    """taskpackages_taskpackageson表数据的迁移"""

    conn = psycopg2.connect(dbname="mmanageV3.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = u"insert into taskpackages_taskpackageson (taskpackage_name,user_username,version,file,describe,createtime,updatetime,isdelete) values ('%s','%s','%s',%r,'%s',%r,%r,%r)" % (
        data[8], data[7], data[1], data[6], data[5], str(data[3]), str(data[4]), data[2])

    # sql = "insert into taskpackages_taskpackageson (taskpackage_name,user_username,version,file,describe,createtime,updatetime,isdelete) values ('111','222','2222','3333','22222','2018-12-12 20:06:56.016+08','2018-12-12 20:06:56.016+08',FALSE )"

    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackageowner_data(tablename):
    # 获取@表数据
    conn = psycopg2.connect(dbname="mmanageV2.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    data_list = cur.fetchall()
    for data in data_list:
        data = list(data)
        print data
        taskpackage_id = data[-1]
        cur.execute(u"select name from taskpackages_taskpackage where id = %d" % taskpackage_id)
        taskpackage_name = cur.fetchone()[0]
        data[-1] = taskpackage_name

        taskpackageowner_insert(data)

    conn.close()


def taskpackageowner_insert(data):
    """taskpackages_taskpackageson表数据的迁移"""

    conn = psycopg2.connect(dbname="mmanageV3.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = u"insert into taskpackages_taskpackageowner (id,taskpackage_name,owner,exowner,describe,createtime,isdelete) values (%d,'%s','%s','%s','%s',%r,FALSE )" % (
        data[0], data[-1], data[1], data[2], data[4], str(data[3]))

    cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # 迁移users_user表
    # get_user_data("users_users")

    # 迁移主任务包表
    get_taskpackage_data("taskpackages_taskpackage")

    # 迁移主任务包子版本
    # get_taskpackageson_data("taskpackages_taskpackageversion")

    # taskpackageson_insert()
    # 迁移@功能表
    # get_taskpackageowner_data("taskpackages_taskpackageowner")
    pass
