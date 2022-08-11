import numpy as np
import cplex
import pandas as pd
import os
import datetime
import copy
from . import DatasetType

## Main Function ##
class UC:
	"""Make Matrices necessary for cplex."""
	def __init__(self, case_name, constraint, data_path, data_type):
		self.tic=datetime.datetime.now()
		self.caseName=case_name
		self.globalVar()

		self.data_type = data_type
		if self.data_type == "EXCEL":
			self.valid_extension = [".xlsx"]
		elif self.data_type == "CSV":
			self.valid_extension = [".csv"]

		# enter constraints list
		self.inputCons(constraint)
		
		# enter folder data path
		self.inputDataPath(data_path)
	
	def run_simulation(self):
		if 'consIslanding' in self.consList:
			for data in self.dataList:
				self.prepare_dataset(data)
				self.run_UC()
		else:
			self.prepare_dataset()
			self.run_UC()

	def inputDataPath(self,dataPath):
		self.dataPath=dataPath

		# Get Dataset
		self.dataList = []
		for val in os.listdir(self.dataPath):
			file_extension = os.path.splitext(val)[1]

			if file_extension in self.valid_extension:
				self.dataList.append(val)
	
	def prepare_dataset(self, data):
		if self.data_type == "EXCEL":
			file_path = os.path.join(self.dataPath, data)
			self.excelFile=pd.ExcelFile(file_path)
			self.sheet_names = self.excelFile.sheet_names
			
			self.inputDataExcel()
		elif self.data_type == "CSV":
			for i in range(len(self.dataList)):
				self.dataList[i]=self.dataList[i].replace('.csv','')
			
			self.inputDataCSV()

	def getPath(self,name_mark=False):
		#Make Output Folder
		currentPath=os.getcwd()
		if name_mark==True:
			self.name_mark=self.tic.strftime("%y")+self.tic.strftime("%m")+self.tic.strftime("%d")+'_'+self.tic.strftime("%H")+self.tic.strftime("%M")
		else:
			self.name_mark=''
		self.outputPath=os.path.join(currentPath,'result\\result_'+self.caseName+'_'+self.name_mark)
		pass

	def globalVar(self):
		global UN_YM,BL_YM,PMAX_YM,PMIN_YM,RU_YM,RD_YM,MUT_YM,MDT_YM,HS_YM,QHP_YM,AHP_YM,BHP_YM,TOP_YM,\
				MD_YM,P1_YM,P2_YM,P3_YM,P4_YM,P5_YM,P6_YM,F1_YM,F2_YM,F3_YM,F4_YM,\
				F5_YM,F6_YM,M1_YM,M2_YM,M3_YM,M4_YM,M5_YM,ACOST_YM,BCOST_YM,CCOST_YM,\
				HSCOST_YM,CSCOST_YM,SRCOST_YM,SDCOST_YM,HT_YM,\
				IS_YM,UT_YM,DT_YM,IP_YM,LS_YM,MF_YM,\
				PRCOST_YM,TRCOST_YM,FDMIN_YM,FNOM_YM,RPMAX_YM,RSRMAX_YM,RTMAX_YM,RAGC_YM,\
				DRPERC_YM,DRMWHZ_YM,FDSS_YM,SB_YM,BMVA_YM,BN_YM,FROM_YM,TO_YM,R_YM,X_YM,LCAP_YM,REG_YM,\
				BID_YM,BBL_YM,SOCMAX_YM,SOCMIN_YM,CRMAX_YM,DRMAX_YM,BCEFF_YM,BDEFF_YM,ISOC_YM,FSOC_YM,RSTMIN_YM,DRMAXRS_YM,TRES_YM,\
				PID_YM,PBL_YM,URMAX_YM,URMIN_YM,PPMIN_YM,PPMAX_YM,PGMIN_YM,PGMAX_YM,PPEFF_YM,PGEFF_YM,IUR_YM,FUR_YM,PDMAX_YM,GDMAX_YM,PH_YM,G_YM,WD_YM,PRCOSTPHS_YM,RPRMAX_YM,PHSIN_YM,PHSGR_YM,FDEAD_YM,DPS_YM,DSS_YM,RUMAX_YM,\
				PROBLIST_YM,VOLL_YM,EENSMAX_YM,SRPENALTY_YM,INERTIA_YM,FDB_YM,RGOV_YM,\
				PVID_YM,PVLOC_YM,PVCAP_MY,PVCOST_YM,\
				PVPROMIN_YM,PVPROMAX_YM,PVINSCAPMIN_YM,PVINSCAPMAX_YM

		# standardGenData
		# [UN_YM,BL_YM,PMAX_YM,PMIN_YM,RU_YM,RD_YM,MUT_YM,MDT_YM]=range(8)
		[UN_YM,BL_YM,PMAX_YM,PMIN_YM,RU_YM,RD_YM,MUT_YM,MDT_YM,HS_YM,QHP_YM,AHP_YM,BHP_YM,TOP_YM]=range(13)

		#cost Gen Data
		[MD_YM,HSCOST_YM,CSCOST_YM,HT_YM,SDCOST_YM,P1_YM,P2_YM,P3_YM,P4_YM,P5_YM,P6_YM,F1_YM,F2_YM,F3_YM,F4_YM,\
			F5_YM,F6_YM,M1_YM,M2_YM,M3_YM,M4_YM,M5_YM,ACOST_YM,BCOST_YM,CCOST_YM]=range(25)
		
		# continuityGenData
		[IP_YM,IS_YM,UT_YM,DT_YM]=range(4)

		# timeDependentPowerLimitGenData
		[LS_YM,MF_YM]=range(2)

		# freqRegulationGenData
		[PRCOST_YM,SRCOST_YM,TRCOST_YM,FDMIN_YM,FNOM_YM,RPMAX_YM,RSRMAX_YM,RTMAX_YM,RAGC_YM,\
			DRPERC_YM,DRMWHZ_YM,INERTIA_YM,FDB_YM,RGOV_YM,FDSS_YM]=range(15)
		
		# busData
		[SB_YM,BMVA_YM]=range(2)

		# branchData
		[BN_YM,FROM_YM,TO_YM,R_YM,X_YM,LCAP_YM,REG_YM]=range(7)

		# batteryData
		[BID_YM,BBL_YM,SOCMAX_YM,SOCMIN_YM,CRMAX_YM,DRMAX_YM,BCEFF_YM,BDEFF_YM,ISOC_YM,FSOC_YM,RSTMIN_YM,DRMAXRS_YM,TRES_YM]=range(13)

		# phsData
		# [PID_YM,PBL_YM,URMAX_YM,URMIN_YM,PRMIN_YM,PPMAX_YM,GRMIN_YM,PGMAX_YM,PPEFF_YM,PGEFF_YM,IUR_YM,FUR_YM,PDMAX_YM,GDMAX_YM,PH_YM,G_YM,WD_YM,MRU_YM]=range(18)
		# [PID_YM,PBL_YM,URMAX_YM,URMIN_YM,PPMAX_YM,PGMAX_YM,PPEFF_YM,PGEFF_YM,IUR_YM,FUR_YM,PDMAX_YM,GDMAX_YM,PH_YM,G_YM,WD_YM]=range(15)
		[PID_YM,PBL_YM,URMAX_YM,URMIN_YM,PPMIN_YM,PPMAX_YM,PGMIN_YM,PGMAX_YM,PPEFF_YM,PGEFF_YM,IUR_YM,FUR_YM,PDMAX_YM,GDMAX_YM,PH_YM,G_YM,WD_YM,PRCOSTPHS_YM,RPRMAX_YM,PHSIN_YM,PHSGR_YM,FDEAD_YM,DPS_YM,DSS_YM,RUMAX_YM]=range(25)

		# probabilityData
		[PROBLIST_YM]=range(1)

		# reliabilityData
		[VOLL_YM,EENSMAX_YM,SRPENALTY_YM]=range(3)

		# PVCandidate
		[PVID_YM,PVLOC_YM,PVCAP_MY,PVCOST_YM]=range(4)

		# PVPlacementConstraints
		[PVPROMIN_YM,PVPROMAX_YM,PVINSCAPMIN_YM,PVINSCAPMAX_YM]=range(4)

		global dim1,dim2,dim3
		[dim1,dim2,dim3]=range(3)

		global epsilonNumber
		epsilonNumber=1/cplex.infinity

	def inputDataExcel(self):
		for sheetName in self.sheet_names:
			if sheetName=='standardGenData':
				self.standardGenData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='costGenData':
				self.costGenData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='freqRegulationGenData':
				self.freqRegulationGenData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='continuityGenData':
				self.continuityGenData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='loadData':
				self.loadData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='powerSun':
				self.powerSun=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='powerWind':
				self.powerWind=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='SRContingency':
				self.SRContingency=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='SRPower':
				self.SRPower=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='SRPercentage':
				self.SRPercentage=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='busLoad':
				self.busLoad=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='busSun':
				self.busSun=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='busWind':
				self.busWind=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='busData':
				self.busData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='branchData':
				self.branchData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='batteryData':
				self.batteryData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='phsData':
				self.phsData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()	
			elif sheetName=='probabilityData':
				self.probabilityData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='mustOnData':
				self.mustOnData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='mustOffData':
				self.mustOffData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
			elif sheetName=='reliabilityIndexData':
				self.reliabilityIndexData=(pd.read_excel(self.excelFile,sheetName)).to_numpy()
	
	def inputDataCSV(self):
		for csvName in self.dataList:
			if csvName=='standardGenData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.standardGenData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='costGenData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.costGenData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='freqRegulationGenData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.freqRegulationGenData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='continuityGenData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.continuityGenData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='loadData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.loadData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='powerSun':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.powerSun=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='powerWind':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.powerWind=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='SRContingency':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.SRContingency=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='SRPower':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.SRPower=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='SRPercentage':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.SRPercentage=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='busLoad':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.busLoad=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='busSun':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.busSun=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='busWind':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.busWind=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='busData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.busData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='branchData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.branchData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='batteryData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.batteryData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='phsData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.phsData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='probabilityData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.probabilityData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='mustOnData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.mustOnData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='mustOffData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.mustOffData=(pd.read_csv(thisPath)).to_numpy()
			elif csvName=='reliabilityIndexData':
				thisPath=os.path.join(self.dataPath,csvName+'.csv')
				self.reliabilityIndexData=(pd.read_csv(thisPath)).to_numpy()
		pass
	
	def inputData(self,data_name,np_arr):
		if type(np_arr).__module__ == np.__name__:
			pass
		elif type(np_arr) == list:
			np_arr=np.array(np_arr)
			pass
		elif isinstance(np_arr, pd.DataFrame):
			np_arr=np_arr.to_numpy()
		else:
			print('Input Data Unrecognized')
			return

		if data_name=='standardGenData':
			self.standardGenData=np_arr
		elif data_name=='costGenData':
			self.costGenData=np_arr
		elif data_name=='freqRegulationGenData':
			self.freqRegulationGenData=np_arr
		elif data_name=='continuityGenData':
			self.continuityGenData=np_arr
		elif data_name=='loadData':
			self.loadData=np_arr
		elif data_name=='powerSun':
			self.powerSun=np_arr
		elif data_name=='powerWind':
			self.powerWind=np_arr
		elif data_name=='SRContingency':
			self.SRContingency=np_arr
		elif data_name=='SRPower':
			self.SRPower=np_arr
		elif data_name=='SRPercentage':
			self.SRPercentage=np_arr
		elif data_name=='busLoad':
			self.busLoad=np_arr
		elif data_name=='busSun':
			self.busSun=np_arr
		elif data_name=='busWind':
			self.busWind=np_arr
		elif data_name=='busData':
			self.busData=np_arr
		elif data_name=='branchData':
			self.branchData=np_arr
		elif data_name=='batteryData':
			self.batteryData=np_arr
		elif data_name=='phsData':
			self.phsData=np_arr
		elif data_name=='probabilityData':
			self.probabilityData=np_arr
		elif data_name=='mustOnData':
			self.mustOnData=np_arr
		elif data_name=='mustOffData':
			self.mustOffData=np_arr
		elif data_name=='reliabilityIndexData':
			self.reliabilityIndexData=np_arr
		else:
			print('Input Name Unrecognized')
			return

		pass

	def inputCons(self,consList):
		self.consList=consList
		pass

	def inputCaseName(self,caseName):
		self.caseName=caseName
		pass

	def makeProblem(self):
	## initial ##
		self.numberOfGen=np.shape(self.standardGenData)[dim1]
		[self.numberOfState,self.numberOfTime]=np.atleast_2d(self.loadData).shape
		self.probList=self.probabilityData[:,PROBLIST_YM].astype(float).tolist()

		self.latestIdx=0
		
		self.A=[]
		self.b=[]
		self.senses=''
		self.objVar=[]
		self.lbVar=[]
		self.ubVar=[]
		self.typesVar=''
		self.qmat=[]

		T=self.numberOfTime
		G=self.numberOfGen
		S=self.numberOfState
		# print('T:',T)
		# print('G',G)
		# print('S',S)
	#------------------------------------------------------------------------------#
	## Set Variable ##
		if 'consUC' in self.consList:
			self.idxUC=self.latestIdx #Unit Commitment
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime
			self.idxSD=self.latestIdx #Shutdown
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime
			self.idxSU=self.latestIdx #Startup
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime
			self.idxPGen=self.latestIdx #Power Generation
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime*self.numberOfState
			
			self.numberOfVar=self.latestIdx

			idxUC=self.idxUC
			idxSD=self.idxSD
			idxSU=self.idxSU
			idxPGen=self.idxPGen
		
			fuelCostA=self.costGenData[:,ACOST_YM].astype(float).tolist()
			fuelCostB=self.costGenData[:,BCOST_YM].astype(float).tolist()
			fuelCostC=self.costGenData[:,CCOST_YM].astype(float).tolist()
			startupCost=self.costGenData[:,CSCOST_YM].astype(float).tolist()

			if 'consPiecewiseCost' in self.consList:
				self.numberOfPiece=(P6_YM-P1_YM) #piece between point 6-1, 5 piece
				Piece=self.numberOfPiece
				
				self.idxPPieceGen=self.latestIdx #Power Generation in Piece Wise
				self.latestIdx=self.latestIdx+self.numberOfPiece*self.numberOfGen*self.numberOfTime*self.numberOfState
				
				self.numberOfVar=self.latestIdx
				idxPPieceGen=self.idxPPieceGen

				fuelCostMode=self.costGenData[:,MD_YM].astype(int).tolist() #Mode, 0: Piecewise F, 1: Piecewise M, 2: Quadratic
				fuelCostPiecePower=self.costGenData[:,P1_YM:P6_YM+1].astype(float).tolist() #6 points
				fuelCostPieceDollar=self.costGenData[:,F1_YM:F6_YM+1].astype(float).tolist() #6 points (note that first and second F use first M)
				
				self.idxPPieceFlag=self.latestIdx #Piece Flag Status, 1 if used and 0 if not
				self.latestIdx=self.latestIdx+self.numberOfPiece*self.numberOfGen*self.numberOfTime*self.numberOfState
				self.numberOfVar=self.latestIdx
				idxPPieceFlag=self.idxPPieceFlag

				#gradient cost ()
				fuelCostM=[]
				for g in range(G):
					i=fuelCostMode[g]
					if i == 0: #use picewise F
						fuelCostA[g]=0 #zeroed
						fuelCostB[g]=0 #zeroed
						fuelCostC[g]=self.costGenData[g,F1_YM].tolist()
						for p in range(Piece):
							if fuelCostPiecePower[g][p]==fuelCostPiecePower[g][p+1]:
								fuelCostM.extend([0])
								pass
							else:
								gradienTemp=(fuelCostPieceDollar[g][p]-fuelCostPieceDollar[g][p+1])/(fuelCostPiecePower[g][p]-fuelCostPiecePower[g][p+1])
								fuelCostM.extend([gradienTemp])
								pass
						pass

					if i == 1: #use picewise M
						fuelCostA[g]=0 #zeroed
						fuelCostB[g]=0 #zeroed
						fuelCostC[g]=self.costGenData[g,F1_YM].tolist()
						fuelCostM.extend(self.costGenData[g,M1_YM:M5_YM+1].astype(float).tolist()) #5 gradien
						pass

					if i == 2: #use quadratic
						fuelCostM.extend([0]*Piece)
						pass
				
				#piece width
				pieceWidth=[]
				for g in range(G):
					for p in range(Piece):
						pieceWidth.extend([fuelCostPiecePower[g][p+1]-fuelCostPiecePower[g][p]])
			if 'consStairwiseCost' in self.consList:
				self.idxCountDown=self.latestIdx #Counting Current Down Duration
				self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime
				self.idxHS=self.latestIdx #Counting Current Down Duration
				self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime
				self.idxCS=self.latestIdx #Counting Current Down Duration
				self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime

				self.numberOfVar=self.latestIdx
				
				idxCountDown=self.idxCountDown
				idxHS=self.idxHS
				idxCS=self.idxCS

				startupCost=[0]*G
				startupCostHot=self.costGenData[:,HSCOST_YM].astype(float).tolist()
				startupCostCold=self.costGenData[:,CSCOST_YM].astype(float).tolist()

			#objVar
			self.objVar.extend(fuelCostC*T) #UC
			self.objVar.extend(self.costGenData[:,SDCOST_YM].tolist()*T) #SD
			self.objVar.extend(startupCost*T) #SU ~ 0 if use stairwise
			for probMultiplier in self.probList:
				self.objVar.extend((np.array(fuelCostB*T)*probMultiplier).tolist()) #PGEN (np.array(a)*3).tolist()

			#lbVar
			self.lbVar.extend([0]*G*T) #UC
			self.lbVar.extend([0]*G*T) #SD
			self.lbVar.extend([0]*G*T) #SU
			self.lbVar.extend([0]*G*T*S) #PGEN
			
			#ubVar
			self.ubVar.extend([1]*G*T) #UC
			self.ubVar.extend([1]*G*T) #SD
			self.ubVar.extend([1]*G*T) #SU
			self.ubVar.extend(self.standardGenData[:,PMAX_YM].tolist()*T*S) #PGEN ~ maxcap
			#typesVar
			for i in range(G*T): #UC
				self.typesVar+='B'
			for i in range(G*T): #SD
				self.typesVar+='B'
			for i in range(G*T): #SU
				self.typesVar+='B'
			for i in range(G*T*S): #PGEN
				self.typesVar+='C'

			#qmat
			for i in range(idxUC,idxUC+G*T):
				self.qmat.append([[0],[0]])
			for i in range(idxSD,idxSD+G*T):
				self.qmat.append([[0],[0]])
			for i in range(idxSU,idxSU+G*T):
				self.qmat.append([[0],[0]])
			for s,probMultiplier in zip(range(S),self.probList):
				for i,j in zip(range(idxPGen+s*G*T,idxPGen+(s+1)*G*T),(fuelCostA*T)):
					self.qmat.append([[i],[2*j*probMultiplier]])
			
			#compile for output
			self.fuelCostA=fuelCostA
			self.fuelCostB=fuelCostB
			self.fuelCostC=fuelCostC
			self.shutDownCost=self.costGenData[:,SDCOST_YM].tolist() 

			if 'consPiecewiseCost' in self.consList:
				for probMultiplier in self.probList:
					self.objVar.extend((np.array(fuelCostM*T)*probMultiplier).tolist()) #PPICEGEN
				self.lbVar.extend([0]*Piece*G*T*S) #PPICEGEN
				self.ubVar.extend(pieceWidth*T*S) #PPICEGEN
				for i in range(Piece*G*T*S): #PPICEGEN
					self.typesVar+='C'
				for i in range(idxPPieceGen,idxPPieceGen+Piece*G*T*S):
					self.qmat.append([[0],[0]])
				self.fuelCostM=fuelCostM
			
				self.objVar.extend([0]*Piece*G*T*S) #PPICEFLAG
				self.lbVar.extend([0]*Piece*G*T*S) #PPICEFLAG
				self.ubVar.extend([1]*Piece*G*T*S) #PPICEFLAG
				for i in range(Piece*G*T*S): #PPICEFLAG
					self.typesVar+='B'
				for i in range(idxPPieceFlag,idxPPieceFlag+Piece*G*T*S):
					self.qmat.append([[0],[0]])
				pass
			if 'consStairwiseCost' in self.consList:
				self.objVar.extend([0]*G*T) #countDown
				self.objVar.extend(startupCostHot*T) #hotStart
				self.objVar.extend(startupCostCold*T) #coldStart
				self.lbVar.extend([0]*G*T)
				self.lbVar.extend([0]*G*T)
				self.lbVar.extend([0]*G*T)
				self.ubVar.extend([cplex.infinity]*G*T)
				self.ubVar.extend([1]*G*T)
				self.ubVar.extend([1]*G*T)
				for i in range(G*T):
					self.typesVar+='I'
				for i in range(G*T):
					self.typesVar+='B'
				for i in range(G*T):
					self.typesVar+='B'
				for i in range(idxCountDown,idxCountDown+G*T):
					self.qmat.append([[0],[0]])
				for i in range(idxHS,idxHS+G*T):
					self.qmat.append([[0],[0]])
				for i in range(idxCS,idxCS+G*T):
					self.qmat.append([[0],[0]])
				self.startupCostHot=startupCostHot
				self.startupCostCold=startupCostCold
				pass
			
			self.startupCost=startupCost
			#debug
			# print('obj:',len(self.objVar))
			# print('lbVar:',len(self.lbVar))
			# print('ubVar:',len(self.ubVar))
			# print('type:',len(self.typesVar))
			# print(fuelCostA)
			# print('qmat Matrices:',self.qmat)

		if 'consWorstCaseInertia' in self.consList:
			self.idxRPr=self.latestIdx #Scheduled Steady Primary Frequency Reserve
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime*self.numberOfState
			self.numberOfVar=self.latestIdx
			idxRPr=self.idxRPr
			for probMultiplier in self.probList:
				self.objVar.extend((self.freqRegulationGenData[:,PRCOST_YM]*probMultiplier).tolist()*T) #RPr
			self.lbVar.extend([0]*G*T*S) #RPr
			self.ubVar.extend(self.freqRegulationGenData[:,RPMAX_YM].tolist()*T*S) #RPr
			for i in range(G*T*S):
				self.typesVar+='C' #RPr
			for i in range(idxRPr,idxRPr+G*T*S): #RPr
				self.qmat.append([[0],[0]])
			self.SteadyPrimaryReserveCost=self.freqRegulationGenData[:,PRCOST_YM].tolist()
		if 'consWorstCaseInertia' in self.consList:
			pass
		
		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			self.idxRSR=self.latestIdx #Scheduled Steady Primary Frequency Reserve
			self.latestIdx=self.latestIdx+self.numberOfGen*self.numberOfTime*self.numberOfState

			self.numberOfVar=self.latestIdx

			idxRSR=self.idxRSR

			for probMultiplier in self.probList:
				self.objVar.extend((self.freqRegulationGenData[:,SRCOST_YM]*probMultiplier).tolist()*T) #RSR
				
			self.lbVar.extend([0]*G*T*S) #RSR

			self.ubVar.extend(self.freqRegulationGenData[:,RSRMAX_YM].tolist()*T*S) #RSR

			for i in range(G*T*S):
				self.typesVar+='C' #RSR

			for i in range(idxRSR,idxRSR+G*T*S):
				self.qmat.append([[0],[0]])

			self.secondaryReserveCost=self.freqRegulationGenData[:,SRCOST_YM].tolist()
		if 'consDCPF' in self.consList:
			self.numberOfBus=np.shape(self.busLoad)[dim1]
			print("ANJIR 1", self.numberOfBus)
			self.numberOfBranch=np.shape(self.branchData)[dim1]

			Bus=self.numberOfBus
			Branch=self.numberOfBranch

			self.idxPBus=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBus*self.numberOfTime*self.numberOfState
			self.idxTheta=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBus*self.numberOfTime*self.numberOfState
			self.idxLineLoad=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBranch*self.numberOfTime*self.numberOfState
			
			self.numberOfVar=self.latestIdx

			idxPBus=self.idxPBus
			idxTheta=self.idxTheta
			idxLineLoad=self.idxLineLoad
			
			self.objVar.extend([0]*Bus*T*S) #PBus
			self.objVar.extend([0]*Bus*T*S) #Theta
			self.objVar.extend([0]*Branch*T*S) #LineLoad
			self.lbVar.extend([-1*cplex.infinity]*Bus*T*S) #PBus
			self.lbVar.extend([-1*cplex.infinity]*Bus*T*S) #Theta
			self.lbVar.extend((-1*self.branchData[:,LCAP_YM]).tolist()*T*S) #LineLoad
			self.ubVar.extend([cplex.infinity]*Bus*T*S) #PBus
			self.ubVar.extend([cplex.infinity]*Bus*T*S) #Theta
			self.ubVar.extend(self.branchData[:,LCAP_YM].tolist()*T*S) #LineLoad

			for i in range(Bus*T*S):
				self.typesVar+='C' #PBus
			for i in range(Bus*T*S):
				self.typesVar+='C' #Theta
			for i in range(Branch*T*S):
				self.typesVar+='C' #LineLoad

			for i in range(idxPBus,idxPBus+Bus*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxTheta,idxTheta+Bus*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxLineLoad,idxLineLoad+Branch*T*S):
				self.qmat.append([[0],[0]])

		if 'consCongestionPr' in self.consList:
			self.numberOfBus=np.shape(self.busLoad)[dim1]
			self.numberOfBranch=np.shape(self.branchData)[dim1]

			Bus=self.numberOfBus
			Branch=self.numberOfBranch

			self.idxPBusPr=self.latestIdx
			self.latestIdx=self.latestIdx+self.numberOfBus*self.numberOfTime*self.numberOfState
			self.idxThetaPr=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBus*self.numberOfTime*self.numberOfState
			self.idxLineLoadPr=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBranch*self.numberOfTime*self.numberOfState

			self.numberOfVar=self.latestIdx

			idxPBusPr=self.idxPBusPr
			idxThetaPr=self.idxThetaPr
			idxLineLoadPr=self.idxLineLoadPr

			self.objVar.extend([0]*Bus*T*S) #PBusPr
			self.objVar.extend([0]*Bus*T*S) #ThetaPr
			self.objVar.extend([0]*Branch*T*S) #LineLoadPr
			self.lbVar.extend([-1*cplex.infinity]*Bus*T*S) #PBusPr
			self.lbVar.extend([-1*cplex.infinity]*Bus*T*S) #ThetaPr
			# self.lbVar.extend((-1*self.branchData[:,LCAP_YM]).tolist()*T*S) #LineLoadPr
			self.lbVar.extend([-1*cplex.infinity]*Branch*T*S) #LineLoadPrTanpaKekangan
			self.ubVar.extend([cplex.infinity]*Bus*T*S) #PBusPr
			self.ubVar.extend([cplex.infinity]*Bus*T*S) #ThetaPr
			# self.ubVar.extend(self.branchData[:,LCAP_YM].tolist()*T*S) #LineLoadPr
			self.ubVar.extend([1*cplex.infinity]*Branch*T*S) #LineLoadPrTanpaKekangan

			for i in range(Bus*T*S):
				self.typesVar+='C' #PBusPr
			for i in range(Bus*T*S):
				self.typesVar+='C' #ThetaPr
			for i in range(Branch*T*S):
				self.typesVar+='C' #LineLoadPr

			for i in range(idxPBusPr,idxPBusPr+Bus*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxThetaPr,idxThetaPr+Bus*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxLineLoadPr,idxLineLoadPr+Branch*T*S):
				self.qmat.append([[0],[0]])

		if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad','consBatteryAsReserve'] for i in self.consList):
			self.numberOfBattery=np.shape(self.batteryData[:,BID_YM].astype(int).tolist())[dim1]
			
			Battery=self.numberOfBattery

			self.idxChargeStatus=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime
			self.idxDischargeStatus=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime
			self.idxChargePower=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState
			self.idxDischargePower=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState
			self.idxSOC=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState
			self.idxSOCPrev=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState
			# self.idxRSt=self.latestIdx
			# self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState
			
			self.numberOfVar=self.latestIdx

			idxChargeStatus=self.idxChargeStatus
			idxDischargeStatus=self.idxDischargeStatus
			idxChargePower=self.idxChargePower
			idxDischargePower=self.idxDischargePower
			idxSOC=self.idxSOC
			idxSOCPrev=self.idxSOCPrev
			# idxSTr=self.idcSTr

			self.objVar.extend([0]*Battery*T) #chargeStatus
			self.objVar.extend([0]*Battery*T) #dischargeStatus
			self.objVar.extend([0]*Battery*T*S) #chargePower
			self.objVar.extend([0]*Battery*T*S) #discharePower
			self.objVar.extend([0]*Battery*T*S) #self.SOC
			self.objVar.extend([0]*Battery*T*S) #self.SOC(t-1)
			self.lbVar.extend([0]*Battery*T) #chargeStatus
			self.lbVar.extend([0]*Battery*T) #dischargeStatus
			self.lbVar.extend([0]*Battery*T*S) #chargePower
			self.lbVar.extend([0]*Battery*T*S) #discharePower
			self.lbVar.extend(self.batteryData[:,SOCMIN_YM].astype(float).tolist()*T*S) #self.SOC
			self.lbVar.extend(self.batteryData[:,SOCMIN_YM].astype(float).tolist()*T*S) #self.SOC(t-1)
			self.ubVar.extend([1]*Battery*T) #chargeStatus
			self.ubVar.extend([1]*Battery*T) #dischargeStatus
			self.ubVar.extend(self.batteryData[:,CRMAX_YM].astype(float).tolist()*T*S) #chargePower
			self.ubVar.extend(self.batteryData[:,DRMAX_YM].astype(float).tolist()*T*S) #discharePower
			self.ubVar.extend(self.batteryData[:,SOCMAX_YM].astype(float).tolist()*T*S) #self.SOC
			self.ubVar.extend(self.batteryData[:,SOCMAX_YM].astype(float).tolist()*T*S) #self.SOC(t-1)
			
			for i in range(Battery*T):
				self.typesVar+='B'
			for i in range(Battery*T):
				self.typesVar+='B'
			for i in range(Battery*T*S):
				self.typesVar+='C'
			for i in range(Battery*T*S):
				self.typesVar+='C'
			for i in range(Battery*T*S):
				self.typesVar+='C'
			for i in range(Battery*T*S):
				self.typesVar+='C'
			
			for i in range(idxChargeStatus,idxChargeStatus+Battery*T):
				self.qmat.append([[0],[0]])
			for i in range(idxDischargeStatus,idxDischargeStatus+Battery*T):
				self.qmat.append([[0],[0]])
			for i in range(idxChargePower,idxChargePower+Battery*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxDischargePower,idxDischargePower+Battery*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxSOC,idxSOC+Battery*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxSOCPrev,idxSOCPrev+Battery*T*S):
				self.qmat.append([[0],[0]])
		if 'consBatteryAsPVDummyLoad' in self.consList:
			self.idxPVU=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfTime*self.numberOfState
			self.idxChargePowerFromPV=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState

			self.numberOfVar=self.latestIdx

			idxPVU=self.idxPVU
			idxChargePowerFromPV=self.idxChargePowerFromPV

			self.objVar.extend([0]*T*S) #PVU
			self.objVar.extend([0]*Battery*T*S) #ChargePowerFromPV
			self.lbVar.extend([0]*T*S) #PVU
			self.lbVar.extend([0]*Battery*T*S) #ChargePowerFromPV
			self.ubVar.extend([cplex.infinity]*T*S) #PVU
			self.ubVar.extend(self.batteryData[:,CRMAX_YM].astype(float).tolist()*T*S)#ChargePowerFromPV

			for i in range(T*S): #PVU
				self.typesVar+='C'
			for i in range(Battery*T*S): #ChargePowerFromPV 
				self.typesVar+='C'
			
			for i in range(idxPVU,idxPVU+T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxChargePowerFromPV,idxChargePowerFromPV+Battery*T*S):
				self.qmat.append([[0],[0]])

		if 'consBatteryAsReserve' in self.consList:
			self.idxRSt=self.latestIdx
			self.latestIdx=self.latestIdx+self.numberOfBattery*self.numberOfTime*self.numberOfState			

			self.numberOfVar=self.latestIdx

			idxRSt=self.idxRSt

			self.objVar.extend([0]*Battery*T*S) #RSt
			self.lbVar.extend([0]*Battery*T*S) #RSt
			self.ubVar.extend([1*cplex.infinity]*Battery*T*S) #RSt

			for i in range(Battery*T*S): #RSt
				self.typesVar+='C'
			
			for i in range(idxRSt,idxRSt+Battery*T*S):
				self.qmat.append([[0],[0]])
				
			#debug
			# print(self.powerSun[0,:])
			# print(self.objVar,len(self.objVar))
			# print(self.lbVar,len(self.lbVar))
			# print(self.ubVar,len(self.ubVar))
			# print(self.typesVar,len(self.typesVar))
			# print(self.qmat,len(self.qmat))
		if 'consPHS' in self.consList:			
			self.numberOfPHS=np.shape(self.phsData[:,PID_YM].astype(int).tolist())[dim1]

			PHS=self.numberOfPHS

			self.idxPumpStatus=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime
			self.idxGenerateStatus=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime
			self.idxPumpPower=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			self.idxGeneratePower=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			self.idxUR=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			self.idxURPrev=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			self.idxSCRPHSG=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			self.idxSCRPHSP=self.latestIdx 
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState

			self.numberOfVar=self.latestIdx

			idxPumpStatus=self.idxPumpStatus
			idxGenerateStatus=self.idxGenerateStatus
			idxPumpPower=self.idxPumpPower
			idxGeneratePower=self.idxGeneratePower
			idxUR=self.idxUR
			idxURPrev=self.idxURPrev
			idxSCRPHSG=self.idxSCRPHSG
			idxSCRPHSP=self.idxSCRPHSP

			self.objVar.extend([0]*PHS*T) #pumpStatus
			self.objVar.extend([0]*PHS*T) #generateStatus
			self.objVar.extend([0]*PHS*T*S) #pumpPower
			self.objVar.extend([0]*PHS*T*S) #generatePower
			self.objVar.extend([0]*PHS*T*S) #self.UR
			self.objVar.extend([0]*PHS*T*S) #self.UR(t-1)
			# for probMultiplier in self.probList:
			# 	self.objVar.extend((self.phsData[:,PRCOSTPHS_YM]*probMultiplier).tolist()*T) #RPr
			self.objVar.extend([0]*PHS*T*S) #self.SCRPHSG
			self.objVar.extend([0]*PHS*T*S) #self.SCRPHSP
			self.lbVar.extend([0]*PHS*T) #pumpStatus
			self.lbVar.extend([0]*PHS*T) #generateStatus
			self.lbVar.extend([0]*PHS*T*S) #pumpPower
			self.lbVar.extend([0]*PHS*T*S) #generatePower
			self.lbVar.extend(self.phsData[:,URMIN_YM].astype(float).tolist()*T*S) #self.UR
			self.lbVar.extend(self.phsData[:,URMIN_YM].astype(float).tolist()*T*S) #self.UR(t-1)
			self.lbVar.extend([0]*PHS*T*S) #SCRPHSG
			self.lbVar.extend([0]*PHS*T*S) #SCRPHSP
			self.ubVar.extend([1]*PHS*T) #pumpStatus
			self.ubVar.extend([1]*PHS*T) #generateStatus
			self.ubVar.extend(self.phsData[:,PPMAX_YM].astype(float).tolist()*T*S) #pumpPower
			self.ubVar.extend(self.phsData[:,PGMAX_YM].astype(float).tolist()*T*S) #generatePower
			self.ubVar.extend(self.phsData[:,URMAX_YM].astype(float).tolist()*T*S) #self.UR
			self.ubVar.extend(self.phsData[:,URMAX_YM].astype(float).tolist()*T*S) #self.UR(t-1)
			self.ubVar.extend(self.phsData[:,RUMAX_YM].astype(float).tolist()*T*S) #SCRPHSG
			self.ubVar.extend(self.phsData[:,RUMAX_YM].astype(float).tolist()*T*S) #SCRPHSP
			
			for i in range(PHS*T):
				self.typesVar+='B'
			for i in range(PHS*T):
				self.typesVar+='B'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			for i in range(PHS*T*S):
				self.typesVar+='C'
			
			for i in range(idxPumpStatus,idxPumpStatus+PHS*T):
				self.qmat.append([[0],[0]])
			for i in range(idxGenerateStatus,idxGenerateStatus+PHS*T):
				self.qmat.append([[0],[0]])
			for i in range(idxPumpPower,idxPumpPower+PHS*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxGeneratePower,idxGeneratePower+PHS*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxUR,idxUR+PHS*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxURPrev,idxURPrev+PHS*T*S):
				self.qmat.append([[0],[0]])
			
			for i in range(idxSCRPHSG,idxSCRPHSG+PHS*T*S):
				self.qmat.append([[0],[0]])
			for i in range(idxSCRPHSP,idxSCRPHSP+PHS*T*S):
				self.qmat.append([[0],[0]])

		if 'consRPrPHS' in self.consList:
			self.numberOfPHS=np.shape(self.phsData[:,PID_YM].astype(int).tolist())[dim1]

			self.idxRPrPHS=self.latestIdx
			self.latestIdx=self.latestIdx+self.numberOfPHS*self.numberOfTime*self.numberOfState
			
			self.numberOfVar=self.latestIdx

			idxRPrPHS=self.idxRPrPHS

			self.objVar.extend([0]*PHS*T*S) #RPrPHS
			self.lbVar.extend([0]*PHS*T*S) #RPrPHS
			self.ubVar.extend(self.phsData[:,RPRMAX_YM].astype(float).tolist()*T*S) #RPr
			for i in range(PHS*T*S):
				self.typesVar+='C' #RPrPHS
			for i in range(idxRPrPHS,idxRPrPHS+PHS*T*S): #RPrPHS
				self.qmat.append([[0],[0]])

	#------------------------------------------------------------------------------#
	## Set Matrices ##
		# Basic UC Constraintss
		# print('Daftar Kekangan', self.consList)
		if 'consUC' in self.consList:
			# relation between Startup, Shutdown, and Status considering initial Status            
			for t in range(T):
				if t==0:
					if 'consInit' in self.consList:
						initStatus=self.continuityGenData[:,IS_YM].tolist()
						self.initStatus=initStatus
						for g in range(G):
							self.A.append([[idxUC+t*G+g,idxSD+t*G+g,idxSU+t*G+g],[-1,-1,1]])
							self.b.extend([initStatus[g]*-1])
							self.senses+='E'
				else:
					for g in range(G):
						self.A.append([[idxUC+(t-1)*G+g,idxUC+t*G+g,idxSD+t*G+g,idxSU+t*G+g],[1,-1,-1,1]])
						self.b.extend([0])
						self.senses+='E'

			# Unit cannot be Startup and Shutdown simultaneously
			for t in range(T):
				for g in range(G):
					self.A.append([[idxSD+t*G+g,idxSU+t*G+g],[1,1]])
					self.b.extend([1])
					self.senses+='L'

			# Power capacity
			mincap=self.standardGenData[:,PMIN_YM].tolist()
			for s in range(S):
				for t in range(T):
					for g in range(G):
						self.A.append([[idxUC+t*G+g,idxPGen+s*T*G+t*G+g],[mincap[g],-1]])
						self.b.extend([0])
						self.senses+='L'
			maxcap=self.standardGenData[:,PMAX_YM].tolist()
			for s in range(S):
				for t in range(T):
					for g in range(G):
						self.A.append([[idxUC+t*G+g,idxPGen+s*T*G+t*G+g],[-1*maxcap[g],1]])
						self.b.extend([0])
						self.senses+='L'

			# Power generation must equal to net load demand (power balance)
			if 'consBatteryAsPVDummyLoad' in self.consList:
				netLoadDemand=(self.loadData-self.powerWind).tolist()
			else:	
				netLoadDemand=(self.loadData-self.powerSun-self.powerWind).tolist()
			for s in range(S):
				for t in range(T):
					keyATemp=[]
					valueATemp=[]
					for g in range(G):
						keyATemp.extend([idxPGen+s*T*G+t*G+g])
						valueATemp.extend([1])
					if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
						for battery in range(Battery):
							keyATemp.extend([idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery])
							valueATemp.extend([-1,1])		
					if 'consPVBattery' in self.consList:
						keyATemp.extend([idxPVU+s*T+t])
						valueATemp.extend([+1])
					if 'consPHS' in self.consList:
						for phs in range(PHS):
							keyATemp.extend([idxPumpPower+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs])
							valueATemp.extend([-1,1])
					self.A.append([keyATemp,valueATemp])
					self.b.extend([netLoadDemand[s][t]])
					self.senses+='E'
		if 'consStairwiseCost' in self.consList:
			if 'consInit' in self.consList:
				initialCountDown=self.continuityGenData[:,DT_YM].astype(int).tolist()
			else:
				initialCountDown=[999]*G
			maxCountDown=(np.array(initialCountDown)+T).tolist()
			# Note that the count down only matter if the unit is turned on later. 
			# That way. the value of countDown might be jumpling. 
			# It happens when the countDown considered unecessary.
			
			#countDown must be 0 for every U==1 #Not necessarily affect result
			# for t in range(T):
			#     for g in range(G):
			#         self.A.append([[idxUC+t*G+g,idxCountDown+t*G+g],[maxCountDown[g],1]])
			#         self.b.extend([maxCountDown[g]])
			#         self.senses+='L'

			#countDown-countDown(t-1) must be lower or equal to 1, not jumping offer #Not necessarily affect result
			# for t in range(T):
			#     if t==0:
			#         for g in range(G):
			#             self.A.append([[idxCountDown+t*G+g],[1]])
			#             self.b.extend([1+initialCountDown[g]])
			#             self.senses+='L'
			#     else:
			#         for g in range(G):
			#             self.A.append([[idxCountDown+t*G+g,idxCountDown+(t-1)*G+g],[1,-1]])
			#             self.b.extend([1])
			#             self.senses+='L'

			#countDown Must be incremental for every U==0
			for t in range(T):
				if t==0:
					for g in range(G):
						self.A.append([[idxUC+t*G+g,idxCountDown+t*G+g],[-1*maxCountDown[g],-1]])
						self.b.extend([-1-initialCountDown[g]])
						self.senses+='L'
				else:
					for g in range(G):
						self.A.append([[idxUC+t*G+g,idxCountDown+t*G+g,idxCountDown+(t-1)*G+g],[-1*maxCountDown[g],-1,1]])
						self.b.extend([-1])
						self.senses+='L'
			
			#if SU, either CS or HS must be 1
			for t in range(T):
				for g in range(G):
					self.A.append([[idxSU+t*G+g,idxHS+t*G+g,idxCS+t*G+g],[1,-1,-1]])
					self.b.extend([0])
					self.senses+='E'
			
			#must coldStart if countDown(t-1) >= hotTime
			hotTime=self.costGenData[:,HT_YM].astype(int).tolist()
			for t in range(T):
				if t==0:
					for g in range(G):
						self.A.append([[idxSU+t*G+g,idxHS+t*G+g,idxCS+t*G+g],[maxCountDown[g],-1*hotTime[g],-1*maxCountDown[g]]])
						self.b.extend([-1+maxCountDown[g]-initialCountDown[g]])
						self.senses+='L'
				else:
					for g in range(G):
						self.A.append([[idxSU+t*G+g,idxHS+t*G+g,idxCS+t*G+g,idxCountDown+(t-1)*G+g],[maxCountDown[g],-1*hotTime[g],-1*maxCountDown[g],1]])
						self.b.extend([-1+maxCountDown[g]])
						self.senses+='L'

		if 'consPiecewiseCost' in self.consList:
			# Sum of piece must equal to power dispatch
			for s in range(S):
				for t in range(T):
					for g in range(G):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxUC+t*G+g,idxPGen+s*T*G+t*G+g])
						valueATemp.extend([-1*mincap[g],1])
						for p in range(Piece):
							keyATemp.extend([idxPPieceGen+s*T*G*Piece+t*G*Piece+g*Piece+p])
							valueATemp.extend([-1])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+=('E')

			# Piece flag that the previous piece is maxed out
			for s in range(S):
				for t in range(T):
					for g in range(G):
						for p in range(Piece):
							if p==0: #Not necessary needed, since PPiece restricted to PGen
								self.A.append([[idxUC+t*G+g,idxPPieceFlag+s*T*G*Piece+t*G*Piece+g*Piece+p],[-1,1]])
								self.b.extend([0])
								self.senses+=('E')
								pass
							else:
								self.A.append([[idxPPieceGen+s*T*G*Piece+t*G*Piece+g*Piece+p-1,idxPPieceFlag+s*T*G*Piece+t*G*Piece+g*Piece+p],[-1,pieceWidth[g*Piece+p-1]]]) #-1 because flag based on prev
								self.b.extend([0])
								self.senses+='L'
			# Piece generate only if the flag==1
			for s in range(S):
				for t in range(T):
					for g in range(G):
						for p in range(Piece):
							self.A.append([[idxPPieceGen+s*T*G*Piece+t*G*Piece+g*Piece+p,idxPPieceFlag+s*T*G*Piece+t*G*Piece+g*Piece+p],[1,-1*pieceWidth[g*Piece+p]]])
							self.b.extend([0])
							self.senses+='L'

		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			# RSR and PGen must not exceed Pmax
			for s in range(S):
				for t in range(T):
					for g in range(G):
						self.A.append([[idxPGen+s*T*G+t*G+g,idxRSR+s*T*G+t*G+g],[1,1]])
						self.b.extend([maxcap[g]])
						self.senses+='L'
				
			# RSR Relation with UC
			maxRSR=self.freqRegulationGenData[:,RSRMAX_YM].tolist()
			for s in range(S):
				for t in range(T):
					for g in range(G):
						self.A.append([[idxRSR+s*T*G+t*G+g,idxUC+t*G+g],[1,-1*maxRSR[g]]])
						self.b.extend([0])
						self.senses+='L'

		if 'consSRContingency' in self.consList: #only support N-1 for now
			SRContingency=self.SRContingency.squeeze().astype(int).tolist()
			for s in range(S):
				for t in range(T):
					if SRContingency[t]==1:
						for g in range(G):
							keyATemp=[]
							valueATemp=[]
							keyATemp.extend([idxPGen+s*T*G+t*G+g])
							valueATemp.extend([1])
							for k in range(G):
								if k != g:
									keyATemp.extend([idxRSR+s*T*G+t*G+k])
									valueATemp.extend([-1])
							if 'consSCRPHS' in self.consList:
								for phs in range (PHS):
									keyATemp.extend([idxSCRPHSG+s*T*PHS+t*PHS+phs])
									valueATemp.extend([-1])
									if 'consFixedSpeedPHS' not in self.consList:
										keyATemp.extend([idxSCRPHSP+s*T*PHS+t*PHS+phs])
										valueATemp.extend([-1])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([0])
							self.senses+='L'
			pass

		# Minimum Up and Down Time
		if 'consMUTMDT' in self.consList:
			minimumUpTime=self.standardGenData[:,MUT_YM].astype(int).tolist()
			minimumDownTime=self.standardGenData[:,MDT_YM].astype(int).tolist()
			if 'consInit' in self.consList:
				previousUpTime=self.continuityGenData[:,UT_YM].tolist()
				previousDownTime=self.continuityGenData[:,DT_YM].tolist()

			#Minimum Up Time
			for t in range(T):
				for g in range(G):
					if t < minimumUpTime[g]:
						if 'consInit' in self.consList:
							keyATemp=[]
							valueATemp=[]
							for j in range(t):
								keyATemp.extend([idxUC+j*G+g])
								valueATemp.extend([-1])
							keyATemp.extend([idxSD+t*G+g])
							valueATemp.extend([minimumUpTime[g]])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([previousUpTime[g]])
							self.senses+='L'
					else:
						keyATemp=[]
						valueATemp=[]
						for j in range(t-minimumUpTime[g],t):
							keyATemp.extend([idxUC+j*G+g])
							valueATemp.extend([-1])
						keyATemp.extend([idxSD+t*G+g])
						valueATemp.extend([minimumUpTime[g]])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+='L'

			#Minimum Down Time
			for t in range(T):
				for g in range(G):
					if t < minimumDownTime[g]:
						if 'consInit' in self.consList:
							keyATemp=[]
							valueATemp=[]
							for j in range(t):
								keyATemp.extend([idxUC+j*G+g])
								valueATemp.extend([1])
							keyATemp.extend([idxSU+t*G+g])
							valueATemp.extend([minimumDownTime[g]])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([t+previousDownTime[g]])
							self.senses+='L'
					else:
						keyATemp=[]
						valueATemp=[]
						for j in range(t-minimumDownTime[g],t):
							keyATemp.extend([idxUC+j*G+g])
							valueATemp.extend([1])
						keyATemp.extend([idxSU+t*G+g])
						valueATemp.extend([minimumDownTime[g]])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([minimumDownTime[g]])
						self.senses+='L'

		# Initial Power Constraints
		if 'consBasicRamp' in self.consList:
			if 'consInit' in self.consList:
				initPower=self.continuityGenData[:,IP_YM].tolist()
				self.initPower=initPower

		# Basic Ramp Constraints
		if 'consBasicRamp' in self.consList:
			hourlyRampUp=self.standardGenData[:,RU_YM].tolist()
			hourlyRampDown=self.standardGenData[:,RD_YM].tolist()
			bonusStartupRamp=[]
			bonusShutdownRamp=[]
			for g in range(G):
				if mincap[g]>hourlyRampUp[g]:
					bonusStartupRamp.append(mincap[g]-hourlyRampUp[g])
				else:
					bonusStartupRamp.append(0)
				if mincap[g]>hourlyRampDown[g]:
					bonusShutdownRamp.append(mincap[g]-hourlyRampDown[g])
				else:
					bonusShutdownRamp.append(0)
			for s in range(S):
				for t in range(T):
					if t == 0: #firstHour
						if 'consInit' in self.consList:                            
							for g in range(G):
								self.A.append([[idxSD+t*G+g,idxSU+t*G+g,idxPGen+s*T*G+t*G+g],[bonusShutdownRamp[g],-1*bonusStartupRamp[g],1]])
								self.b.extend([hourlyRampUp[g]+initPower[g]])
								self.senses+='L'
							for g in range(G):
								self.A.append([[idxSD+t*G+g,idxSU+t*G+g,idxPGen+s*T*G+t*G+g],[-1*bonusShutdownRamp[g],bonusStartupRamp[g],-1]])
								self.b.extend([hourlyRampDown[g]-initPower[g]])
								self.senses+='L'                            
					else:            
						for g in range(G):
								self.A.append([[idxSD+t*G+g,idxSU+t*G+g,idxPGen+s*T*G+(t-1)*G+g,idxPGen+s*T*G+t*G+g],[bonusShutdownRamp[g],-1*bonusStartupRamp[g],-1,1]])
								self.b.extend([hourlyRampUp[g]])
								self.senses+='L'
						for g in range(G):        
								self.A.append([[idxSD+t*G+g,idxSU+t*G+g,idxPGen+s*T*G+(t-1)*G+g,idxPGen+s*T*G+t*G+g],[-1*bonusShutdownRamp[g],bonusStartupRamp[g],1,-1]])
								self.b.extend([hourlyRampDown[g]])
								self.senses+='L'

		# Must On Constraint
		if 'consMustOn' in self.consList:
			mustOnList=self.mustOnData.transpose().flatten().tolist()
			for i,j in zip(range(G*T),mustOnList):
				if j==1:
					self.A.append([[idxUC+i],[1]])
					self.b.extend([1])
					self.senses+='E'

		# Must Off Constraint
		if 'consMustOff' in self.consList:
			mustOffList=self.mustOffData.transpose().flatten().tolist()
			for i,j in zip(range(G*T),mustOffList):
				if j==1:
					self.A.append([[idxUC+i],[1]])
					self.b.extend([0])
					self.senses+='E'
					
		# Primary Reserve
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			# Primary reserve + P_it <= PMax
			for s in range(S):
				for t in range(T):
					for g in range(G):
						if 'consSRContingency' in self.consList:
							self.A.append([[idxUC+t*G+g,idxPGen+s*T*G+t*G+g,idxRPr+s*T*G+t*G+g],[-1*maxcap[g],1,1]])
							self.b.extend([0])
							self.senses+='L'
						# 	self.A.append([[idxUC+t*G+g,idxPGen+s*T*G+t*G+g,idxRPr+s*T*G+t*G+g,idxRSR+s*T*G+t*G+g],[-1*maxcap[g],1,1,1]])
						# 	self.b.extend([0])
						# 	self.senses+='L'
						# else :
						# 	self.A.append([[idxUC+t*G+g,idxPGen+s*T*G+t*G+g,idxRPr+s*T*G+t*G+g],[-1*maxcap[g],1,1]])
						# 	self.b.extend([0])
						# 	self.senses+='L'
						
			# RPr relation with Status - Unit hanya bisa menyediakan PFR jika kondisi ON
			maxRPr=self.freqRegulationGenData[:,RPMAX_YM].tolist()
			for s in range(S):
				for t in range(T):
					for g in range(G):
						self.A.append([[idxUC+t*G+g,idxRPr+s*T*G+t*G+g],[-1*maxRPr[g],1]])
						self.b.extend([0])
						self.senses+='L'

			# Primary reserve must be higher than outage unit, check for every unit -> Total PFR sistem >= Dispatch terbesar
			for s in range(S):
				for t in range(T):
					for g in range(G): #g is the outage unit
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxPGen+s*T*G+t*G+g])
						valueATemp.extend([1])
						for k in range(G):
							if k != g:
								keyATemp.extend([idxRPr+s*T*G+t*G+k])
								valueATemp.extend([-1])
						if 'consBatteryAsReserve' in self.consList:
							for battery in range(Battery):
								keyATemp.extend([idxRSt+s*T*Battery+t*Battery+battery])
								valueATemp.extend([-1])
						if 'consRPrPHS' in self.consList:
							for phs in range (PHS):
								keyATemp.extend([idxRPrPHS+s*T*PHS+t*PHS+phs])
								valueATemp.extend([-1])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+='L'

		# Primary Reserve with Minimum Frequency Steady State Constraint 				
		if 'consPrimaryDroop' in self.consList:
			FDSS=self.freqRegulationGenData[:,FDSS_YM].tolist()
			droopGen=self.freqRegulationGenData[:,DRMWHZ_YM].tolist()
			for s in range (S):
				for t in range (T):
					for g in range (G):
						self.A.append([[idxRPr+s*T*G+t*G+g,idxUC+t*G+g],[1,-1*droopGen[g]*FDSS[g]]])
						self.b.extend([0])
						self.senses+='L'

		# Primary Reserve Supplied by PHS
		if 'consRPrPHS' in self.consList:
			steady=self.phsData[:,DSS_YM].astype(float).tolist()
			Droop=self.phsData[:,DPS_YM].astype(float).tolist()
			for s in range (S):
				for t in range (T):
					for phs in range (PHS):
						self.A.append([[idxRPrPHS+s*T*PHS+t*PHS+phs,idxGenerateStatus+t*PHS+phs],[1,-1*Droop[phs]*steady[phs]]])
						self.b.extend([0])
						self.senses+='L'

		# Worst Case Contingency Inertia Reserve
		if 'consWorstCaseInertia' in self.consList:
			maxContingency=max(maxcap)
			maxContingencyIndex=maxcap.index(maxContingency)
			freqDeviationMax=-1*min(self.freqRegulationGenData[:,FDMIN_YM].tolist()) #f0-fmin-fdb, note: fmin-f0=freq dev min
			freqNominal=min(self.freqRegulationGenData[:,FNOM_YM].tolist())
			freqDeadBandDelta=self.freqRegulationGenData[:,FDB_YM].tolist()
			freqNadir=freqNominal-freqDeviationMax
			govRamp=self.freqRegulationGenData[:,RGOV_YM].tolist()
			inertia=self.freqRegulationGenData[:,INERTIA_YM].tolist()
			deadband=self.phsData[:,FDEAD_YM].tolist()
			govRampPHS=self.phsData[:,PHSGR_YM].tolist()
			inertiaPHS=self.phsData[:,PHSIN_YM].tolist()
			maxGenerate=self.phsData[:,PGMAX_YM].tolist() #generatingPower
			# #RPr limited by time nadir (time nadir is product of worst case inertia)
			for s in range(S):
				for t in range(T):
					for g in range(G):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxRPr+s*T*G+t*G+g])
						valueATemp.extend([freqNominal*maxContingency/(govRamp[g]*(4*freqNominal-2*freqDeadBandDelta[g]-4*freqNadir))])
						# print('b',freqNominal*maxContingency/(govRamp[g]*(4*freqNominal-2*freqDeadBandDelta[g]-4*freqNadir)))
						for k in range(G):
							keyATemp.extend([idxUC+t*G+k])
							valueATemp.extend([-1*inertia[k]*maxcap[k]])
						if 'consPHS' in self.consList:
							for phs in range(PHS):
								keyATemp.extend([idxGenerateStatus+t*PHS+phs])
								valueATemp.extend([-1*inertiaPHS[phs]*maxGenerate[phs]])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([-1*inertia[maxContingencyIndex]*maxContingency])
						self.senses+='L'

			if 'consRPrPHS' in self.consList:
				for s in range (S):
					for t in range (T):
						for phs in range (PHS):
							keyATemp=[]
							valueATemp=[]
							keyATemp.extend([idxRPrPHS+s*T*PHS+t*PHS+phs])
							valueATemp.extend([freqNominal*maxContingency/(govRampPHS[phs]*(4*freqNominal-2*deadband[phs]-4*freqNadir))])
							for k in range(G):
								keyATemp.extend([idxUC+t*G+k])
								valueATemp.extend([-1*inertia[k]*maxcap[k]])
							for phs in range(PHS):
								keyATemp.extend([idxGenerateStatus+t*PHS+phs])
								valueATemp.extend([-1*inertiaPHS[phs]*maxGenerate[phs]])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([-1*inertia[maxContingencyIndex]*maxContingency])
							self.senses+='L'	

			# print(np.array(self.A))
			# print(np.array(self.b))
			# exit()

		# Power Flow Constraints using DC Model
		if 'consDCPF' in self.consList:
			#basMVA
			[baseMVA]=self.busData[:,BMVA_YM].tolist()

			#PBus equal to the net of power (+ means generate, - means absorb) -> membuat vektor injeksi daya bus
			genLocation=(self.standardGenData[:,BL_YM]-1).tolist() #genLocation -1 to make it in python format
			print("ANJIR", self.busLoad.shape)
			netLoadBus=(-self.busLoad+self.busSun+self.busWind).tolist()
			for s in range(S):
				for t in range(T):
					for bus in range(Bus):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxPBus+s*T*Bus+t*Bus+bus])
						valueATemp.extend([1])
						for g in range(G):
							if genLocation[g]==bus:
								keyATemp.extend([idxPGen+s*T*G+t*G+g])
								valueATemp.extend([-1/baseMVA])
						if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
							batteryLocation=(self.batteryData[:,BBL_YM]-1).tolist()
							for battery in range(Battery):
								if batteryLocation[battery]==bus:
									keyATemp.extend([idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery])
									valueATemp.extend([1/baseMVA,-1/baseMVA])
						if 'consPHS' in self.consList:
							phsLocation=(self.phsData[:,PBL_YM]-1).tolist()
							for phs in range(PHS):
								if phsLocation[phs]==bus:
									keyATemp.extend([idxPumpPower+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs])
									valueATemp.extend([1/baseMVA,-1/baseMVA])
						if 'consBatteryAsPVDummyLoad' in self.consList:
							batteryLocation=(self.batteryData[:,BBL_YM]-1).tolist()
							for battery in range(Battery):
								if batteryLocation[battery]==bus:
									keyATemp.extend([idxChargePowerFromPV+s*T*Battery+t*Battery+battery])
									valueATemp.extend([1/baseMVA])
							
						self.A.append([keyATemp,valueATemp])
						self.b.extend([netLoadBus[bus][s*T+t]/baseMVA])
						self.senses+='E'
			# print('The Gen Loc',genLocation)
			# print('The Net Load Bus',netLoadBus)
			# print(batteryLocation)

			#susceptance -> membuat matrix susceptance
			reactance=self.branchData[:,X_YM].tolist()
			susceptance=[]
			for branch in range(Branch):
				susceptance.extend([1/(reactance[branch])])
			# exit()

			#susceptance diagonal (b matrix) -> membuat matriks b
			susceptanceDiag=np.zeros((Branch,Branch))
			for branch in range(Branch):
				susceptanceDiag[branch,branch]=susceptance[branch]
			# print(np.array(susceptanceDiag))
			# exit()

			#from-to matrix (A matrix) -> Membuat matriks A
			fromList=(self.branchData[:,FROM_YM]-1).astype(int).tolist() #-1 to make it in python format
			toList=(self.branchData[:,TO_YM]-1).astype(int).tolist() #-1 to make it in python format
			fromTo=np.zeros((Branch,Bus))
			for branch in range(Branch):
				fromTo[branch,fromList[branch]]=1
				fromTo[branch,toList[branch]]=-1
			# print(fromList)
			# print(toList)
			# print(fromTo)
			# exit()

			#bA matrix
			bAMatrix=(baseMVA*np.matmul(susceptanceDiag,fromTo)).tolist()
			# print(np.array(bAMatrix))
			# exit()
			
			#admitanceMatrix -> membuat matriks susceptance
			admitanceMatrix=np.zeros((Bus,Bus))
			for fromList_val,toList_val,susceptance_val in zip(fromList,toList,susceptance):
				admitanceMatrix[fromList_val,toList_val]=-1*susceptance_val
				admitanceMatrix[toList_val,fromList_val]=-1*susceptance_val
				admitanceMatrix[fromList_val,fromList_val]=admitanceMatrix[fromList_val,fromList_val]+susceptance_val
				admitanceMatrix[toList_val,toList_val]=admitanceMatrix[toList_val,toList_val]+susceptance_val

			[slackBus]=(self.busData[:,SB_YM]-1).astype(int).tolist()
			admitanceMatrixNew=admitanceMatrix
			admitanceMatrixNew=np.delete(admitanceMatrixNew,slackBus,0)
			admitanceMatrixNew=np.delete(admitanceMatrixNew,slackBus,1)
			# print(admitanceMatrixNew)
			admitanceMatrixNew=np.linalg.inv(admitanceMatrixNew)
			admitanceMatrixNew=np.insert(admitanceMatrixNew,slackBus,None,0)
			admitanceMatrixNew=np.insert(admitanceMatrixNew,slackBus,None,1)
			admitanceMatrixNew=admitanceMatrixNew.tolist()
			# print(admitanceMatrix)
			# print(np.array(admitanceMatrixNew))
			# exit()

			#theta -> membuat vektor theta (buat PTDF)
			for s in range(S):
				for t in range(T):
					for row in range(Bus):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxTheta+s*T*Bus+t*Bus+row])
						valueATemp.extend([1])
						if row != slackBus:
							for col in range (Bus):
								if col != slackBus:
									keyATemp.extend([idxPBus+s*T*Bus+t*Bus+col])
									valueATemp.extend([-1*(admitanceMatrixNew[row][col])])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+='E'
						pass
						
			#lineLoading -> perhitungan aliran daya (lineloading = matriks PTDF x injeksi daya bus)
			for s in range(S):
				for t in range(T):
					for branch in range(Branch):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxLineLoad+s*T*Branch+t*Branch+branch])
						valueATemp.extend([1])
						for bus in range(Bus):
							keyATemp.extend([idxTheta+s*T*Bus+t*Bus+bus])
							valueATemp.extend([-1*(bAMatrix[branch][bus])])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+='E'

		# To guarantee post contingency line load doesnt exceed line limit
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList): 
			if 'consCongestionPr' in self.consList:
				#baseMVA
				[baseMVA]=self.busData[:,BMVA_YM].tolist()
				#PBus equal to the net of power (+ means generate, - means absorb) -> membuat vektor injeksi daya bus dengan tambahan PFR
				genLocation=(self.standardGenData[:,BL_YM]-1).tolist() #genLocation -1 to make it in python format
				netLoadBus=(-self.busLoad+self.busSun+self.busWind).tolist()# PBusPr
				for s in range (S):
					for t in range (T):
						for bus in range (Bus):
							keyATemp=[]
							valueATemp=[]
							keyATemp.extend([idxPBusPr+s*T*Bus+t*Bus+bus])
							valueATemp.extend([1])
							for k in range (G):
								if k != g:
									if genLocation[k]==bus:
										keyATemp.extend([idxPGen+s*T*G+t*G+k])
										valueATemp.extend([-1/baseMVA])
										keyATemp.extend([idxRPr+s*T*G+t*G+k])
										valueATemp.extend([-1/baseMVA])
							if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
								batteryLocation=(self.batteryData[:,BBL_YM]-1).tolist()
								for battery in range(Battery):
									if batteryLocation[battery]==bus:
										keyATemp.extend([idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery])
										valueATemp.extend([1/baseMVA,-1/baseMVA])
							if 'consPHS' in self.consList:
								phsLocation=(self.phsData[:,PBL_YM]-1).tolist()
								for phs in range(PHS):
									if phsLocation[phs]==bus:
										keyATemp.extend([idxPumpPower+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs])
										valueATemp.extend([1/baseMVA,-1/baseMVA])
										if 'consRPrPHS' in self.consList:
											keyATemp.extend([idxRPrPHS+s*T*PHS+t*phs+phs])
											valueATemp.extend([1/baseMVA])
							if 'consBatteryAsPVDummyLoad' in self.consList:
								batteryLocation=(self.batteryData[:,BBL_YM]-1).tolist()
								for battery in range(Battery):
									if batteryLocation[battery]==bus:
										keyATemp.extend([idxChargePowerFromPV+s*T*Battery+t*Battery+battery])
										valueATemp.extend([1/baseMVA])
							if 'consBatteryAsReserve' in self.consList:
								batteryLocation=(self.batteryData[:,BBL_YM]-1).tolist()
								for battery in range(Battery):
									if batteryLocation[battery]==bus:
										keyATemp.extend([idxRSt+s*T*Battery+t*Battery+battery])
										valueATemp.extend([-1/baseMVA])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([netLoadBus[bus][s*T+t]/baseMVA])
							self.senses+='E'
			
				# ThetaPr
				for s in range(S):
					for t in range(T):
						for row in range(Bus):
							keyATemp=[]
							valueATemp=[]
							keyATemp.extend([idxThetaPr+s*T*Bus+t*Bus+row])
							valueATemp.extend([1])
							if row != slackBus:
								for col in range (Bus):
									if col != slackBus:
										keyATemp.extend([idxPBusPr+s*T*Bus+t*Bus+col])
										valueATemp.extend([-1*(admitanceMatrixNew[row][col])])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([0])
							self.senses+='E'
							pass

				#lineLoadingPr
				for s in range(S):
					for t in range(T):
						for branch in range(Branch):
							keyATemp=[]
							valueATemp=[]
							keyATemp.extend([idxLineLoadPr+s*T*Branch+t*Branch+branch])
							valueATemp.extend([1])
							for bus in range(Bus):
								keyATemp.extend([idxThetaPr+s*T*Bus+t*Bus+bus])
								valueATemp.extend([-1*(bAMatrix[branch][bus])])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([0])
							self.senses+='E' 

		#Batas Transfer Daya Region(Jabal)
		if 'consRegionTransfer' in self.consList:
			Region=self.branchData[:,REG_YM].astype(float).tolist()
			for t in range(T):
				keyATemp=[]
				valueATemp=[]
				keyBTemp=[]
				valueBTemp=[]
				keyCTemp=[]
				valueCTemp=[]
				for branch in range(Branch):
					if Region[branch] == 1:
						keyATemp.extend([idxLineLoad+t*Branch+branch])
						valueATemp.extend([1])
					if Region[branch] ==  2:
						keyBTemp.extend([idxLineLoad+t*Branch+branch])
						valueBTemp.extend([1])
					if Region[branch] ==  3:
						keyCTemp.extend([idxLineLoad+t*Branch+branch])
						valueCTemp.extend([1])
					self.A.append([keyATemp,valueATemp])
					self.b.extend([2300])
					self.senses+= 'L'
					self.A.append([keyBTemp,valueBTemp])
					self.b.extend([2300])
					self.senses+= 'L'
					self.A.append([keyCTemp,valueCTemp])
					self.b.extend([2300])
					self.senses+= 'L'

		# Battery Operation Constraints
		if 'consBatteryAsLoadLeveling' in self.consList:
			#chargeStatus when charging
			maxCharge=self.batteryData[:,CRMAX_YM].astype(float).tolist() #chargePower
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						self.A.append([[idxChargeStatus+t*Battery+battery,idxChargePower+s*T*Battery+t*Battery+battery],[-1*maxCharge[battery],1]])
						self.b.extend([0])
						self.senses+='L'

			#dischargeStatus when discharging
			maxDischarge=self.batteryData[:,DRMAX_YM].astype(float).tolist() #discharePower
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						self.A.append([[idxDischargeStatus+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery],[-1*maxDischarge[battery],1]])
						self.b.extend([0])
						self.senses+='L'     

			#self.SOC
			batteryChargeEfficiency=self.batteryData[:,BCEFF_YM].astype(float).tolist()
			batteryDischargeEfficiency=self.batteryData[:,BDEFF_YM].astype(float).tolist()
			timeRes=self.batteryData[:,TRES_YM].tolist()
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						self.A.append([[idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery,idxSOC+s*T*Battery+t*Battery+battery,idxSOCPrev+s*T*Battery+t*Battery+battery],[batteryChargeEfficiency[battery]*timeRes[battery],-1/batteryDischargeEfficiency[battery]*timeRes[battery],-1,1]])
						self.b.extend([0])
						self.senses+='E'       

		if 'consBatteryAsPVDummyLoad' in self.consList:	
			powerSun=self.powerSun.tolist()
			for s in range(S):
				for t in range(T):
					keyATemp=[]
					valueATemp=[]
					keyATemp.extend([idxPVU+s*T+t])
					valueATemp.extend([1])
					for battery in range(Battery):
						keyATemp.extend([idxChargePowerFromPV+s*T*Battery+t*Battery+battery])
						valueATemp.extend([1])
					self.A.append([keyATemp,valueATemp])
					self.b.extend([powerSun[s][t]])
					self.senses+='E'
	
			#chargeStatus when charging
			maxCharge=self.batteryData[:,CRMAX_YM].astype(float).tolist() #chargePower
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						self.A.append([[idxChargeStatus+t*Battery+battery,idxChargePower+s*T*Battery+t*Battery+battery,idxChargePowerFromPV+s*T*Battery+t*Battery+battery],[-1*maxCharge[battery],1,1]])
						self.b.extend([0])
						self.senses+='L'

			#dischargeStatus when discharging
			maxDischarge=self.batteryData[:,DRMAX_YM].astype(float).tolist() #dischargePower
			maxDRWithRS=self.batteryData[:,DRMAXRS_YM].astype(float).tolist()
			# minRSt=self.batteryData[:,RSTMIN_YM].astype(float).tolist()	#allocationRStMinimum
			# allocationRSt=maxDischarge*minRSt
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						# self.A.append([[idxDischargeStatus+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery],[-1*maxDischarge[battery],1]])
						self.A.append([[idxDischargeStatus+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery],[-1*maxDRWithRS[battery],1]])
						self.b.extend([0])
						self.senses+='L'     
			#self.SOC
			batteryChargeEfficiency=self.batteryData[:,BCEFF_YM].astype(float).tolist()
			batteryDischargeEfficiency=self.batteryData[:,BDEFF_YM].astype(float).tolist()
			timeRes=self.batteryData[:,TRES_YM].tolist()
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						self.A.append([[idxChargePower+s*T*Battery+t*Battery+battery,idxChargePowerFromPV+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery,idxSOC+s*T*Battery+t*Battery+battery,idxSOCPrev+s*T*Battery+t*Battery+battery],[batteryChargeEfficiency[battery]*timeRes[battery],batteryChargeEfficiency[battery]*timeRes[battery],-1/batteryDischargeEfficiency[battery]*timeRes[battery],-1,1]])
						self.b.extend([0])
						self.senses+='E'

		if 'consBatteryAsReserve' in self.consList:
			#RSt+PD<PDMax
			maxDischarge=self.batteryData[:,DRMAX_YM].astype(float).tolist() #dischargePower
			for s in range(S):
				for t in range(T):
					for battery in range(Battery):
						keyATemp=[]
						valueATemp=[]
						# keyATemp.extend([idxRSt+s*T*Battery+t*Battery+battery,idxDischargeStatus+t*Battery+battery,idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery])
						# valueATemp.extend([1,-1*maxDischarge[batttery],1,1])
						# keyATemp.extend([idxDischargeStatus+t*Battery+battery,idxRSt+s*T*Battery+t*Battery+battery])
						# keyATemp.extend([idxDischargeStatus+t*Battery+battery,idxRSt+s*T*Battery+t*Battery+battery,idxChargePower+s*T*Battery+t*Battery+battery])
						# valueATemp.extend([-1*maxDischarge[battery],1])
						# valueATemp.extend([-1*maxDischarge[battery],1,1])
						# if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
							# keyATemp.extend([idxDischargePower+s*T*Battery+t*Battery+battery])
							# valueATemp.extend([1])
						self.A.append([[idxRSt+s*T*Battery+t*Battery+battery,idxChargePower+s*T*Battery+t*Battery+battery,idxDischargePower+s*T*Battery+t*Battery+battery],[1,-1,1]])
						self.b.extend([maxDischarge[battery]])
						self.senses+='L'
						# self.A.append([keyATemp,valueATemp])
						# self.b.extend([0])
						# self.senses+='L'  
			
		if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
			#can't charging and discharging at the same time
			for t in range(T):
				for battery in range(Battery):
					self.A.append([[idxChargeStatus+t*Battery+battery,idxDischargeStatus+t*Battery+battery],[1,1]])
					self.b.extend([1])
					self.senses+='L'

			#self.SOC and self.SOCPrev Relationship
			initialSOC=self.batteryData[:,ISOC_YM].astype(float).tolist()
			# print(initialSOC)
			for s in range(S):
				for t in range(T):
					if t == 0:
						for battery in range(Battery):
							self.A.append([[idxSOCPrev+s*T*Battery+t*Battery+battery],[1]])
							self.b.extend([initialSOC[battery]])
							self.senses+='E'
							self.A.append([[idxSOC+s*T*Battery+t*Battery+battery],[1]])
							self.b.extend([initialSOC[battery]])
							self.senses+='E'                
					else:
						for battery in range(Battery):
							self.A.append([[idxSOC+s*T*Battery+(t-1)*Battery+battery,idxSOCPrev+s*T*Battery+t*Battery+battery],[1,-1]])
							self.b.extend([0])
							self.senses+='E'
			#FinalSOC
			finalSOC=self.batteryData[:,FSOC_YM].astype(float).tolist()
			# exit()
			for s in range(S):
				for battery in range(Battery):
					self.A.append([[idxSOC+s*T*Battery+(T-1)*Battery+battery],[1]])
					self.b.extend([finalSOC[battery]])
					self.senses+='E'        

		#  PHS Operation Constraints
		if 'consPHS' in self.consList:
			#pumpStatus when pumping
			maxPump=self.phsData[:,PPMAX_YM].astype(float).tolist() #pumpingPower
			for s in range(S):
				for t in range(T):
					for phs in range(PHS):
						if 'consFixedSpeedPHS' in self.consList:
							self.A.append([[idxPumpStatus+t*PHS+phs,idxPumpPower+s*T*PHS+t*PHS+phs],[-1*maxPump[phs],1]])
							self.b.extend([0])
							self.senses+='E'
						else :
							self.A.append([[idxPumpStatus+t*PHS+phs,idxPumpPower+s*T*PHS+t*PHS+phs],[-1*maxPump[phs],1]])
							self.b.extend([0])
							self.senses+='L'
			#Minimum Pump (Rpr PHS <= PPump-Pmin)
			# minPump=self.phsData[:,PPMIN_YM].astype(float).tolist()
			# if 'consFixedSpeedPHS' not in self.consList:
			# 	for s in range (S):
			# 		for t in range (T):
			# 			for phs in range (PHS):
			# 				keyATemp=[]
			# 				valueATemp=[]
			# 				keyATemp.extend([idxPumpStatus+t*PHS+phs,idxPumpPower+s*T*PHS+t*PHS+phs])
			# 				valueATemp.extend([minPump[phs],-1])
			# 				# if 'consRPrPHS' in self.consList:
			# 				# 	keyATemp.extend([idxRPrPHSDown+s*T*PHS+t*PHS+phs])
			# 				# 	valueATemp.extend([1])
			# 				self.A.append([keyATemp,valueATemp])
			# 				self.b.extend([0])
			# 				self.senses+='L' 

			#GenereateStatus when generating (Pgen + RPr PHS <= Max Generator Capacity)
			maxGenerate=self.phsData[:,PGMAX_YM].astype(float).tolist() #generatingPower
			for s in range(S):
				for t in range(T):
					for phs in range(PHS):
						keyATemp=[]
						valueATemp=[]
						keyATemp.extend([idxGenerateStatus+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs])
						valueATemp.extend([-1*maxGenerate[phs],1])
						if 'consRPrPHS' in self.consList:
							keyATemp.extend([idxRPrPHS+s*T*PHS+t*PHS+phs])
							valueATemp.extend([1])
						if 'consSCRPHS' in self.consList:
							keyATemp.extend([idxSCRPHSG+s*T*PHS+t*PHS+phs])
							valueATemp.extend([1])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([0])
						self.senses+='L'  

			minGenerate=self.phsData[:,PGMIN_YM].astype(float).tolist()
			for s in range(S):
				for t in range(T):
					for phs in range(PHS):
						self.A.append([[idxGenerateStatus+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs],[minGenerate[phs],-1]])
						self.b.extend([0])
						self.senses+='L'   

			#pumpDebitStatus when pumping
			maxPumpDebit=self.phsData[:,PDMAX_YM].astype(float).tolist() #pumpingPowerDebit
			phsPumpEfficiency=self.phsData[:,PPEFF_YM].astype(float).tolist()
			phsHead=self.phsData[:,PH_YM].astype(float).tolist()
			phsWaterDensity=self.phsData[:,WD_YM].astype(float).tolist()
			phsGravity=self.phsData[:,G_YM].astype(float).tolist()
			# for s in range(S):
			# 	for t in range(T):
			# 		for phs in range(PHS):
			# 			self.A.append([[idxPumpStatus+t*PHS+phs,idxPumpPower+s*T*PHS+t*PHS+phs],[-1*maxPumpDebit[phs],(phsPumpEfficiency[phs]/(phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs]))]])
			# 			self.b.extend([0])
			# 			self.senses+='L'

			#GenerateDebitStatus when generating
			maxGenerateDebit=self.phsData[:,GDMAX_YM].astype(float).tolist() #generatingPowerDebit
			phsGenerateEfficiency=self.phsData[:,PGEFF_YM].astype(float).tolist()
			for s in range(S):
				for t in range(T):
					for phs in range(PHS):
						self.A.append([[idxGenerateStatus+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs],[-1*maxGenerateDebit[phs],1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs])]])
						# self.A.append([[idxGenerateStatus+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs,idxRPrPHS+s*T*PHS+t*PHS+phs],[-1*maxGenerateDebit[phs],1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs]),1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs])]])
						self.b.extend([0])
						self.senses+='L'     

			#self.UR
			for s in range(S):
				for t in range(T):
					for phs in range(PHS):
						self.A.append([[idxPumpPower+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs,idxUR+s*T*PHS+t*PHS+phs,idxURPrev+s*T*PHS+t*PHS+phs],[(phsPumpEfficiency[phs]/(phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs])),(-1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs])),-1,1]])
						self.b.extend([0])
						self.senses+='E'
			
			URMin=self.phsData[:,URMIN_YM].astype(float).tolist()
			# Memastikan status gen dan pump selalu sesuai
			if 'consRPrPHS' in self.consList:
				# RPrPHS relation with Status
				maxRPrPHS=self.phsData[:,RPRMAX_YM].tolist()
				for s in range(S):
					for t in range(T):
						for phs in range(PHS):
							self.A.append([[idxGenerateStatus+t*PHS+phs,idxRPrPHS+s*T*PHS+t*PHS+phs],[-1*maxRPrPHS[phs],1]])
							self.b.extend([0])
							self.senses+='L'
				
				# can't empty reservoir when RPrPHS ON
				# for s in range (S):
				# 	for t in range (T):
				# 		for phs in range (PHS):
				# 			keyATemp=[]
				# 			valueATemp=[]
				# 			keyATemp.extend=([idxGenerateStatus+t*PHS+phs,idxURPrev+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs,idxRPr+s*T*PHS+t*PHS+phs])
				# 			valueATemp.extend=([URMin[phs],-1,(1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs])),(1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs]))])
				# 			if 'consSCRPHS' in self.consList:
				# 				keyATemp.extend([idxSCRPHSG*s*T*PHS+t*PHS+phs])
				# 				valueATemp.extend([(1/(phsGenerateEfficiency[phs]*phsWaterDensity[phs]*phsGravity[phs]*phsHead[phs]))])
				# 			self.A.append([keyATemp,valueATemp])
				# 			self.b.extend([0])
				# 			self.senses+='L'

			# can't pump and generate at the same time
			for t in range(T):
				for phs in range(PHS):
					self.A.append([[idxPumpStatus+t*PHS+phs,idxGenerateStatus+t*PHS+phs],[1,1]])
					self.b.extend([1])
					self.senses+='L'

			#self.UR and self.URPrev Relationship
			initialUR=self.phsData[:,IUR_YM].astype(float).tolist()
			print(initialUR)
			for s in range(S):
				for t in range(T):
					if t == 0:
						for phs in range(PHS):
							self.A.append([[idxURPrev+s*T*PHS+t*PHS+phs],[1]])
							self.b.extend([initialUR[phs]])
							self.senses+='E'
							self.A.append([[idxUR+s*T*PHS+t*PHS+phs],[1]])
							self.b.extend([initialUR[phs]])
							self.senses+='E'                
					else:
						for phs in range(PHS):
							self.A.append([[idxUR+s*T*PHS+(t-1)*PHS+phs,idxURPrev+s*T*PHS+t*PHS+phs],[1,-1]])
							self.b.extend([0])
							self.senses+='E'
			#FinalUR
			finalUR=self.phsData[:,FUR_YM].astype(float).tolist()
			# exit()
			for s in range(S):
				for phs in range(PHS):
					self.A.append([[idxUR+s*T*PHS+(T-1)*PHS+phs],[1]])
					self.b.extend([finalUR[phs]])
					self.senses+='E'        
		
			# Changing Status (1)
			for t in range(T):
				for phs in range(PHS):
					if t!=0:
						self.A.append([[idxPumpStatus+t*PHS+phs,idxGenerateStatus+(t+1)*PHS+phs],[1,1]])
						self.b.extend([1])
						self.senses+='L'
		
			# Changing Status (2)
			for t in range(T):
				for phs in range(PHS):
					if t!=0:
						self.A.append([[idxPumpStatus+(t+1)*PHS+phs,idxGenerateStatus+t*PHS+phs],[1,1]])
						self.b.extend([1])
						self.senses+='L'

			if 'consSCRPHS' in self.consList:
				#PHS Spinning reserve allocation
				# Max allowable SCR from PHS :
				minPump=self.phsData[:,PPMIN_YM].astype(float).tolist()
				maxRamp=self.phsData[:,RUMAX_YM].astype(float).tolist()

				# SCRPHSPump Mode <= PGen-Pmin 
				if 'consFixedSpeedPHS' not in self.consList:
					for s in range (S):
						for t in range (T):
							for phs in range(PHS):
								self.A.append([[idxSCRPHSP+s*T*PHS+t*PHS+phs,idxPumpPower+s*T*PHS+t*PHS+phs,idxPumpStatus+t*PHS+phs],[1,-1,1*minPump[phs]]])
								self.b.extend([0])
								self.senses+='L'

					#  SCR PHS Pump only has value if Status = Gen 
					for s in range (S):
						for t in range (T):
							for phs in range (PHS):
								self.A.append([[idxSCRPHSP+s*T*PHS+t*PHS+phs,idxPumpStatus+t*PHS+phs],[1,-1*maxRamp[phs]]])
								self.b.extend([0])
								self.senses+='L'

				# # SCR PHS Pump Only has value if Status = Pump						
				# for s in range (S):	
				# 	for t in range (T):
				# 		for phs in range(PHS):
				# 			self.A.append([[idxSCRPHSG+s*T*PHS+t*PHS+phs,idxGeneratePower+s*T*PHS+t*PHS+phs,idxGenerateStatus+t*PHS+phs],[1,1,-1*maxGenerate[phs]]])
				# 			self.b.extend([0])
				# 			self.senses+='L'

		# HydroThermal Coordination
		if 'consHydroThermalCoordination' in self.consList :
			#Equation 1 (Q = a+ bP)
			Debit=self.standardGenData[:,QHP_YM].astype(float).tolist()
			HydroStatus=self.standardGenData[:,HS_YM].astype(int).tolist()
			HydroA=self.standardGenData[:,AHP_YM].astype(float).tolist()
			HydroB=self.standardGenData[:,BHP_YM].astype(float).tolist()
			for s in range (S):
				for t in range(T):
					for g in range(G):
						if HydroStatus[g]!=0:
							for h in range (HydroStatus[g]):
								if h==0:
									keyATemp=[idxUC+s*T*G+t*G+g, idxPGen+s*T*G+t*G+g]
									valueATemp=[HydroA[g]/HydroStatus[g], HydroB[g]]
									# keyATemp.extend([idxUC+s*T*G+t*G+g, idxPGen+s*T*G+t*G+g])
									# valueATemp.extend([HydroA[g]/HydroStatus[g], HydroB[g]])
								elif h>0:
									keyATemp.extend([idxUC+s*T*G+t*G+g+h, idxPGen+s*T*G+t*G+g+h])
									valueATemp.extend([HydroA[g]/HydroStatus[g], HydroB[g]])
							self.A.append([keyATemp,valueATemp])
							self.b.extend([Debit[g]])
							self.senses+='L'
		# Take or Pay PLTP
		if 'consToP' in self.consList:	
			ToP=self.standardGenData[:,TOP_YM].astype(float).tolist()	
			for s in range(S):
				for g in range(G):
					if ToP[g]!=0:
						keyATemp = []
						valueATemp= []	
						for t in range(T):
							keyATemp.extend([idxPGen+s*T*G+t*G+g])
							valueATemp.extend([-1])
						self.A.append([keyATemp,valueATemp])
						self.b.extend([-1*ToP[g]])
						self.senses+='L'
	
		# print('A Matrix: ', np.array(self.A))
		# print('b Matrix: ', self.b)
		# print("Matrix f'",self.objVar)
		# print("Matrix Q",self.qmat)
		# print('Sense',self.senses)
		# exit()
	#------------------------------------------------------------------------------#
	## To CPLEX Format
		# print('obj',len(self.objVar))
		# print('lb',len(self.lbVar))
		# print('ub',len(self.ubVar))
		# print('type', len(self.typesVar))
		# print('senses',len(self.senses),np.shape(self.senses))
		# print('rhs',len(self.b),np.shape(self.b))
		# print('lin_expr',len(self.A),np.shape(self.A))
		# print(self.senses)
		# exit()
		self.cplexClass=cplex.Cplex()
		self.cplexClass.set_problem_name(self.caseName)
		self.cplexClass.objective.set_sense(self.cplexClass.objective.sense.minimize)
		self.cplexClass.variables.add(
			obj=self.objVar,
			ub=self.ubVar,
			lb=self.lbVar,
			types=self.typesVar
		)
		self.cplexClass.linear_constraints.add(
			lin_expr=self.A,
			rhs=self.b,
			senses=self.senses
		)
		if 'consModeOptimOnlyMILP' not in self.consList:
			self.cplexClass.objective.set_quadratic(self.qmat)

		# with open("output.txt", "w") as f:
		#     output = theProblem.set_results_stream(f)
		#     output.write("this is an example")
			
		# theProblem.set_results_stream()
		# theProblem.parameters.barrier.convergetol=0.00000001
		# theProblem.parameters.barrier.limits.objrange

	def printIndex(self):
		print('idxUC',self.idxUC)
		print('idxSD',self.idxSD)
		print('idxSU',self.idxSU)
		print('idxPGen',self.idxPGen)
		if 'consPiecewiseCost' in self.consList:
			print('idxPPieceGen',self.idxPPieceGen)
			if 'consModePiecewiseNaive' not in self.consList:
				print('idxPPieceFlag',self.idxPPieceFlag)
		if 'consStairwiseCost' in self.consList:
			print('idxHS',self.idxHS)
			print('idxCS',self.idxCS)
		if any (i in ['consWorstCaseInertia','consSteadyPrimFreq'] for i in self.consList):
			print('idxRPr',self.idxRPr)

	def printNumberOfData(self):
		print('nGen: ',self.numberOfGen)
		print('nT: ',self.numberOfTime)
		print('nS: ',self.numberOfState)
		if 'consPiecewiseCost' in self.consList:
			print('nPiece: ',self.numberOfPiece)
		if 'consDCPF' in self.consList:
			print('nBus: ',self.numberOfBus)
			print('nBranch: ',self.numberOfBranch)
		if any(i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad','consBatteryAsReserve'] for i in self.consList):
			print('nBat: ',self.numberOfBattery)
	
	def run_UC(self):
		# Problem Formulation
		self.makeProblem()

		# Print Problem Parameters
		self.printIndex()
		self.printNumberOfData()

		self.logPath=os.path.join(os.getcwd(),'log_UC.txt')
		with open(self.logPath, 'w+') as fileTxt:
			self.cplexClass.set_results_stream(fileTxt)
			self.cplexClass.solve()
		with open(self.logPath, 'r') as fileTxt:
			for line in fileTxt:
				if 'Total (root+branch&cut) =' in line:
					lineTime=line.split()
					self.computationTime=float(lineTime[3])
					print('Computation Time =',self.computationTime)
		self.solution=self.cplexClass.solution
		print("Case Name: ",self.caseName)
		print("Solution status = " , self.solution.get_status(), ":", end=' ') #101
		print(self.solution.status[self.solution.get_status()]) #optimal
		print("Solution value  = ", self.solution.get_objective_value())
		self.reshapeOutputFlag=0
		self.partialCostFlag=0
		self.summaryDicFlag=0

		# Print Output
		self.printOutput()
		self.partialCost(decimal_place=4)
		self.getSummaryDic(print_summary_dic=True)
		self.exportToCSV(name_mark=False)

	
	def reshapeOutput(self):
		if self.reshapeOutputFlag==1:
			return
		self.reshapeOutputFlag=1
		
		if 'consUC'in self.consList:
			self.ucOut=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxUC
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.ucOut[g,t]=self.solution.get_values(k)
					k+=1

			self.powerOut=np.zeros((self.numberOfState,self.numberOfGen,self.numberOfTime))
			k=self.idxPGen
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for g in range(self.numberOfGen):
						self.powerOut[s,g,t]=self.solution.get_values(k)
						k+=1

			self.startUpOut=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxSU
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.startUpOut[g,t]=self.solution.get_values(k)
					k+=1

			self.shutDownOut=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxSD
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.shutDownOut[g,t]=self.solution.get_values(k)
					k+=1

		if all(i in ['consInit','consMUTMDT'] for i in self.consList):
			pass
		
		if 'consPiecewiseCost' in self.consList:
			self.PPieceGen=np.zeros((self.numberOfState,self.numberOfTime,self.numberOfGen,self.numberOfPiece))
			k=self.idxPPieceGen
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for g in range(self.numberOfGen):
						for p in range(self.numberOfPiece):
							self.PPieceGen[s,t,g,p]=self.solution.get_values(k)
							k+=1
			self.PPieceFlag=np.zeros((self.numberOfState,self.numberOfTime,self.numberOfGen,self.numberOfPiece))
			k=self.idxPPieceFlag
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for g in range(self.numberOfGen):
						for p in range(self.numberOfPiece):
							self.PPieceFlag[s,t,g,p]=self.solution.get_values(k)
							k+=1

		if 'consStairwiseCost' in self.consList:
			self.CountDown=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxCountDown
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.CountDown[g,t]=self.solution.get_values(k)
					k+=1

			self.HotStart=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxHS
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.HotStart[g,t]=self.solution.get_values(k)
					k+=1

			self.ColdStart=np.zeros((self.numberOfGen,self.numberOfTime))
			k=self.idxCS
			for t in range(self.numberOfTime):
				for g in range(self.numberOfGen):
					self.ColdStart[g,t]=self.solution.get_values(k)
					k+=1

		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
				self.RSROut=np.zeros((self.numberOfState,self.numberOfGen,self.numberOfTime))
				k=self.idxRSR
				for s in range(self.numberOfState):
					for t in range(self.numberOfTime):
						for g in range(self.numberOfGen):
							self.RSROut[s,g,t]=self.solution.get_values(k)
							k+=1

		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			self.RPrOut=np.zeros((self.numberOfState,self.numberOfGen,self.numberOfTime))
			k=self.idxRPr
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for g in range(self.numberOfGen):
						self.RPrOut[s,g,t]=self.solution.get_values(k)
						k+=1

		if 'consDCPF' in self.consList:
			self.PBusOut=np.zeros((self.numberOfState,self.numberOfBus,self.numberOfTime))
			k=self.idxPBus
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for bus in range(self.numberOfBus):
						self.PBusOut[s,bus,t]=self.solution.get_values(k)
						k+=1

			self.ThetaOut=np.zeros((self.numberOfState,self.numberOfBus,self.numberOfTime))
			k=self.idxTheta
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for bus in range(self.numberOfBus):
						self.ThetaOut[s,bus,t]=self.solution.get_values(k)
						k+=1

			self.LineLoadOut=np.zeros((self.numberOfState,self.numberOfBranch,self.numberOfTime))
			k=self.idxLineLoad
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for branch in range(self.numberOfBranch):
						self.LineLoadOut[s,branch,t]=self.solution.get_values(k)
						k+=1
		if 'consCongestionPr' in self.consList:
			self.PBusPrOut=np.zeros((self.numberOfState,self.numberOfBus,self.numberOfTime))
			k=self.idxPBusPr
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for bus in range(self.numberOfBus):
						self.PBusPrOut[s,bus,t]=self.solution.get_values(k)
						k+=1

			self.ThetaPrOut=np.zeros((self.numberOfState,self.numberOfBus,self.numberOfTime))
			k=self.idxThetaPr
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for bus in range(self.numberOfBus):
						self.ThetaPrOut[s,bus,t]=self.solution.get_values(k)
						k+=1

			self.LineLoadPrOut=np.zeros((self.numberOfState,self.numberOfBranch,self.numberOfTime))
			k=self.idxLineLoadPr
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for branch in range(self.numberOfBranch):
						self.LineLoadPrOut[s,branch,t]=self.solution.get_values(k)
						k+=1

		if any(i in['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
			self.ChargeStatus=np.zeros((self.numberOfBattery,self.numberOfTime))
			k=self.idxChargeStatus
			for t in range(self.numberOfTime):
				for battery in range(self.numberOfBattery):
					self.ChargeStatus[battery,t]=self.solution.get_values(k)
					k+=1

			self.DischargeStatus=np.zeros((self.numberOfBattery,self.numberOfTime))
			k=self.idxDischargeStatus
			for t in range(self.numberOfTime):
				for battery in range(self.numberOfBattery):
					self.DischargeStatus[battery,t]=self.solution.get_values(k)
					k+=1

			self.ChargePower=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxChargePower
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.ChargePower[s,battery,t]=self.solution.get_values(k)
						k+=1

			self.DischargePower=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxDischargePower
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.DischargePower[s,battery,t]=self.solution.get_values(k)
						k+=1

			self.SOC=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxSOC
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.SOC[s,battery,t]=self.solution.get_values(k)
						k+=1

			self.SOCPrev=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxSOCPrev
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.SOCPrev[s,battery,t]=self.solution.get_values(k)
						k+=1
		
		if 'consBatteryAsPVDummyLoad' in self.consList:
			self.PVU=np.zeros((self.numberOfState,self.numberOfTime))
			k=self.idxPVU
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					self.PVU[s,t]=self.solution.get_values(k)
					k+=1
			
			self.ChargePowerFromPV=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxChargePowerFromPV
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.ChargePowerFromPV[s,battery,t]=self.solution.get_values(k)
						k+=1

		if 'consBatteryAsReserve' in self.consList:	
			self.RSt=np.zeros((self.numberOfState,self.numberOfBattery,self.numberOfTime))
			k=self.idxRSt
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for battery in range(self.numberOfBattery):
						self.RSt[s,battery,t]=self.solution.get_values(k)
						k+=1

		if 'consPHS' in self.consList:
			self.PumpStatus=np.zeros((self.numberOfPHS,self.numberOfTime))
			k=self.idxPumpStatus
			for t in range(self.numberOfTime):
				for phs in range(self.numberOfPHS):
					self.PumpStatus[phs,t]=self.solution.get_values(k)
					k+=1

			self.GenerateStatus=np.zeros((self.numberOfPHS,self.numberOfTime))
			k=self.idxGenerateStatus
			for t in range(self.numberOfTime):
				for phs in range(self.numberOfPHS):
					self.GenerateStatus[phs,t]=self.solution.get_values(k)
					k+=1

			self.PumpPower=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
			k=self.idxPumpPower
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.PumpPower[s,phs,t]=self.solution.get_values(k)
						k+=1

			self.GeneratePower=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
			k=self.idxGeneratePower
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.GeneratePower[s,phs,t]=self.solution.get_values(k)
						k+=1

			self.UR=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
			k=self.idxUR
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.UR[s,phs,t]=self.solution.get_values(k)
						k+=1

			self.URPrev=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
			k=self.idxURPrev
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.URPrev[s,phs,t]=self.solution.get_values(k)
						k+=1			
		if 'consRPrPHS' in self.consList:
			self.RPrPHSOut=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
			k=self.idxRPrPHS
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.RPrPHSOut[s,phs,t]=self.solution.get_values(k)
						k+=1
					self.SCRPHSG=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
		if 'consSCRPHS' in self.consList:	
			k=self.idxSCRPHSG
			for s in range(self.numberOfState):
				for t in range(self.numberOfTime):
					for phs in range(self.numberOfPHS):
						self.SCRPHSG[s,phs,t]=self.solution.get_values(k)
						k+=1
			if 'consFixedSpeedPHS' not in self.consList:
				self.SCRPHSP=np.zeros((self.numberOfState,self.numberOfPHS,self.numberOfTime))
				k=self.idxSCRPHSP
				for s in range(self.numberOfState):
					for t in range(self.numberOfTime):
						for phs in range(self.numberOfPHS):
							self.SCRPHSP[s,phs,t]=self.solution.get_values(k)
							k+=1
		pass

	def printOutput(self,decimal_place=2):
		if self.reshapeOutputFlag==0:
			self.reshapeOutput()
			
		# Print Output
		if 'consUC'in self.consList:
			print('UC Output:')
			print(self.ucOut.round())

			print('Power Output:')
			print(self.powerOut.round(decimal_place))

			print('Startup Output:')
			print(self.startUpOut.round())

			print('Shutdown Output:')
			print(self.shutDownOut.round())
		
		if all(i in ['consInit','consMUTMDT'] for i in self.consList):
			print('Initial Status, and Initial Power')
			print(np.vstack((self.initStatus,self.initPower)).transpose())    
		
		if 'consPiecewiseCost' in self.consList:
			print('Power self.numberOfPiece Output:')
			print(self.PPieceGen.round(decimal_place))
			print('Power self.numberOfPiece Flag Output:')
			print(self.PPieceFlag.round())
		
		if 'consStairwiseCost' in self.consList:
			print('Count Down:')
			print(self.CountDown.round())

			print('Hot Start:')
			print(self.HotStart.round())

			print('Cold Start:')
			print(self.ColdStart.round())
		
		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			print('R SR:')
			print(self.RSROut.round(decimal_place))
		
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			print('Reserve Steady Primary Output:')
			print(self.RPrOut.round(decimal_place))
					
		if 'consDCPF' in self.consList:
			print('self.numberOfBus Power Output:')
			print(self.PBusOut.round(decimal_place))

			print('self.numberOfBus Theta Output:')
			print(self.ThetaOut.round(decimal_place))

			print('self.numberOfBranch Line Load Output:')
			print(self.LineLoadOut.round(decimal_place))

		if 'consCongestionPr' in self.consList:
			print('self.numberOfBus Power Output:')
			print(self.PBusPrOut.round(decimal_place))

			print('self.numberOfBus Theta Output:')
			print(self.ThetaPrOut.round(decimal_place))

			print('self.numberOfBranch Line Load Output:')
			print(self.LineLoadPrOut.round(decimal_place))	
		
		if any (i in ['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
			print('self.ChargeStatus:')
			print(self.ChargeStatus.round())

			print('self.DischargeStatus:')
			print(self.DischargeStatus.round())

			print('self.ChargePower:')
			print(self.ChargePower.round(decimal_place))

			print('self.DischargePower:')
			print(self.DischargePower.round(decimal_place))

			print('self.SOC:')
			print(self.SOC.round(decimal_place))

			print('self.SOCPrev:')
			print(self.SOCPrev.round(decimal_place))
		
		if 'consBatteryAsPVDummyLoad' in self.consList:
			print('self.PVU:')
			print(self.PVU.round(decimal_place))

			print('self.ChargePowerFromPV:')
			print(self.ChargePowerFromPV.round(decimal_place))

		if 'consBatteryAsReserve' in self.consList:
			print('self.RSt:')
			print(self.RSt.round(decimal_place))
		
		if 'consPHS' in self.consList:
			print('self.PumpStatus:')
			print(self.PumpStatus.round())

			print('self.GenerateStatus:')
			print(self.GenerateStatus.round())

			print('self.PumpPower:')
			print(self.PumpPower.round(decimal_place))

			print('self.GeneratePower:')
			print(self.GeneratePower.round(decimal_place))

			print('self.UR:')
			print(self.UR.round(decimal_place))

			print('self.URPrev:')
			print(self.URPrev.round(decimal_place))

		if'consRPrPHS' in self.consList:
			print('self.RPrPHSOut:')
			print(self.RPrPHSOut.round(decimal_place))
		
		pass

	def partialCost(self,decimal_place=2):
		if self.partialCostFlag==1:
			return
		self.partialCostFlag=1
		self.totalCost=0

		if 'consUC'in self.consList:
			totalCostA=0
			totalCostB=0
			totalCostC=0
			totalCostPieceGradient=0
			if 'consPiecewiseCost' in self.consList:
				#xPiecePowerOut
				xPiecePowerOut=np.array(self.solution.get_values(self.idxPPieceGen,self.idxPPieceGen+self.numberOfPiece*self.numberOfGen*self.numberOfTime*self.numberOfState-1))
				
				#totalCostPieceGradient
				fuelCostMFixed=[]
				for probMultiplier in self.probList:
					fuelCostMFixed.extend((np.array(self.fuelCostM*self.numberOfTime)*probMultiplier).tolist())
				totalCostPieceGradient=np.matmul(fuelCostMFixed,xPiecePowerOut.transpose())
				print('totalCostPieceGradient')
				print(totalCostPieceGradient.round(decimal_place))
			else:
				#xPowerOut
				xPowerOut=np.array(self.solution.get_values(self.idxPGen,self.idxPGen+self.numberOfGen*self.numberOfTime*self.numberOfState-1))

				#totalCostA
				QMatrix=np.zeros([self.numberOfGen*self.numberOfTime*self.numberOfState,self.numberOfGen*self.numberOfTime*self.numberOfState])
				for s,probMultiplier in zip(range(self.numberOfState),self.probList):
					for key,value in zip(range(self.numberOfGen*self.numberOfTime),self.fuelCostA*self.numberOfTime*self.numberOfState):
						QMatrix[key+s*self.numberOfGen*self.numberOfTime,key+s*self.numberOfGen*self.numberOfTime]=value*probMultiplier
				totalCostA=np.matmul(np.matmul(xPowerOut,QMatrix),xPowerOut.transpose())
				print('totalCostA')
				print(totalCostA.round(decimal_place))

				#totalCostB
				fuelCostBFixed=[]
				for probMultiplier in self.probList:
					fuelCostBFixed.extend((np.array(self.fuelCostB*self.numberOfTime)*probMultiplier).tolist())
				totalCostB=np.matmul(fuelCostBFixed,xPowerOut.transpose())
				print('totalCostB')
				print(totalCostB.round(decimal_place))

			#xUCOut
			xUCOut=np.array(self.solution.get_values(self.idxUC,self.idxUC+self.numberOfGen*self.numberOfTime-1)).round()

			#totalCostC
			totalCostC=np.matmul(self.fuelCostC*self.numberOfTime,xUCOut.transpose())
			print('totalCostC')
			print(totalCostC.round(decimal_place))

			#totalCostABCPiece
			self.totalCostFuel=(totalCostA+totalCostB+totalCostC+totalCostPieceGradient).round(decimal_place)
			print('totalFuelCost = totalCostA + totalCostB + totalCostC + totalCostPieceGradient')
			print(self.totalCostFuel)
			
			#totalCostShutDown
			xShutDownOut=np.array(self.solution.get_values(self.idxSD,self.idxSD+self.numberOfGen*self.numberOfTime-1)).round()
			self.totalCostShutDown=np.matmul(self.shutDownCost*self.numberOfTime,xShutDownOut.transpose())
			print('Total Shutdown Cost')
			print(self.totalCostShutDown)

			if 'consStairwiseCost' in self.consList:
				#totalCostHotStart
				xHotStartOut=np.array(self.solution.get_values(self.idxHS,self.idxHS+self.numberOfGen*self.numberOfTime-1)).round()
				self.totalCostHotStart=np.matmul(self.startupCostHot*self.numberOfTime,xHotStartOut.transpose())
				print('Total Hot Startup Cost')
				print(self.totalCostHotStart)

				#totalCostColdStart
				xColdStartOut=np.array(self.solution.get_values(self.idxCS,self.idxCS+self.numberOfGen*self.numberOfTime-1)).round()
				self.totalCostColdStart=np.matmul(self.startupCostCold*self.numberOfTime,xColdStartOut.transpose())
				print('Total Cold Startup Cost')
				print(self.totalCostColdStart)

				self.totalCostStartup=self.totalCostHotStart+self.totalCostColdStart
			else:
				#totalCostStartup
				xStartupOut=np.array(self.solution.get_values(self.idxSU,self.idxSU+self.numberOfGen*self.numberOfTime-1)).round()
				self.totalCostStartup=np.matmul(self.startupCost*self.numberOfTime,xStartupOut.transpose())
			print('Total Startup Cost')
			print(self.totalCostStartup)

			self.totalCost=self.totalCost+(totalCostA+totalCostB+totalCostC+totalCostPieceGradient).round(decimal_place)+self.totalCostShutDown+self.totalCostStartup
		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			#totalCostSecondaryReserve
			xSpinningReserveOut=np.array(self.solution.get_values(self.idxRSR,self.idxRSR+self.numberOfState*self.numberOfGen*self.numberOfTime-1))
			secondaryReserveCostFixed=[]
			for probMultiplier in self.probList:
				secondaryReserveCostFixed.extend((np.array(self.secondaryReserveCost*self.numberOfTime)*probMultiplier).tolist())
			self.totalCostSecondaryReserve=np.matmul(secondaryReserveCostFixed,xSpinningReserveOut.transpose())
			print('totalCostSecondaryReserve')
			print(self.totalCostSecondaryReserve.round(decimal_place))

			self.totalCost=self.totalCost+self.totalCostSecondaryReserve.round(decimal_place)
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			xPrimaryReserveOut=np.array(self.solution.get_values(self.idxRPr,self.idxRPr+self.numberOfState*self.numberOfGen*self.numberOfTime-1))
			SteadyPrimaryReserveCostFixed=[]
			for probMultiplier in self.probList:
				SteadyPrimaryReserveCostFixed.extend((np.array(self.SteadyPrimaryReserveCost*self.numberOfTime)*probMultiplier).tolist())
			self.totalCostSteadyPrimaryReserve=np.matmul(SteadyPrimaryReserveCostFixed,xPrimaryReserveOut.transpose())
			
			print('totalCostSteadyPrimaryReserve')
			print(self.totalCostSteadyPrimaryReserve.round(decimal_place))

			self.totalCost=self.totalCost+self.totalCostSteadyPrimaryReserve.round(decimal_place)
		
		#Total Cost Comparison (for Debug)
		print('Manual Computation Total Cost: ')
		print(self.totalCost)
		print('CPLEX Computation Total Cost: ')
		self.totalCost_cplex=self.solution.get_objective_value()
		print(self.totalCost_cplex)
		pass

	def getSummaryDic(self,print_summary_dic=False,tol=1e-6):
		self.summaryDicFlag=1
		if self.partialCostFlag==0:
			self.partialCost()
		if self.reshapeOutputFlag==0:
			self.reshapeOutput()
		#Summary
		summaryDic={
			'Case Name':self.caseName,
			'Manual Computation Total Cost':self.totalCost,
			'CPLEX Computation Total Cost':self.solution.get_objective_value(),
			'Computation Time (sec)':self.computationTime,
			'Constraints':self.consList,
			'Number of Generators':self.numberOfGen,
			'Number of Hours (or Time Segments)':self.numberOfTime,
			'Number of State':self.numberOfState,
			'Total Fuel Cost':self.totalCostFuel,
			'Total Shut Down Cost':self.totalCostShutDown,
			'Total Startup Cost':self.totalCostStartup,
		}

		if 'consStairwiseCost' in self.consList:
			summaryDic['Hot Start Component in Startup']=self.totalCostHotStart
			summaryDic['Cold Start Component in Startup']=self.totalCostColdStart
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			summaryDic['Total Steady Primary Reserve Cost']=self.totalCostSteadyPrimaryReserve
		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			summaryDic['Total Secondary Reserve Cost']=self.totalCostSecondaryReserve

		self.summaryDic=summaryDic
		if print_summary_dic==True:
			print(self.summaryDic)
		pass

	def pandaExport(self,dF,folderPath,fileName,index=False):
		if type(dF).__module__ == np.__name__:
			dF=pd.DataFrame(dF)
		filePath=os.path.join(folderPath,fileName)
		dF.to_csv(filePath,index=False)
		pass

	def exportToCSV(self,outputPath=None,name_mark=False):
		if outputPath==None:
			self.getPath(name_mark=name_mark)
		else:
			self.outputPath=outputPath
		
		if name_mark==False:
			self.name_mark=''
		
		if not os.path.isdir(self.outputPath):
			os.makedirs(self.outputPath)
		
		if self.reshapeOutputFlag==0:
			self.reshapeOutput()
		if self.partialCostFlag==0:
			self.partialCost()
		
		if 'consUC'in self.consList:
			#UC
			#Make DataFrame From Numpy
			dF=pd.DataFrame(self.ucOut.round())

			#Export
			self.pandaExport(dF,self.outputPath,'UC'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#Dicpatch
			#Make DataFrame From Numpy
			temp = []
			for matrix in self.powerOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Dispatch'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#Total Cost
			#Make DataFrame From Float
			dF=pd.DataFrame([self.solution.get_objective_value()])
			
			#Export
			self.pandaExport(dF,self.outputPath,'Total Cost'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			pass
		if all(i in ['consInit','consMUTMDT'] for i in self.consList):
			pass
		if 'consPiecewiseCost' in self.consList:
			pass
		if 'consStairwiseCost' in self.consList:
			pass
		if any (i in ['consSRContingency','consSRPower','consSRPercentage'] for i in self.consList):
			#Spinning Reserve
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.RSROut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Spinning Reserve'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			pass
		if any (i in ['consWorstCaseInertia','consPrimaryDroop'] for i in self.consList):
			#Reserve Primary
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.RPrOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Reserve Primary'+'_'+self.caseName+'_'+self.name_mark+'.csv')
		if 'consDCPF' in self.consList:
			#Power Output
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.PBusOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Bus Power Output'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#Branch Line Load Output
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.LineLoadOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Branch Line Load Output'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			pass
		if 'consCongestionPr' in self.consList:
			#Power Output
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.PBusPrOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Bus Power Output Pasca Kontingensi'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#Branch Line Load Output
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.LineLoadPrOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Branch Line Load Output Pasca Kontingensi'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			pass
		if any (i in['consBatteryAsLoadLeveling','consBatteryAsPVDummyLoad'] for i in self.consList):
			#SOC
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.SOC:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'SOC'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#ChargePower
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.ChargePower:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'ChargePower'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			
			#DischargePower
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.DischargePower:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'Discharge Power'+'_'+self.caseName+'_'+self.name_mark+'.csv')

		if 'consPHS' in self.consList:
			#UR
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.UR:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'Upper Reservoir Volume'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#GenerateStatus
			#Make DataFrame From Numpy
			dF=pd.DataFrame(self.GenerateStatus.round())

			#Export
			self.pandaExport(dF,self.outputPath,'Gen Status'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#PumpStatus
			#Make DataFrame From Numpy
			dF=pd.DataFrame(self.PumpStatus.round())

			#Export
			self.pandaExport(dF,self.outputPath,'Pump Status'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#PumpPower
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.PumpPower:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'PumpPower'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			
			#GeneratePower
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.GeneratePower:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'Generate Power'+'_'+self.caseName+'_'+self.name_mark+'.csv')

		if 'consRPrPHS' in self.consList:
			#Reserve Primary PHS
			#Make Data Frame From Numpy
			temp= []
			for matrix in self.RPrPHSOut:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)

			#Export
			self.pandaExport(dF,self.outputPath,'Reserve Primary PHS'+'_'+self.caseName+'_'+self.name_mark+'.csv')
		
		if 'consSCRPHS' in self.consList:
			#SCR Gen
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.SCRPHSG:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'SCR PHS Mode Gen'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			if 'consFixedSpeedPHS' not in self.consList:
				#SCR Pump
				#Make Data Frame From Numpy
				temp = []
				for matrix in self.SCRPHSP:
					temp.extend(matrix)
					temp.extend([[] * len(matrix[0])])
				dF=pd.DataFrame(temp)
				#Export
				self.pandaExport(dF,self.outputPath,'SCR PHS Mode Pump'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			
		if 'consBatteryAsPVDummyLoad' in self.consList:
			#PVU
			#Make Data Frame From Numpy
			dF=pd.DataFrame(self.PVU)
			#Export
			self.pandaExport(dF,self.outputPath,'PVU'+'_'+self.caseName+'_'+self.name_mark+'.csv')

			#ChargePowerFromPV
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.ChargePowerFromPV:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'ChargePowerFromPV'+'_'+self.caseName+'_'+self.name_mark+'.csv')
			
		if 'consBatteryAsReserve' in self.consList:
			#RSt
			#Make Data Frame From Numpy
			temp = []
			for matrix in self.RSt:
				temp.extend(matrix)
				temp.extend([[] * len(matrix[0])])
			dF=pd.DataFrame(temp)
			#Export
			self.pandaExport(dF,self.outputPath,'RSt'+'_'+self.caseName+'_'+self.name_mark+'.csv')

		if self.summaryDicFlag==0:
			self.getSummaryDic()
		summaryDataFrame=pd.DataFrame.from_dict(self.summaryDic, orient='index')
		summaryDataFrame.to_csv(os.path.join(self.outputPath,'Summary '+'_'+self.caseName+'_'+self.name_mark+'.csv'),header=False)

		self.logPath_paste=os.path.join(self.outputPath,'log_UC'+'_'+self.name_mark+'.txt')
		if os.name == 'posix': #linux/unix
			os.system('cp "'+self.logPath+'" "'+self.logPath_paste+'"') 
		elif os.name == 'nt': #windows
			os.system('copy "'+self.logPath+'" "'+self.logPath_paste+'"')
		else:
			print('Log is not coppied because os is not Windows nor Linux!')
		pass

## Notes Start ##
	# UN_YM=0 #unitNumber
	# BL_YM=1 #busLocation
	# PMAX_YM=2 #pMax
	# PMIN_YM=3 #pMin
	# RU_YM=4 #hourlyRampUp
	# RD_YM=5 #hourlyRampDown
	# MUT_YM=6 #minimumUpTime
	# MDT_YM=7 #minumumDownTime
	# ACOST_YM=8 #secondOrderCost
	# BCOST_YM=9 #firstOrderCost
	# CCOST_YM=10 #zerothOrderCost
	# HSCOST_YM=11 #hotStasrtCost
	# CSCOST_YM=12 #coldStartCost
	# SDCOST_YM=13 #shutDownCost
	# HT_YM=14 #NT1 (maximumTimeForHotStart)
	# NT2_YM=15 #NT2
	# IP_YM=0 #initialPower
	# IS_YM=1 #initialStatus
	# UT_YM=2 #previousUpTime
	# DT_YM=3 #previousDownTime
	# LS_YM=0 #fuelLimitConstraint
	# MF_YM=1 #maximumFuelInOneRunTime
	# PRCOST_YM=0 #primaryReserveRateCost
	# TRCOST_YM=1 #tersiaryReserveRateCost
	# FDMIN_YM=2 #frequencyDeviationMin
	# FNOM_YM=3 #nominalFreq
	# RPMAX_YM=4 #rampUpUnderPrimaryRegulation
	# RTMAX_YM=5 #rampUpUnderTersiaryRegulation
	# R10_YM=6 #ramp10Minute
	# R30_YM=7 #ramp30Minute
	# RAGC_YM=8 #rampAGC
	# DRPERC_YM=9 #droopGen
	## Notes End ##