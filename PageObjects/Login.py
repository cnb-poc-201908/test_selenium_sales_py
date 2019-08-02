'''
Created on Jun 19, 2017

@author: suiyan
'''
from selenium.webdriver.common.by import By
from time import sleep
import base64

class Login(object):
    '''
    classdocs
    '''
    username_location=(By.ID,"UserID")
    userpassword_location=(By.ID,"Password")
    submit_location=(By.CSS_SELECTOR,".ui-button-text")

    def __init__(self, paramWebdriverIns=None,paramLoginUserName=None,paramLoginUserPasswordEnc=None):
        '''
        Constructor
        '''
        self.Webdriverins=paramWebdriverIns
        self.LoginUserName=paramLoginUserName
        self.LoginUserPassEnc=paramLoginUserPasswordEnc
        
    def UserLoginMain(self, strOutputDir=None):
        self.Webdriverins.find_element(*self.username_location).send_keys(self.LoginUserName)
        sleep(3)
        self.Webdriverins.find_element(*self.userpassword_location).send_keys(base64.b64decode(self.LoginUserPassEnc).decode("utf-8"))
        sleep(3)
        self.Webdriverins.save_screenshot(strOutputDir + 'login_beforeClickSubmit.png')
        self.Webdriverins.find_element(*self.submit_location).click()
        sleep(3)
        self.Webdriverins.save_screenshot(strOutputDir + 'login_AfterClickSubmit.png')
        print('login completed.')
        
        
        
    
