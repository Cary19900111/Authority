#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
class loginPage(object):
    def __init__(self,driver):
        self._driver = driver
        self._driver.get("http://ci.mycos.com/Login.aspx")
        self.username = self._driver.find_element_by_id("txtuid")
        self.password = self._driver.find_element_by_id("txtpwd")
        self.login_button = self._driver.find_element_by_id("btnlogin")
    def login(self,name,password):
        self.username.send_keys(name)
        self.password.send_keys(password)
        self.login_button.click()