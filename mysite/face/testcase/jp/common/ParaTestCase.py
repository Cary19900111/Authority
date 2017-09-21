#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
import unittest
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    #这个设置为类属性,用self和cls都可以访问
    para = {}
    def __init__(self,methodName='runTest',param=None):
        #super(ParametrizedTestCase, self).__init__(methodName)
        #为什么一定要加methodName
        unittest.TestCase.__init__(self,methodName)
        #self.param = param
        ParametrizedTestCase.para = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        # runner.run(test_suite)
        # suite1 = unittest.TestLoader().loadTestsFromTestCase(testcase_klass)
        # #suite2 = unittest.TestLoader().loadTestsFromTestCase(TestHello)
        # suite = unittest.TestSuite([suite1])
        # unittest.TextTestRunner(verbosity=2).run(suite)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite