'''
@author: suiyan
'''
import xml.etree.ElementTree
import os

class LoadConfigureXml(object):
    '''
    classdocs
    '''
    def __init__(self, filenameXml=r'./Automation-Configuration.xml',ParaStrTargetSuite="", ParaStrEnvTarget=""):
        '''
        Constructor
        '''
        self.xmlHandleRoot = xml.etree.ElementTree.parse(filenameXml).getroot()
        
        #target suite to fetch.
        self.targetSuite=ParaStrTargetSuite
        
        self.targetEnv=ParaStrEnvTarget
        
        #fetch content from configuration XML.
        self.listTargetTestdataFile=[]
        self.targetURL=""
        self.outputMainDirectory=""
        self.loginUsername=""
        self.loginUserpass=""
        
        #whether find target suite in configuration XML.
        self.boolFindTargetSuite=False
        
    def getTargetURL(self):
        return self.targetURL
        
    def getlistTargetTestdataFile(self):
        return self.listTargetTestdataFile
    
    def getOutputdirectory(self):    
        return self.outputMainDirectory
    
    def getLoginUserName(self):
        return self.loginUsername
    
    def getLoginUserPass(self):
        return self.loginUserpass
        
    def ParsexmlMain(self):
        
        if self.targetSuite==None:
            return False
        
        #get target test data file name list. (currently not implement directory find.)
        targetExeSuite=self.xmlHandleRoot.getiterator("TestExecutionSuite")
        
        for oneSuite in targetExeSuite:
            #find matched suite name.
            if oneSuite.get('name').upper()==self.targetSuite.upper():
                self.boolFindTargetSuite=True
                
                #if this is a directory information.
                if oneSuite.get('repositoryType').upper()=="FILEDIRECTORY":
                    targetDirectory=oneSuite.find("./TestCaseExecutionTarget").text
                    for filename in os.listdir(targetDirectory):
                        if filename[-5:]==".xlsx":
                            self.listTargetTestdataFile.append(targetDirectory + filename)
                #in case file list specified.        
                if oneSuite.get('repositoryType').upper()=="FILENAMELIST":
                    #get file list directly.
                    iterfileList=oneSuite.getiterator("TestCaseExecutionTarget")
                    for oneFile in iterfileList:
                        self.listTargetTestdataFile.append(oneFile.text)
        
        #get system URL and output directory from XML.
        if self.targetEnv=="UAT":
            self.targetURL=self.xmlHandleRoot.find("./TestEnvironment/WebSystemURL_UAT").text
        elif self.targetEnv=="DEV":
            self.targetURL=self.xmlHandleRoot.find("./TestEnvironment/WebSystemURL_DEV").text
        else:
            self.targetURL=self.xmlHandleRoot.find("./TestEnvironment/WebSystemURL_PROD").text
        
        self.outputMainDirectory=self.xmlHandleRoot.find("./TestCaseExecutionOutputDirectory").text
        
        self.loginUsername=self.xmlHandleRoot.find("./TestEnvironment/LoginUserName").text
        self.loginUserpass=self.xmlHandleRoot.find("./TestEnvironment/LoginUserPasswordDes").text
        
        #create output main directory if does not exist.
        if (os.path.exists(self.outputMainDirectory) and os.path.isdir(self.outputMainDirectory))==False:
            os.mkdir(self.outputMainDirectory)
        
        return self.boolFindTargetSuite
    
    
if __name__ == "__main__":
    LoadConfigureXmlIns=LoadConfigureXml(r'../Automation-Configuration.xml',"touchTest")
    LoadConfigureXmlIns.ParsexmlMain()
    print(LoadConfigureXmlIns.getlistTargetTestdataFile())
    print(LoadConfigureXmlIns.getOutputdirectory())
    print(LoadConfigureXmlIns.getTargetURL())
    
