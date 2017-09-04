#！/usr/bin/env python
#coding:utf-8
import unittest
from selenium import webdriver
import requests
import json

__author__ = 'caryr'
#@unittest.skip("test2")
class Testjiuyelv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    def test_department_count(self):
        department_load_data = {
            'year': '2016',
            "universityid": "1435",
            "action": 'jiuyelv',
            "statisticstype": '2_0-104-7-2-14-101-5-4-9-6-11-102-103-12',
            "version": '3',
            "itemid": '4',
            "productid": '1',
            "refproductid": '',
            "userid": '7261',
        }
        department_response = requests.post(url="http://ciadmin.mycos.com//kz/typecompmodel.aspx", params=department_load_data)
        department_num = len(json.loads(department_response.text)['data']['res1'])
        self.assertEqual(department_num,14)
    def test_major_count(self):
        major_load_data = {
            "year": "2016",
            "version": '3',
            "userid": '7261',
            "universityid": '1435',
            "statisticstype": '3_0-071201-050202-080204-110302-100701-10070110-081101-081001-080605-100307-100401-110303-100301-10030114-100397-110206-110205-030302-081801-070402-080607-081899-110202-100202-080609-110102-100801-10080102-100304-100303-10030336-070302-07020210-050201-100201-040204-081102-100802',
            "refproductid": '',
            "productid": '1',
            "itemid": '4',
            "action": 'jiuyelv',
        }
        major_response = requests.post(url="http://ciadmin.mycos.com//kz/typecompmodel.aspx", params=major_load_data)
        major_num = len(json.loads(major_response.text)['data']['res1'])
        print(major_num)
        self.assertEqual(major_num,39)
    @classmethod
    def tearDownClass(cls):
        pass
