import os
from epslab import UC

# File Location
inputFolderName='Islanding B IEEE' #Excel file name

# Constraints used (you can comment unused constraints)
constraints=[
    'consUC',
    'consModeOptimOnlyMILP',
    'consStairwiseCost',
    'consPiecewiseCost',
     'consSRContingency',
    'consMUTMDT',
    'consBasicRamp',
     #'consInit',
    #'consMustOn',
    #'consMustOff',
    'consWorstCaseInertia', #Primary cons will be included, but simplified (max(Pgen) assumed to be max(Pmax))
    'consPrimaryDroop', #Primary cons with Minimum Frequency Steady State requirement
    'consDCPF',
    #'consCongestionPr',
     #'consToP',
     #'consRegionTransfer',
     #'consHydroThermalCoordination',
    #'consBatteryAsLoadLeveling',
     #'consBatteryAsPVDummyLoad', #underdevelopment
    #'consBatteryAsReserve',
    # 'consPHS',
    # 'consRPrPHS',
    # 'consSCRPHS',
    # 'consFixedSpeedPHS'
]

# initiate
theCase=UC()

# enter constraints list
theCase.inputCons(constraints)

# enter folder data path
CURRENTPATH=os.getcwd() #alternatively: os.path.dirname(__file__)
PATH=os.path.join(CURRENTPATH,'data',inputFolderName)
theCase.inputDataPath(PATH) # folder path, not file path

# Problem Formulation
theCase.makeProblem()

# Print Problem Parameters
theCase.printIndex()
theCase.printNumberOfData()

# Run
theCase.run_UC()

# Print Output
theCase.printOutput()
theCase.partialCost(decimal_place=4)
theCase.getSummaryDic(print_summary_dic=True)
theCase.exportToCSV(name_mark=False)