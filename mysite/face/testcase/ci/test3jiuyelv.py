#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
import unittest
from selenium import webdriver
import requests
import json
__author__ = 'caryr'
#@unittest.skip("test3")
class jiuyelv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    def test_jiuyelv_department(self):
        major_load_data = {
            "year": "2016",
            "version": '3',
            "userid": '7261',
            "universityid": '1435',
            "statisticstype": '2_7',
            "refproductid": '',
            "productid": '1',
            "itemid": '4',
            "action": 'jiuyelv',
        }
        department_response = requests.post(url="http://ciadmin.mycos.com//kz/typecompmodel.aspx", params=major_load_data)
        count = json.loads(department_response.text)['data']['res1'][0]['data'][0]['value']
        self.assertEqual(count,'240-253')
    def test_jiuyelv_department_another(self):
        major_load_data = {
            "year": "2016",
            "version": '3',
            "userid": '7261',
            "universityid": '1435',
            "statisticstype": '2_7',
            "refproductid": '',
            "productid": '1',
            "itemid": '4',
            "action": 'jiuyelv',
        }
        department_response = requests.post(url="http://ciadmin.mycos.com//kz/typecompmodel.aspx", params=major_load_data)
        count = json.loads(department_response.text)['data']['res1'][0]['data'][0]['value']
        self.assertEqual(count,'240-253')
    @classmethod
    def tearDownClass(cls):
        pass