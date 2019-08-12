'''
@author: IBM
'''
import unittest
from selenium import webdriver
from Utility.HTMLTestRunner import HTMLTestRunner
from Utility.UIOperation import UIOperation
from Utility.ReadExcelFile_FirstWorksheet import ExcelFileRead

import time

class Test(unittest.TestCase):

    def setUp(self):
        
        #to accept untrusted connection warning.
        #self.FirefoxProfile=webdriver.FirefoxProfile()
        #self.FirefoxProfile.default_preferences["webdriver_assume_untrusted_issuer"] = 'false'
        #self.firefoxWebdriver=webdriver.Firefox(self.FirefoxProfile)
        #self.firefoxWebdriver=webdriver.Firefox()
        self.firefoxWebdriver=webdriver.Chrome()
        self.firefoxWebdriver.get("https://cn.bing.com")
        time.sleep(3)


    def tearDown(self):
        pass
        #self.firefoxWebdriver.quit()

    def testThisone(self):
        print("begin testing")
        readExcelIns=ExcelFileRead()
        readExcelIns.open_excel()
        UIoperationIns=UIOperation(readExcelIns.read_FirstWorksheet(),self.firefoxWebdriver)
        UIoperationIns.IterListAndInvokeUImain()


if __name__ == "__main__":
    suite=unittest.TestSuite()
    suite.addTest(Test("testThisone"))
    fp=open('/home/anakin/Desktop/abcdefg.html','wb')
    runner=HTMLTestRunner(stream=fp)
    #runner=unittest.TextTestRunner()
    runner.run(suite)
    fp.close()

    
