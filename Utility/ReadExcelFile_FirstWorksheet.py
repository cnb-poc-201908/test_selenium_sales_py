'''
Created on Apr 17, 2017

@author: suiyan
'''
import xlrd
from xlrd.book import Book

class ExcelFileRead():
    #initial the split character for saving user operatoins.
    def __init__(self):
        self.SPLITCHAR="|"
        self.bookIns=Book()
        
    #open one excel test case file to load.
    def open_excel(self, fileName=r'../TestData/dataDriven_sample.xlsx'):
        try:
            #read workbook file into various excelFile.
            self.bookIns = xlrd.open_workbook(fileName)
            return True
        except Exception:
            print("Exception when open excel file " + fileName)
            return False
    
    
    #read first work sheet of test case and save actions into list.
    def read_FirstWorksheet(self):
        self.firstWorksheet=self.bookIns.sheet_by_index(0)
        self.listOperation=[]    #use this list as repository of use's behaviors described in test case.  
        #user operation description should begin from row 2 in excel. please refer to test case
        for self.iIterRow in range(1, self.firstWorksheet.nrows):
            #one string maps one action, append into list.
            self.listOperation.append(self.firstWorksheet.cell(self.iIterRow,1).value + self.SPLITCHAR + \
                                      self.firstWorksheet.cell(self.iIterRow,2).value + self.SPLITCHAR + \
                                      str(self.firstWorksheet.cell(self.iIterRow,3).value) )
        return self.listOperation
    
    def TestIterationList(self):
        #print(len(self.listOperation))
        #print(self.listOperation)
        for oneAction in self.listOperation:
            print(oneAction)

            
if __name__ == "__main__":
    excelInstance=ExcelFileRead()
    if excelInstance.open_excel()==False:
        print("error happened.")
    else:
        excelInstance.read_FirstWorksheet()
        excelInstance.TestIterationList()
                
