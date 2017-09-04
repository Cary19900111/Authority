#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
import unittest,os,HTMLTestRunner
from datetime import datetime
def test_ci_all_case(filename):
    try:
        abs_path = os.path.abspath('.')
        test_dir = abs_path + r'\face\testcase\ci'
        HtmlFile = r'{abs_path}\face\testcase\result\{filename}'.format(abs_path=abs_path, filename=filename)
        testunit = unittest.TestSuite()
        discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py',
                                                       top_level_dir=None)  # 返回多个suite，一个文件是一个suite
        for test_suite in discover:  # 得到一个suite
            for test_case in test_suite:  # 得到一个case
                testunit.addTests(test_case)
        fp = open(HtmlFile, "wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"TestReport", description=u"CI测试报告")
        runner.run(testunit)
        fp.close()
    except Exception as err:
        print(err)
if __name__ == '__main__':
    test_ci_all_case("123")