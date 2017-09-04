#！/usr/bin/env python
#coding:utf-8
import pymysql
from .dbconfig import DbConfig
__author__ = 'caryr'
class PopulationSample(object):
    def __init__(self):
        self.db = pymysql.connect(**DbConfig.db1)
        self.cursor = self.db.cursor()
    def get_jiuyelv_sample_count(self):
        sql = "select * from dataexchange_1_ban where universitycode=10439 and subjectcode=2000"
        sql_result = self.cursor.execute(sql)
        return sql_result
    def get_xiaoyoutuijiajiandu_sample_count(self):
        sql = "select * from dataexchange_history where universitycode=10439 and subjectcode=47"
        sql_result = self.cursor.execute(sql)
        return sql_result
    def get_nenglimanzu_sample_count(self):
        sql="select DISTINCT StudentSerialNo  from dataexchange_history where universitycode=10439 and type='b'and " \
            "Answer not like '9%'and Answer not like '%->->'and Answer not LIKE '%->'and 'Year'=2016"
        sql_result = self.cursor.execute(sql)
        return sql_result
    def __del__(self):
        self.db.close()