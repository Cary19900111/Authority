#！/usr/bin/env python
#coding:utf-8
import unittest
from selenium import webdriver
import requests
import json,re
from ..ci.common.ParaTestCase import ParametrizedTestCase
from .dal.populationSample import PopulationSample

__author__ = 'caryr'
#@unittest.skip("test2")
class Testjiuyelv(ParametrizedTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_state(self):
        real_result = PopulationSample(self.param).get_state()
        self.assertEqual(real_result, 2)

    def test_department_count(self):
        department_load_data = {
            'action': 'getdepartment',
            'callbackparam': 'jQuery18204532285189406071_1504767677554',
            'universityid': self.param['id'],
            'userid': '7261',
            'version': '3',
            'modelType': 'A',
            'productid': '1',
            '_': '1504768511790',
        }
        department_response = requests.get(url="http://ciadmin.mycos.com//api/common.aspx", params=department_load_data,timeout=2)
        pattern = re.compile(r'.*"data":(.*])')
        num = re.findall(pattern, department_response.text)
        pattern_depart = re.compile(r'{.*?}')
        result = re.findall(pattern_depart, num[0])
        expect_result = PopulationSample(self.param).get_department_num()
        self.assertEqual(len(result)-1, expect_result)

    def test_major_count(self):
        major_load_data = {
            'action': 'getmajor',
            'callbackparam': 'jQuery18204532285189406071_1504767677554',
            'universityid': self.param['id'],
            'userid': '7261',
            'version': '3',
            'modelType': 'A',
            'productid': '1',
            '_': '1504850289154',
        }
        major_response = requests.get(url="http://ciadmin.mycos.com//api/common.aspx", params=major_load_data,timeout=2)
        pattern = re.compile(r'.*"data":(.*])')
        num = re.findall(pattern, major_response.text)
        pattern_depart = re.compile(r'{.*?}')
        result = re.findall(pattern_depart, num[0])
        expect_result = PopulationSample(self.param).get_major_num()
        self.assertEqual(len(result) - 1, expect_result)

    def test_jiuyeliuxiang(self):
        action = ['jiuyezhuangtailiuxiang','jiuyezhuangtailiuxianggaozhi']
        itemid = ['28','177']
        load_data = {
            'year': str(self.param['year']),
            'universityid': str(self.param['id']),
            'action': action[self.param['level']-1],
            'statisticstype': '1_0',
            'version': '3',
            'itemid': itemid[self.param['level']-1],
            'productid': str(self.param['product']),
            'refproductid': '',
            'userid': '4467',
        }
        major_response = requests.post(url="http://ciadmin.mycos.com//kz/typecompmodel.aspx", params=load_data)
        result_data = json.loads(major_response.text)['data']['res1']
        subjectitem_list = result_data[0]['data']
        subjectitem_text =[]
        #选项是否正确，本科有留学和读研，专科有读
        for subjectitem in subjectitem_list:
            subjectitem_text.append(subjectitem['text'])
        if(self.param['level']==1):
            expectresult = ['正在读研和留学','准备读研和留学']
            if(expectresult[0] in subjectitem_text and expectresult[1] in subjectitem_text ):
                return True
            else:
                self.assertTrue(1)
        if (self.param['level'] == 2):
            expectresult ='毕业后读本科'
            self.assertIn(expectresult,subjectitem_text)
    @classmethod
    def tearDownClass(cls):
        pass
