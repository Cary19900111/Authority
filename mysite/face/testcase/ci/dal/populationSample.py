#！/usr/bin/env python
#coding:utf-8
import pymysql
from .dbconfig import DbConfig
__author__ = 'caryr'
class PopulationSample(object):
    def __init__(self,para):
        self.para = para
        self.db_all =[DbConfig.db1,DbConfig.db2,DbConfig.db3,DbConfig.db4,DbConfig.db5]
        self.db = pymysql.connect(**self.db_all[int(self.para['db']-1)])
        self.cursor = self.db.cursor()

    def get_state(self):
        sql= "select state from repairuniversity where universityid=%s and productid=1" %(self.para['id'])
        result = self.cursor.execute(sql)
        return result
    def get_department_num(self):
        sql = "select count(*) from department where universityid=%s and productid=1" %(self.para['id'])
        sql_distinct = "select distinct Code from department where universityid=%s and productid=1" %(self.para['id'])
        result_sql = self.cursor.execute(sql)
        result_sql_distinct = self.cursor.execute(sql_distinct)
        if(result_sql == result_sql_distinct):
            return result_sql
        return 0

    def get_major_num(self):
        sql = "select * from major where universityid=%s and productid=1" %(self.para['id'])
        sql_distinct = "select distinct Code from major where universityid=%s and productid=1" %(self.para['id'])
        result_sql = self.cursor.execute(sql)
        result_sql_distinct = self.cursor.execute(sql_distinct)
        if(result_sql == result_sql_distinct):
            return result_sql
        return 0

    def get_jiuyelv_sample_count(self):
        sql_ban = "select * from dataexchange_1_ban where universitycode=%s and subjectcode=2000 and " \
                  "type='1' and year=%s" %(self.para['code'],self.para['year'])
        sql_history = "select * from dataexchange_history where universitycode=%s and subjectcode=2000 " \
                      "and type='1' and year=%s" %(self.para['code'],self.para['year'])
        result_ban = self.cursor.execute(sql_ban)
        result_history =  self.cursor.execute(sql_history)
        return result_ban+result_history

    def get_xiaoyoutuijiajiandu_sample_count(self):
        sql_ban = "select * from dataexchange_1_ban where universitycode=%s and subjectcode=47 " \
                  "and type=1 and year=%s" %(self.para['code'],self.para['year'])
        sql_history = "select * from dataexchange_history where universitycode=%s and subjectcode=47 " \
                      "and type=1 and year=%s" %(self.para['code'],self.para['year'])
        result_history = self.cursor.execute(sql_ban)
        sql_result = self.cursor.execute(sql_history)
        return result_history+sql_result
    # def get_nenglimanzu_sample_count(self):
    #     sql="select DISTINCT StudentSerialNo  from dataexchange_history where universitycode=10439 and type='b'and " \
    #         "Answer not like '9%'and Answer not like '%->->'and Answer not LIKE '%->'and 'Year'=2016"
    #     sql_result = self.cursor.execute(sql)
    #     return sql_result
    def __del__(self):
        self.db.close()