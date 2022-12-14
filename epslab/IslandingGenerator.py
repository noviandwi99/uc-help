import pandas as pd
import numpy as np
import os

class IslandingGenerator:
    def __init__(self, data_path, filename):
        self.excel_file = pd.ExcelFile(os.path.join(data_path, filename))
        self.filename = filename
        self.data_path = data_path

    def greeting(self):
        print("++++++++++++++++++++++++++++++")
        print("+ GENERATE ISLANDING DATASET +")
        print("++++++++++++++++++++++++++++++\n")

    # Show prompt, to get input from user
    def prompt_user(self):
        self.region_name = input("Region Name: ")
        self.slack_bus = int(input("Slack Bus: "))

        self.number_of_gen = int(input("\nNumber of Generators: "))
        self.generator = list(map(int, input("Input Generator Number\n> ").split(", ")))[:self.number_of_gen]

        self.number_of_bus = int(input("\nNumber of Buses: "))
        self.bus = list(map(int, input("Input Bus Number\n> ").split(", ")))[:self.number_of_bus]

        self.number_of_branch = int(input("\nNumber of Branches: "))
        self.branch = list(map(int, input("Input Branch Number\n> ").split(", ")))[:self.number_of_branch]
    
    # Read excel file from specific sheet
    def read_dataset(self):
        self.standardGenData=pd.read_excel(self.excel_file,'standardGenData')
        self.standardGenData.index += 1
        self.standardGenData=self.standardGenData.loc[self.generator]

        self.costGenData=pd.read_excel(self.excel_file,'costGenData')
        self.costGenData.index += 1
        self.costGenData=self.costGenData.loc[self.generator]

        self.freqRegulationGenData=pd.read_excel(self.excel_file,'freqRegulationGenData')
        self.freqRegulationGenData.index += 1
        self.freqRegulationGenData=self.freqRegulationGenData.loc[self.generator]

        self.continuityGenData=pd.read_excel(self.excel_file,'continuityGenData')
        self.continuityGenData.index += 1
        self.continuityGenData=self.continuityGenData.loc[self.generator]

        self.loadData=pd.read_excel(self.excel_file,'loadData')
        self.powerSun=pd.read_excel(self.excel_file,'powerSun')
        self.powerWind=pd.read_excel(self.excel_file,'powerWind')
        self.SRContingency=pd.read_excel(self.excel_file,'SRContingency')
        self.SRPower=pd.read_excel(self.excel_file,'SRPower')
        self.SRPercentage=pd.read_excel(self.excel_file,'SRPercentage')
        self.busLoad=pd.read_excel(self.excel_file,'busLoad')
        self.busLoad.index += 1
        self.busLoad=self.busLoad.loc[self.bus]

        self.busSun=pd.read_excel(self.excel_file,'busSun')
        self.busSun.index += 1
        self.busSun=self.busSun.loc[self.bus]

        self.busWind=pd.read_excel(self.excel_file,'busWind')
        self.busWind.index += 1
        self.busWind=self.busWind.loc[self.bus]

        self.busData=pd.read_excel(self.excel_file,'busData')
        self.branchData=pd.read_excel(self.excel_file,'branchData')
        self.branchData.index += 1
        self.branchData=self.branchData.loc[self.branch]

        self.batteryData=pd.read_excel(self.excel_file,'batteryData')
        self.phsData=pd.read_excel(self.excel_file,'phsData')
        self.probabilityData=pd.read_excel(self.excel_file,'probabilityData')
        self.mustOnData=pd.read_excel(self.excel_file,'mustOnData')
        self.mustOnData.index += 1
        self.mustOnData=self.mustOnData.loc[self.generator]

        self.mustOffData=pd.read_excel(self.excel_file,'mustOffData')
        self.mustOffData.index += 1
        self.mustOffData=self.mustOffData.loc[self.generator]

        self.reliabilityIndexData=pd.read_excel(self.excel_file,'reliabilityIndexData')
    
    # Calcuate load for each bus type
    def calculate_load(self):
        # Calculate bus load
        self.loadData.loc[0] = self.busLoad.sum()
        # Calculate bus Sun
        self.powerSun.loc[0] = self.busSun.sum()
        # Calculate bus Wind
        self.powerWind.loc[0] = self.busWind.sum()

    # Save to excel for every sheet
    def save_to_excel(self):
        new_filename = self.filename.split(".")[0] + "_" + self.region_name + ".xlsx"
        with pd.ExcelWriter(f"{self.data_path}/{new_filename}") as writer:  
            self.standardGenData.to_excel(writer, index=False, sheet_name='standardGenData')
            self.costGenData.to_excel(writer, index=False, sheet_name='costGenData')
            self.freqRegulationGenData.to_excel(writer, index=False, sheet_name='freqRegulationGenData')
            self.continuityGenData.to_excel(writer, index=False, sheet_name='continuityGenData')
            self.loadData.to_excel(writer, index=False, sheet_name='loadData')
            self.powerSun.to_excel(writer, index=False, sheet_name='powerSun')
            self.powerWind.to_excel(writer, index=False, sheet_name='powerWind')
            self.SRContingency.to_excel(writer, index=False, sheet_name='SRContingency')
            self.SRPower.to_excel(writer, index=False, sheet_name='SRPower')
            self.SRPercentage.to_excel(writer, index=False, sheet_name='SRPercentage')
            self.busLoad.to_excel(writer, index=False, sheet_name='busLoad')
            self.busSun.to_excel(writer, index=False, sheet_name='busSun')
            self.busWind.to_excel(writer, index=False, sheet_name='busWind')
            self.busData.to_excel(writer, index=False, sheet_name='busData')
            self.branchData.to_excel(writer, index=False, sheet_name='branchData')
            self.batteryData.to_excel(writer, index=False, sheet_name='batteryData')
            self.phsData.to_excel(writer, index=False, sheet_name='phsData')
            self.probabilityData.to_excel(writer, index=False, sheet_name='probabilityData')
            self.mustOnData.to_excel(writer, index=False, sheet_name='mustOnData')
            self.mustOffData.to_excel(writer, index=False, sheet_name='mustOffData')
            self.reliabilityIndexData.to_excel(writer, index=False, sheet_name='reliabilityIndexData')

    # This function will reindex bus (start from 1) for every region
    def reindex(self):
        # Before reindex check slackBus correct
        # Correct means slackBus is in the generator list
        if self.slack_bus not in self.standardGenData.loc[:, "Bus Location"].values:
            raise ValueError("Invalid slack bus, slack bus must in generator")
        
        self.busData.loc[0, "slackBus"] = self.bus.index(self.slack_bus) + 1

        # Reindex bus in sheet stanardGenData
        for index, row in self.standardGenData.iterrows():
            if row['Bus Location'] not in self.bus:
                raise ValueError(f"Bus Location: {row['Bus Location']} in sheet standardGenData not found in bus list")
            
            self.standardGenData.loc[index, "Bus Location"] = self.bus.index(row['Bus Location']) + 1
        
        # Reindex bus in sheet branchData
        for index, row in self.branchData.iterrows():
            if row['from'] not in self.bus:
                raise ValueError(f"Bus Location (from): {row['from']} in sheet branchData not found in bus list")
            
            self.branchData.loc[index, "from"] = self.bus.index(row['from']) + 1
        
        for index, row in self.branchData.iterrows():
            if row['to'] not in self.bus:
                raise ValueError(f"Bus Location (to): {row['to']} in sheet branchData not found in bus list")
            
            self.branchData.loc[index, "to"] = self.bus.index(row['to']) + 1

        # Reindex unit and number        
        self.standardGenData.loc[:, "Unit"] = np.arange(1, self.standardGenData.shape[0] + 1)
        self.branchData.loc[:, "number"] = np.arange(1, self.branchData.shape[0] + 1)
        
    def generate(self):
        self.read_dataset()
        self.calculate_load()
        self.reindex()
        self.save_to_excel()