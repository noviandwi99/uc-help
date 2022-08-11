import pandas as pd
import os

def excel2csv(excel_path, csv_path):
    # #Input Path
    # currentPath=os.getcwd()
    # excel_path=os.path.join(currentPath,PATH)

    # #Output Path
    # csv_path=os.path.join(currentPath,PATH)
    # if not os.path.isdir(csv_path):
    #     os.mkdir(csv_path)

    #ListDir
    dirList=os.listdir(excel_path)

    for fileName in dirList:
        #readXLSX
        thisPath=os.path.join(excel_path,fileName)
        excelFile=pd.ExcelFile(thisPath)

        #Sheet List
        sheetList=excelFile.sheet_names
        
        #subFolderOutputPath
        fileName=fileName.replace('.xlsx','')
        fileName=fileName.replace('.xls','')
        subFolderOutputPath=os.path.join(csv_path,fileName)
        if not os.path.isdir(subFolderOutputPath):
            os.mkdir(subFolderOutputPath)

        for sheetName in sheetList:
            thisDataFrame=pd.read_excel(excelFile,sheetName)
            thisDataFrame.to_csv(os.path.join(subFolderOutputPath,sheetName+'.csv'),index=False)
