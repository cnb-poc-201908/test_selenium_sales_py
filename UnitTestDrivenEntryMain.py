'''
@author: suiyan
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from Utility.HTMLTestRunner import HTMLTestRunner
from Utility.UIOperation import UIOperation
from Utility.ReadExcelFile_FirstWorksheet import ExcelFileRead
from Utility.LoadConfigureXml import LoadConfigureXml
from Utility.RuntimeWorkingDirectoryCreation import RuntimeWorkingDirectoryCreation
from Utility.FailFlag import FailFlag

from PageObjects.Login import Login

import time
import unittest
import argparse
#import datetime
import sys
#import os

class Test(unittest.TestCase):

    #def __init__(self,argURL,argInputTestCase, argOutputFile):
    #    self.TargetURL=argURL
        
    def __init__(self, methodName='runTest', paramTestCaseFilename=None, paramTestURL=None,paramOutputDir=None, \
                 paramUserName=None,paramUserPass=None, paraResultFlag=None):
        super(Test, self).__init__(methodName)
        self.paramTestCaseFilenameMember = paramTestCaseFilename
        self.paramURLMember=paramTestURL

        #output directory specified in xml configuration file.
        self.paramOutputDirMember=paramOutputDir

        #Generated output result directory.
        self.OutputDirectory=""
        
        self.UserName=paramUserName
        self.UserPass=paramUserPass
        
        self.ResultFlagIns=paraResultFlag
                 
    @staticmethod
    def parametrize(testcase_class, paramTestCaseFilename=None,paramTestURL=None,paramOutputMainDir=None,   \
                    paramUserName=None,paramUserPass=None,paraResultFlag=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'. 
        """  
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name, paramTestCaseFilename=paramTestCaseFilename, \
                                        paramTestURL=paramTestURL, paramOutputDir=paramOutputMainDir, \
                                        paramUserName=paramUserName,paramUserPass=paramUserPass, \
                                        paraResultFlag=paraResultFlag))
        return suite
      
    def setUp(self):
        
        print("\n\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++  BEGIN  +++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

        #create working directory under output main directory
        runtimeWorkingDirIns=RuntimeWorkingDirectoryCreation(self.paramOutputDirMember,self.paramTestCaseFilenameMember)
        runtimeWorkingDirIns.CreateDirectoryByCurrentDatetime()
        self.OutputDirectory=runtimeWorkingDirIns.GetRuntimeOutputDirectory()
        self.firefoxWebdriver=webdriver.Remote(command_executor='http://10.244.2.34:5555/wd/hub',desired_capabilities={'browserName': 'chrome'})
        #print('anakin here')
        #self.firefoxWebdriver=webdriver.Chrome()
        self.firefoxWebdriver.get(self.paramURLMember)
        self.firefoxWebdriver.maximize_window()
        self.firefoxWebdriver.implicitly_wait(20)
        time.sleep(3)
        
    def tearDown(self):
        #pass
        self.firefoxWebdriver.quit()
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++  COMPLETE  ++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Result:")

class TestSuiteScenario(Test):
    
    def test_Smoke(self):
        try:
            LoginIns= Login(self.firefoxWebdriver,self.UserName,self.UserPass)
            LoginIns.UserLoginMain(self.OutputDirectory)
        
            #for get directory from test case file name, for 
            strFileName=self.paramTestCaseFilenameMember
            print('Scenario file:',strFileName)
            strRealFileName=strFileName.split("/")[-1]
            print("execute senario : " + self.paramTestCaseFilenameMember)

            readExcelIns=ExcelFileRead()
            readExcelIns.open_excel(self.paramTestCaseFilenameMember)
            UIoperationIns=UIOperation(readExcelIns.read_FirstWorksheet(),self.firefoxWebdriver,self.OutputDirectory, strFileName[0:len(strFileName)-len(strRealFileName)])
            #print('anakin, before iterate actions.')
            UIoperationIns.IterListAndInvokeUImain()
        except NoSuchElementException:
            print("NoSuchElementException found.....")
            self.ResultFlagIns.SetFlagToFalse()
        except AssertionError:
            print("Assertion error found.....")
            self.ResultFlagIns.SetFlagToFalse()
        except Exception as ee:
            print(ee)
            print("Other exceptions found in....." + self.paramTestCaseFilenameMember)
            self.ResultFlagIns.SetFlagToFalse()        

if __name__ == "__main__":

    #create command line argument entry.
    parser = argparse.ArgumentParser()
    parser.add_argument('-suitename',dest="suiteTarget",action='store',
                        help='use -suitename option to specify target suite name.')
    parser.add_argument('-env',nargs='?',dest="envTarget",action='store',default='PROD')
    
    args = parser.parse_args()
    print('args:',args.suiteTarget)

    #load configuration file.
    LoadConfigureXmlIns=LoadConfigureXml(r'./Automation-Configuration.xml',args.suiteTarget, args.envTarget)
    
    #corresponding suite name not found, exit -1
    if LoadConfigureXmlIns.ParsexmlMain()==False:
        exit(-1)
    
    ffIns=FailFlag()

    #begin to create test suite and waiting for add.
    suite = unittest.TestSuite()
    
    for oneTestcase in LoadConfigureXmlIns.getlistTargetTestdataFile():
        suite.addTest(Test.parametrize(TestSuiteScenario, paramTestCaseFilename=oneTestcase, \
                                           paramTestURL=LoadConfigureXmlIns.getTargetURL(), \
                                           paramOutputMainDir=LoadConfigureXmlIns.getOutputdirectory(), \
                                           paramUserName=LoadConfigureXmlIns.getLoginUserName(), \
                                           paramUserPass=LoadConfigureXmlIns.getLoginUserPass(),paraResultFlag=ffIns))

    unittest.TextTestRunner(verbosity=2).run(suite)
    
    if ffIns.GetFlag()==False:
        sys.exit(-1)

    '''''
    #output to html begin *******************
    strTimeStap=str(datetime.datetime.now())
    strTimeStap=strTimeStap[:len(strTimeStap)-7]
    strTimeStap=strTimeStap.replace('-', '')
    strTimeStap=strTimeStap.replace(' ', '')
    strTimeStap=strTimeStap.replace(':', '')
    strHtmlReportFileName=os.getcwd() + '/ExecutionOutput/testReport.html'
    fp=open(strHtmlReportFileName,'wb')
    runner=HTMLTestRunner(stream=fp)
    runner.run(suite)
    fp.close()
    print("\nRefer to the html report file for result: "  + strHtmlReportFileName)
    #output to html end *******************
    '''''
