#！/usr/bin/env python
#coding:utf-8
from openpyxl import  load_workbook
import os
__author__ = 'caryr'
def get_information():
    '''返回一个列表，一个字典元素代表一个学校'''
    filepath = (os.path.abspath('../../../uploadfile/ci.xlsx')) + "/information/university.xlsx"
    filepath = None

