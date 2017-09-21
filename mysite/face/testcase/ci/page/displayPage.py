#！/usr/bin/env python
#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import re
__author__ = 'caryr'
class displayPage(object):
    def __init__(self,driver):
        self._driver = driver
        self.list = self._driver.find_element_by_id("nav")
        #定位大类别指标,并初始化
        self.big_index_lists_p = self.list.find_elements_by_css_selector("p[class^=title]")
        self.big_index_lists_p[0].click()
        #定位小类指标列表
        self.big_index_lists_div = self.list.find_elements_by_css_selector("div[class^=list]")

    def select_indicator_by_coordinate(self,x,y):
        '''如果y=0，则表示只点击最大分类的列表,y>0表示点击具体的指标'''
        if not(self.big_index_lists_p[x-1].get_attribute("class")=='title on'):
            self.big_index_lists_p[x-1].click()
        if(y>0):
            obj_y = WebDriverWait(self.big_index_lists_div[x-1],10).until(lambda x:x.find_elements_by_css_selector("p")[y-1])
        #obj_y.click()
        #self.big_index_lists_div[x-1].find_elements_by_css_selector("p")[y-1].click()
    def close_indicator_by_coordinate(self,x):
        if (self.big_index_lists_p[x-1].get_attribute("class")=='title  on'):
            self.big_index_lists_p[x-1].click()
    def get_n_indicator_text_list(self,x):
        self.select_indicator_by_coordinate(x,0)
        indicator_p = self.big_index_lists_div[x-1].find_elements_by_css_selector("p")
        text_list = []
        for text_p in indicator_p:
            text_list.append(text_p.text)
        return text_list
    def get_population_sample(self):
        sample_count_span = self._driver.find_element_by_id("showSampleSizeTextOn0Left").text
        sample_pattern = re.compile(r"n=(\d*)")
        sample_count = sample_pattern.findall(sample_count_span)[0]
        return sample_count


