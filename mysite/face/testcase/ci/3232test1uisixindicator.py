#！/usr/bin/env python
#coding:utf-8
import unittest
from selenium import webdriver
import requests
import json.sys
from face.testcase.page.ci import loginPage
from face.testcase.page.ci import displayPage
from face.testcase.dal.populationSample import PopulationSample
__author__ = 'caryr'
class TestUi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        home_page = loginPage(cls.driver)
        home_page.login("tsyxy@test.com","111111")
        cls.page_dis = displayPage(cls.driver)
    def test_jiuyelv(self):
        self.page_dis.select_indicator_by_coordinate(1,1)
        real_result = self.page_dis.get_population_sample()
        expect_result = PopulationSample().get_jiuyelv_sample_count()
        self.assertEqual(real_result,str(expect_result))
    def test_xiaoyoutuijiandu(self):
        self.page_dis = displayPage(self.driver)
        self.page_dis.select_indicator_by_coordinate(2,1)
        real_result = self.page_dis.get_population_sample()
        expect_result = PopulationSample().get_xiaoyoutuijiajiandu_sample_count()
        self.assertEqual(real_result,str(expect_result))
    def test_jiuyeliuxiang(self):
        self.page_dis=displayPage(self.driver)
        self.page_dis.select_indicator_by_coordinate(3,1)
        real_result = self.page_dis.get_population_sample()
        expect_result = PopulationSample().get_jiuyelv_sample_count()
        self.assertEqual(real_result, str(expect_result))
    def test_jiBenNengLiManZuDu(self):
        self.page_dis=displayPage(self.driver)
        self.page_dis.select_indicator_by_coordinate(4,2)
        real_result = self.page_dis.get_population_sample()
        expect_result = PopulationSample().get_nenglimanzu_sample_count()
        self.assertEqual(real_result, str(expect_result))
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
