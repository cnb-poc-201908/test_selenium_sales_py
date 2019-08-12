'''
@author: IBM suiyandl@cn.ibm.com
'''

class FailFlag(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.bIsOk=True
    
    def SetFlagToFalse(self): 
        self.bIsOk=False 
        
    def GetFlag(self):
        return self.bIsOk
    
class TestFail(object):
    
    def __init__(self, ffInstance):
        self.ffInst=ffInstance
    
    def LetMeChage(self):
        self.ffInst.SetFlagToFalse()
        
        
if __name__ == "__main__":
    ffIns=FailFlag()
    
    TestFailIns=TestFail(ffIns)
    TestFailIns.LetMeChage()
    
    if ffIns.GetFlag()==True:
        print("ok")
    else:
        print("fail")
        
