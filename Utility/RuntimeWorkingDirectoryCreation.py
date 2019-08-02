'''
@author: suiyan
'''
import datetime
import os

class RuntimeWorkingDirectoryCreation(object):
    '''
    classdocs
    '''
    def __init__(self, params_outputMainDirectory, params_excelFileName=r'../TestData/dataDriven_sample.xlsx'):
        '''
        Constructor
        '''
        self.mainExecutionDirectory=params_outputMainDirectory
        self.outputDirectoryExcelnamePart=params_excelFileName
        self.runtimeOutputDirectory=""
        
    def CreateDirectoryByCurrentDatetime(self):
        
        #get current date time and output format YYYYMMDDHHMMSS
        strTimeStap=str(datetime.datetime.now())
        strTimeStap=strTimeStap[:len(strTimeStap)-7]
        strTimeStap=strTimeStap.replace('-', '')
        strTimeStap=strTimeStap.replace(' ', '')
        strTimeStap=strTimeStap.replace(':', '')
        
        strFilename=""
        fileNameAllpartTemp=self.outputDirectoryExcelnamePart.split("/")
        for onePart in fileNameAllpartTemp:
            strFilename=onePart
        
        self.runtimeOutputDirectory=str(self.mainExecutionDirectory) + strTimeStap + strFilename[:len(strFilename)-5]
        os.mkdir(self.runtimeOutputDirectory)
        
        
    def GetRuntimeOutputDirectory(self):
        return self.runtimeOutputDirectory + "/"
        
        
if __name__ == "__main__":
    runIns=RuntimeWorkingDirectoryCreation("/home/anakin/Desktop/BMWpocTest/ExecutionOutput/")
    runIns.CreateDirectoryByCurrentDatetime()
    print(runIns.GetRuntimeOutputDirectory())
    
    
