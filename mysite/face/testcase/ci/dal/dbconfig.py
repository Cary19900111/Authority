#！/usr/bin/env python
#coding:utf-8
import pymysql
__author__ = 'caryr'
class DbConfig(object):
    db1 = {
        'host': '192.168.0.151',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ci_2015_1',
        'cursorclass': pymysql.cursors.DictCursor,  # 元组与列表字典的区别
        'charset': 'utf8mb4',
    }
    db2 = {
        'host': '192.168.0.151',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ci_2015_2',
        'cursorclass': pymysql.cursors.DictCursor,  # 元组与列表字典的区别
        'charset': 'utf8mb4',
    }
    db3 = {
        'host': '192.168.0.151',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ci_2015_3',
        'cursorclass': pymysql.cursors.DictCursor,  # 元组与列表字典的区别
        'charset': 'utf8mb4',
    }
    db4 = {
        'host': '192.168.0.151',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ci_2015_4',
        'cursorclass': pymysql.cursors.DictCursor,  # 元组与列表字典的区别
        'charset': 'utf8mb4',
    }
    db5 = {
        'host': '192.168.0.151',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ci_2015_5',
        'cursorclass': pymysql.cursors.DictCursor,  # 元组与列表字典的区别
        'charset': 'utf8mb4',
    }