'''

@author: IBM
'''
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import base64

class Login(object):
    '''
    classdocs
    '''
    username_location=(By.XPATH,"/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/app-login/ion-content/div[2]/form/ion-item[1]/ion-input/input")
    userpassword_location=(By.XPATH,"/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/app-login/ion-content/div[2]/form/ion-item[2]/ion-input/input")
    submit_location=(By.XPATH,"/html/body/app-root/ion-app/ion-split-pane/ion-router-outlet/app-login/ion-content/div[2]/div[2]/ion-button")

    def __init__(self, paramWebdriverIns=None,paramLoginUserName=None,paramLoginUserPasswordEnc=None):
        '''
        Constructor
        '''
        self.Webdriverins=paramWebdriverIns
        self.LoginUserName=paramLoginUserName
        self.LoginUserPassEnc=paramLoginUserPasswordEnc
        
    def UserLoginMain(self, strOutputDir=None):
        self.Webdriverins.save_screenshot(strOutputDir + '0_beforeUsername.png')
        self.Webdriverins.find_element(*self.username_location).send_keys(self.LoginUserName)
        sleep(3)
        self.Webdriverins.find_element(*self.userpassword_location).send_keys(base64.b64decode(self.LoginUserPassEnc).decode("utf-8"))
        sleep(3)
        self.Webdriverins.save_screenshot(strOutputDir + '0_login_AfterInput.png')
        self.Webdriverins.find_element(*self.submit_location).click()
        sleep(3)
        self.Webdriverins.save_screenshot(strOutputDir + '1_login_AfterClickSubmit.png')
        print('login completed.')
