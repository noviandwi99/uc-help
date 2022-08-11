import os
from epslab import UC

# File Location
FOLDER_NAME='Islanding B IEEE' #Excel file name
CURRENTPATH=os.getcwd() #alternatively: os.path.dirname(__file__)
DATASET_PATH=os.path.join(CURRENTPATH,'data',FOLDER_NAME)

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
    # 'consFixedSpeedPHS',
    'consIslanding'
]

# initiate
theCase=UC(
    case_name="Islanding B IEEE",
    constraint=constraints,
    data_path=DATASET_PATH,
    data_type="EXCEL"
)

theCase.run_simulation()