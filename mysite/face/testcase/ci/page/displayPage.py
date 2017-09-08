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
        self.big_index_lists_p = self.list.find_elements_by_css_selector("p[class^=title]")
        self.big_index_lists_div = self.list.find_elements_by_css_selector("div[class^=list]")

    def select_indicator_by_coordinate(self,x,y):
        if not(self.big_index_lists_p[x-1].get_attribute("class")=='title  on'):
            self.big_index_lists_p[x-1].click()
        obj_y = WebDriverWait(self.big_index_lists_div[x-1],10).until(lambda x:x.find_elements_by_css_selector("p")[y-1])
        #self.big_index_lists_div[x-1].find_elements_by_css_selector("p")[y-1].click()
    def get_n_indicator_text(self,x):
        pass
    def get_population_sample(self):
        sample_count_span = self._driver.find_element_by_id("showSampleSizeTextOn0Left").text
        sample_pattern = re.compile(r"n=(\d*)")
        sample_count = sample_pattern.findall(sample_count_span)[0]
        return sample_count


