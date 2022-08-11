import os
from epslab import UC

# File Location
inputFolderName='Simulasi IEEE no BESS2' #Excel file name

# Constraints used (you can comment unused constraints)
constraints=[
    'consUC',
    'consModeOptimOnlyMILP',
    'consStairwiseCost',
    'consPiecewiseCost', 
    # 'consModePiecewiseNaive', #Assume piece gradient gradually increase for faster computation
    'consSRContingency',
    # 'consSRPower',
    # 'consSRPercentage', #Percentage of demand at t
    # 'consModeSRNaive', #Ignore RampSecondary and CostSR for faster computation
    'consMUTMDT',
    'consBasicRamp',
    # 'consAdvancedRamp', #After and before off: PGEN == PMIN
    # 'consInit',
    # 'consMustOn',
    # 'consMustOff',
    'consWorstCaseInertia', #Primary cons will be included, but simplified (max(Pgen) assumed to be max(Pmax))
    'consPrimaryDroop' #Primary cons with Minimum Frequency Steady State requirement
    # 'consSteadyPrimFreq', #More strict than consWorstCaseInertia
    'consDCPF',
    # 'consModePowerFlowCost',#under development
    # 'consBatteryAsLoadLeveling',
    # 'consBatteryAsPVDummyLoad', #underdevelopment
    # 'consBatteryAsReserve',
    # 'consPHS',
    # 'consOptimumPVPlcament', #under development
    # 'consPVPlacementConstraints', #under development
    # 'consAllowLoadShedding',
    # 'consAllowSRViolation',
    # 'consAllowDummyLoadForTML',
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