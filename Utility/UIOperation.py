'''
@author: IBM suiyandl@cn.ibm.com
'''
import time
import base64
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
from Utility.ReadExcelFile_FirstWorksheet import ExcelFileRead

class UIOperation():
    '''
    classdocs
    '''
    strSubObjectValue=""
    strSubObjectName=""
    strInputValue=""
    
    def __init__(self, listOperations, objWebdriver, outputDirectory, inputFileDirectory):
        '''
        Constructor
        '''
        #initial web driver. Currently we use Firefox as test browser.
        self.driver=objWebdriver
        self.driver.implicitly_wait(30)
          
        self.listOperations=listOperations
        self.outputDirectory=outputDirectory
        self.casefileDirectory=inputFileDirectory
        
        #define action and function mapping for auto invoke.
        self.operationsMap = {'type':self.TypeOnControl,   \
                              'click':self.ClickOnControl, \
                              'typePass':self.TypeOnControlPass, \
                              'assertText':self.AssertTextContent, \
                              'typeEnterKey':self.SendEnterKeysOnControl, \
                              'verifyText':self.VerifyTextContent, \
                              'waitElement':self.WaitUnitElementAvailable, \
                              'verifyTextInput':self.VerifyTextContentInput, \
                              'typePageDownKey':self.SendPageDownKeysOnControl, \
                              'scrollToViewThenClick':self.ScrollToViewThenClickOn, \
                              'verifyIntegerInput':self.VerifyIntegerContentInput, \
                              'assertInterInput':self.AssertIntegerContentInput, \
                              'assertTextInput':self.AssertTextContentInput }
        
        #every customized function will use below various as parameters.
        #self.strAction=""
        #self.strTarget=""
        #self.strValue=""
        self.stepNum=2
    
    #iterate list object and invoke UI operations.
    def IterListAndInvokeUImain(self):
        for strOneAction in self.listOperations:
            print("execute....." + strOneAction)
            self._UIOperationCustomized(strOneAction.split("|")[0],strOneAction.split("|")[1],strOneAction.split("|")[2])
        
    def _UIOperationCustomized(self, strAction, strTarget, strValue):
        #receive one action and map then call corresponding method.
        time.sleep(3)
        if strAction.upper()=="TAKESLEEP":
            time.sleep(int(float(strValue)))
            return
        
        if strAction.upper()=="SCREENSHOT":
            self.driver.save_screenshot(self.outputDirectory + strValue)
            return

        if strAction.upper()=="JUMPOUTOFFRAME":
            self.driver.switch_to.parent_frame()
            return
            
        self.strSubObjectName=strTarget[:strTarget.find("=")]
        self.strSubObjectValue=strTarget[strTarget.find("=")+1:]
        
        if strAction.upper()=="JUMPTOFRAME":
            self.driver.switch_to.frame(self.strSubObjectValue)
            return
        
        self.strInputValue=strValue
        
        #finally we invoke action now..........by operationMap
        self.operationsMap.get(strAction)()
              
    def TypeOnControl(self):
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).clear()
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).send_keys(self.strInputValue)
    
    def TypeOnControlPass(self):
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).send_keys(base64.b64decode(self.strInputValue).decode("utf-8"))
        
    def ClickOnControl(self):
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).click()
        
    def ScrollToViewThenClickOn(self):
        elementA=self.driver.find_element(self.GetByObject(),self.strSubObjectValue)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elementA)
        time.sleep(2)
        elementA.click()
        
    def SendEnterKeysOnControl(self):
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).send_keys(Keys.ENTER)

    def SendPageDownKeysOnControl(self):
        self.driver.find_element(self.GetByObject(),self.strSubObjectValue).send_keys(Keys.PAGE_DOWN)
        
    def WaitUnitElementAvailable(self):
        WebDriverWait(self.driver,15).until(expected_conditions.presence_of_element_located((self.GetByObject(),self.strSubObjectValue)))
        
    def AssertTextContent(self):
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).text
        if strActualValue.strip()!=self.strInputValue.strip():
            print("Expect " + self.strInputValue + ", but actual get " + strActualValue)
            raise AssertionError
        #"Expect " + self.strInputValue + ", but actual get " + strActualValue
    
    def VerifyTextContent(self):    
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).text
        if strActualValue.strip()!=self.strInputValue.strip():
            print("verification error found." + "\nExpect:" + self.strInputValue + "\nBut actual:" + strActualValue)

    def VerifyTextContentInput(self):
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).get_attribute("value")
        if strActualValue.strip()!=self.strInputValue.strip():
            print("verification error found." + "\nExpect:" + self.strInputValue + "\nBut actual:" + strActualValue)
    
    def AssertTextContentInput(self):
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).get_attribute("value")
        if strActualValue.strip()!=self.strInputValue.strip():
            print("Assert error found." + "\nExpect:" + self.strInputValue + "\nBut actual:" + strActualValue)
            raise AssertionError
            
    def VerifyIntegerContentInput(self):    
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).get_attribute("value")
        strActualValue=int(float(strActualValue))
        if strActualValue.strip()!=self.strInputValue.strip():
            print("verification error found." + "\nExpect:" + self.strInputValue + "\nBut actual:" + strActualValue)

    def AssertIntegerContentInput(self):
        strActualValue=self.driver.find_element(self.GetByObject(),self.strSubObjectValue).get_attribute("value")
        strActualValue=int(float(strActualValue))
        if strActualValue!=int(float(self.strInputValue)):
            print("Expect " + self.strInputValue + ", but actual get " + strActualValue)
            raise AssertionError
    
    '''
    GetByObject is to convert all the UI operation description to find_element type.
    '''    
    def GetByObject(self):
        #print(self.strSubObjectName)

        if self.strSubObjectName.upper()=="ID":
            return By.ID
        
        if self.strSubObjectName.upper()=="NAME":
            return By.NAME
        
        if self.strSubObjectName.upper()=="CSS":
            return By.CSS_SELECTOR
        
        if self.strSubObjectName.upper()=="XPATH":
            return By.XPATH
        
if __name__ == "__main__":
    excelInstance=ExcelFileRead()
    excelInstance.open_excel()
    uioperatonIns=UIOperation(excelInstance.read_FirstWorksheet())
    uioperatonIns.IterListAndInvokeUImain()

