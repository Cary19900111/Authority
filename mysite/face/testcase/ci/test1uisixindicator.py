#！/usr/bin/env python
#coding:utf-8
import unittest,sys
# print(sys.path)
# sys.path.append('.')
# print(sys.path)
from selenium import webdriver
import sys,time
from openpyxl import load_workbook
from ..ci.common.ParaTestCase import ParametrizedTestCase
from .dal.populationSample import PopulationSample
from .page.displayPage import displayPage
__author__ = 'caryr'
#@unittest.skip("test1")
class TestUi(ParametrizedTestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.driver = webdriver.Chrome()
            cls.driver.implicitly_wait(5)
            cls.driver.get("http://ci.mycos.com/Login.aspx")
            cls.username = cls.driver.find_element_by_id("txtuid")
            cls.password = cls.driver.find_element_by_id("txtpwd")
            cls.login_button = cls.driver.find_element_by_id("btnlogin")
            # cls.username.send_keys(cls.param['account'])
            # cls.password.send_keys(cls.param['password'])
            cls.username.send_keys(cls.para['account'])
            cls.password.send_keys(cls.para['password'])
            cls.login_button.click()
            # home_page = loginPage(cls.driver)
            #home_page.login("tsyxy@test.com","111111")
            cls.page_dis = displayPage(cls.driver)
            cls.db = PopulationSample(cls.para)
        except Exception as err:
            cls.assertLogs(err)

    def test_jiuyelv(self):
        #self.assertEqual(3, 4)
        try:
            self.page_dis.select_indicator_by_coordinate(1,1)
            real_result = self.page_dis.get_population_sample()
            expect_result = self.db.get_jiuyelv_sample_count()
            self.assertEqual(real_result,str(expect_result))
        except Exception as err:
            self.assertLogs(err)

    def test_xiaoyoutuijiandu(self):
        #self.assertEqual(4, 4)
        self.page_dis = displayPage(self.driver)
        self.page_dis.select_indicator_by_coordinate(2,1)
        real_result = self.page_dis.get_population_sample()
        expect_result = self.db.get_xiaoyoutuijiajiandu_sample_count()
        self.assertEqual(real_result,str(expect_result))


    def test_not_display_three(self):
        #速度太快
        self.page_dis = displayPage(self.driver)
        self.page_dis.select_indicator_by_coordinate(1,0)
        xianzhuangmanyidu_list = self.page_dis.get_n_indicator_text_list(1)
        self.page_dis.close_indicator_by_coordinate(1)
        self.page_dis.select_indicator_by_coordinate(3,0)
        #速度太快会导致列表读为空
        time.sleep(2)
        zhiyelei_list = self.page_dis.get_n_indicator_text_list(3)
        self.page_dis.close_indicator_by_coordinate(3)
        print(xianzhuangmanyidu_list)
        print(zhiyelei_list)
        if("现状满意度" in xianzhuangmanyidu_list and "职业类流向" in zhiyelei_list and  "行业类流向" in zhiyelei_list):
            self.assertEqual(1,2)
        self.assertEqual(1,1)
    # def test_jiuyeliuxiang(self):
    #     #self.assertEqual(6, 6)
    #     self.page_dis=displayPage(self.driver)
    #     self.page_dis.select_indicator_by_coordinate(3,1)
    #     real_result = self.page_dis.get_population_sample()
    #     expect_result = PopulationSample().get_jiuyelv_sample_count()
    #     #self.assertEqual(real_result, str(expect_result))
    #     self.assertEqual(real_result, '2546')
    # def test_jiBenNengLiManZuDu(self):
    #     #self.assertEqual(4, 7)
    #     self.page_dis=displayPage(self.driver)
    #     self.page_dis.select_indicator_by_coordinate(4,2)
    #     real_result = self.page_dis.get_population_sample()
    #     expect_result = PopulationSample().get_nenglimanzu_sample_count()
    #     self.assertEqual(real_result, str(expect_result))
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
