"""
Created on Mon Jul  4 15:21:18 2016

@author: Chang Yeon
"""

# SPP portfolio Value Investing strategy
#-------------------------------------------------------------------------------

# step1 Loading sector data

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sector = pd.read_excel("01.DG_Sector.xlsx")
sector.drop(sector.index[0:3], inplace=True)
sector = sector.T
sector.index = sector.pop('Currency') # Set index as Currency column
sector = sector.T
sector.rename(columns={'KRW': 'coname'}, inplace=True) # renaming KRW column to 'Company name'
sector = sector.sort_index(axis=0) # Sort by index(company code)
#-------------------------------------------------------------------------------
# step2 Loading Market Value data
MV = pd.read_excel("02.DG_Market_Value.xlsx") # unit: million won
MV = MV.T
MV.pop('Item') # delete Item column
MV.pop('Calendar Basis') # delete Calendar Basis column
MV.pop('Frequency')# delete Frequency column
MV.pop('Portfolio') # delete Portfolio column
MV.pop('Non-Trading Day') # delete Non-Trading Day column
MV.pop('Include Weekend') # delete Include Weekend column
MV.pop('Term') # delete Term column
MV.pop('Kind') # delete Kind column
MV.pop('Item Name') # delete Item Name column
MV.pop('Symbol Name') # delete Symbol Name column
MV.index = MV.pop('Symbol') # Set index as Symbol column
MV = MV.sort_index(axis=0) # Sort by index(company code)
MV = MV.T # transpose
MV = MV.replace({0 : np.nan}) # Repalce value of zero to NaN
MV = pd.DataFrame(MV, dtype='float64') # change datatype to float64
#-------------------------------------------------------------------------------
# step3 Loading Income Statement data
IS = pd.read_excel("03.DG_IS.xlsx")
IS = IS.T
IS.pop('Calendar Basis') # delete Calendar Basis column
IS.pop('Portfolio') # delete Portfolio column
IS.pop('Item') # delete Item column
IS.pop('Frequency')# delete Frequency column
IS.pop('Non-Trading Day') # delete Non-Trading Day column
IS.pop('Include Weekend') # delete Include Weekend column
IS.pop('Term') # delete Term column
IS.index = IS.pop('Symbol') # Set index as Symbol column
IS = IS.T #Transpose
IS.pop('Symbol Name') # delete Symbol Name column
IS.pop('Kind') # delete Kind column
IS.pop('Item Name ') # delete Item Name column
IS.pop('Frequency') # delete Frequency column
Sales = IS[IS.Item=="M000904001"] # Sales dataframe 생성
OP = IS[IS.Item=="M000906001"] # Operation Profit dataframe 생성
NI = IS[IS.Item=="M000908001"] # Net income dataframe 생성
Sales.pop('Item') # delete Item column
OP.pop('Item') # delete Item column
NI.pop('Item') # delete Item column
Sales = Sales.sort_index(axis=0) # Sort by index(company code)
OP = OP.sort_index(axis=0) # Sort by index(company code)
NI = NI.sort_index(axis=0) # Sort by index(company code)
Sales = Sales.T # transpose
OP = OP.T # transpose
NI = NI.T # transpose
Sales = pd.DataFrame(Sales, dtype='float64')
OP = pd.DataFrame(OP, dtype='float64')
NI = pd.DataFrame(NI, dtype='float64')

# step3-1 Loading Income Statement provisional data
ISprov = pd.read_excel("07.DG_ISprovisional.xlsx")
ISprov = ISprov.T
ISprov.pop('Calendar Basis') # delete Calendar Basis column
ISprov.pop('Portfolio') # delete Portfolio column
ISprov.pop('Item') # delete Item column
ISprov.pop('Frequency')# delete Frequency column
ISprov.pop('Non-Trading Day') # delete Non-Trading Day column
ISprov.pop('Include Weekend') # delete Include Weekend column
ISprov.pop('Term') # delete Term column
ISprov.index = ISprov.pop('Symbol') # Set index as Symbol column
ISprov = ISprov.T #Transpose
ISprov.pop('Symbol Name') # delete Symbol Name column
ISprov.pop('Kind') # delete Kind column
ISprov.pop('Item Name ') # delete Item Name column
ISprov.pop('Frequency') # delete Frequency column
Salesprov = ISprov[ISprov.Item=="FP70904001"] # Sales dataframe 생성
OPprov = ISprov[ISprov.Item=="FP70906001"] # Operation Profit dataframe 생성
NIprov = ISprov[ISprov.Item=="FP70908001"] # Net income dataframe 생성
Salesprov.pop('Item') # delete Item column
OPprov.pop('Item') # delete Item column
NIprov.pop('Item') # delete Item column
Salesprov = Salesprov.sort_index(axis=0) # Sort by index(company code)
OPprov = OPprov.sort_index(axis=0) # Sort by index(company code)
NIprov = NIprov.sort_index(axis=0) # Sort by index(company code)
Salesprov = Salesprov.T # transpose
OPprov = OPprov.T # transpose
NIprov = NIprov.T # transpose
Salesprov = pd.DataFrame(Salesprov*100000, dtype='float64')
OPprov = pd.DataFrame(OPprov*100000, dtype='float64')
NIprov = pd.DataFrame(NIprov*100000, dtype='float64')

# step3-2 combine Income Statement data and provisional data
Sales = pd.DataFrame(Sales.append(Salesprov), dtype='float64')
OP = pd.DataFrame(OP.append(OPprov), dtype='float64')
NI = pd.DataFrame(NI.append(NIprov), dtype='float64')

#-------------------------------------------------------------------------------
# step4 Loading Balance Sheet data
BS = pd.read_excel("05.DG_BS.xlsx")
BS = BS.T
BS.pop('Calendar Basis') # delete Calendar Basis column
BS.pop('Portfolio') # delete Portfolio column
BS.pop('Item') # delete Item column
BS.pop('Frequency')# delete Frequency column
BS.pop('Non-Trading Day') # delete Non-Trading Day column
BS.pop('Include Weekend') # delete Include Weekend column
BS.pop('Term') # delete Term column
BS.index = BS.pop('Symbol') # Set index as Symbol column
BS = BS.T #Transpose
BS.pop('Symbol Name') # delete Symbol Name column
BS.pop('Kind') # delete Kind column
BS.pop('Item Name ') # delete Item Name column
BS.pop('Frequency') # delete Frequency column
totalasset = BS[BS.Item=='M000901001'] # 총자산 dataframe 생성
totalliab = BS[BS.Item=='M000902001'] # 총부채 dataframe 생성
totalequity = BS[BS.Item=='M000903001'] # 총자본 dataframe 생성
totalasset.pop('Item') # delete Item column
totalliab.pop('Item') # delete Item column
totalequity.pop('Item') # delete Item column
totalasset = totalasset.sort_index(axis=0) # Sort by index(company code)
totalliab = totalliab.sort_index(axis=0) # Sort by index(company code)
totalequity = totalequity.sort_index(axis=0) # Sort by index(company code)
totalasset = totalasset.T # transpose
totalliab = totalliab.T # transpose
totalequity = totalequity.T # transpose
totalasset = pd.DataFrame(totalasset, dtype='float64')
totalliab = pd.DataFrame(totalliab, dtype='float64')
totalequity = pd.DataFrame(totalequity, dtype='float64')

#-------------------------------------------------------------------------------
# step5 Loading Price data
P = pd.read_excel("04.DG_Price.xlsx")
P = P.T
P.pop('Item') # delete Item column
P.pop('Calendar Basis') # delete Calendar Basis column
P.pop('Frequency')# delete Frequency column
P.pop('Portfolio') # delete Portfolio column
P.pop('Non-Trading Day') # delete Non-Trading Day column
P.pop('Include Weekend') # delete Include Weekend column
P.pop('Term') # delete Term column
P.pop('Kind') # delete Kind column
P.pop('Item Name') # delete Item Name column
P.pop('Symbol Name') # delete Symbol Name column
P.index = P.pop('Symbol') # Set index as Symbol column
P = P.sort_index(axis=0) # Sort by index(company code)
P = P.T # Transpose
P.replace({0 : np.nan}) # Repalce value of zero to NaN
'''
p500out = P.ix[-1] <= 500 # Find adjusted price that is less than 500 won 
df_out = df_out[df_out==True] # Indicate df_out dataframe as adjusted price is less than 500 won 
'''
#-------------------------------------------------------------------------------
# step8 Loading Cash Flow statement data
CF = pd.read_excel("06.DG_CF.xlsx")
CF = CF.T
CF.pop('Calendar Basis') # delete Calendar Basis column
CF.pop('Portfolio') # delete Portfolio column
CF.pop('Item') # delete Item column
CF.pop('Frequency')# delete Frequency column
CF.pop('Non-Trading Day') # delete Non-Trading Day column
CF.pop('Include Weekend') # delete Include Weekend column
CF.pop('Term') # delete Term column
CF.index = CF.pop('Symbol') # Set index as Symbol column
CF = CF.T #Transpose
CF.pop('Symbol Name') # delete Symbol Name column
CF.pop('Kind') # delete Kind column
CF.pop('Item Name ') # delete Item Name column
CF.pop('Frequency') # delete Frequency column
CFO = CF[CF.Item=="M000909001"] # Sales dataframe 생성
CFI = CF[CF.Item=="M000909015"] # Operation Profit dataframe 생성
CFF = CF[CF.Item=="M000909018"] # Net income dataframe 생성
CFO.pop('Item') # delete Item column
CFI.pop('Item') # delete Item column
CFF.pop('Item') # delete Item column
CFO = CFO.sort_index(axis=0) # Sort by index(company code)
CFI = CFI.sort_index(axis=0) # Sort by index(company code)
CFF = CFF.sort_index(axis=0) # Sort by index(company code)
CFO = CFO.T # transpose
CFI = CFI.T # transpose
CFF = CFF.T # transpose
CFO = pd.DataFrame(CFO, dtype='float64')
CFI = pd.DataFrame(CFI, dtype='float64')
CFF = pd.DataFrame(CFF, dtype='float64')
#-------------------------------------------------------------------------------
# step12 Loading transaction stop data
stop = pd.read_excel("08.DG_stop.xlsx")
stop = stop.T
stop.pop('Calendar Basis') # delete Calendar Basis column
stop.pop('Portfolio') # delete Portfolio column
stop.pop('Item') # delete Item column
stop.pop('Frequency')# delete Frequency column
stop.pop('Non-Trading Day') # delete Non-Trading Day column
stop.pop('Include Weekend') # delete Include Weekend column
stop.pop('Term') # delete Term column
stop.index = stop.pop('Symbol') # Set index as Symbol column
stop = stop.T #Transpose
stop.pop('Symbol Name') # delete Symbol Name column
stop.pop('Kind') # delete Kind column
stop.pop('Item') # delete Item column
stop.pop('Item Name ') # delete Item Name column
stop.pop('Frequency') # delete Frequency column
stop = stop.T #Transpose

#-------------------------------------------------------------------------------

#===============================================================================
monthlyindex = pd.date_range(start='20100101', end='20160901', freq='M') # 리밸런싱 날짜 조정해야함
dailyindex = pd.date_range(start='20100101', end='20160901', freq='D') # 리밸런싱 날짜 조정해야함
#===============================================================================



#-------------------------------------------------------------------------------
# Step6 Calculate PER4Q monthly

# NI4Q
NI4Q = NI+NI.shift(1)+NI.shift(2)+NI.shift(3) # Create 4 quarter accumulated net income(NI4Q)
NI4Q = NI4Q.reindex(monthlyindex) # reindexing to monthly data
NI4Q = NI4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# OP4Q
OP4Q = OP+OP.shift(1)+OP.shift(2)+OP.shift(3)
OP4Q = OP4Q.reindex(monthlyindex) # reindexing to monthly data
OP4Q = OP4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# Sales4Q
Sales4Q = Sales+Sales.shift(1)+Sales.shift(2)+Sales.shift(3)
Sales4Q = Sales4Q.reindex(monthlyindex) # reindexing to monthly data
Sales4Q = Sales4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# Monthly market value
size = MV.reindex(monthlyindex) # market value 단위는 백만원 IS 단위는 천원

# PER4QNI
PER4QNI = size.div(NI4Q.shift(3), fill_value=None)*1000 # calculate PER4Q(Market value diveded by 4 quarter accumulated net income(NI4Q))

# PER4QOP
PER4QOP = size.div(OP4Q.shift(3), fill_value=None)*1000 # calculate PER4Q(Market value diveded by 4 quarter accumulated net income(NI4Q))

#-------------------------------------------------------------------------------
# Step7 Calculate PBR
totalequity = totalequity.reindex(monthlyindex)
totalequity = totalequity .fillna(method='ffill') # fill NaN values using the forward fill method
totalasset = totalasset.reindex(monthlyindex)
totalasset = totalasset.fillna(method='ffill')
totalliab = totalliab.reindex(monthlyindex)
totalliab = totalliab.fillna(method='ffill')

PBR = size.div(totalequity.shift(3), fill_value=None)*1000 # calculate PBR(Market value diveded by totalequity)

#-------------------------------------------------------------------------------

# Step9 Calculate CFO4Q monthly
# CFO4Q
CFO4Q = CFO+CFO.shift(1)+CFO.shift(2)+CFO.shift(3) # Create 4 quarter accumulated net income(CFO4Q)
CFO4Q = CFO4Q.reindex(monthlyindex) # reindexing to monthly data
CFO4Q = CFO4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# CFI4Q
CFI4Q = CFI+CFI.shift(1)+CFI.shift(2)+CFI.shift(3)
CFI4Q = CFI4Q.reindex(monthlyindex) # reindexing to monthly data
CFI4Q = CFI4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# CFF4Q
CFF4Q = CFF+CFF.shift(1)+CFF.shift(2)+CFF.shift(3)
CFF4Q = CFF4Q.reindex(monthlyindex) # reindexing to monthly data
CFF4Q = CFF4Q.fillna(method='ffill') # fill NaN values using the forward fill method

# PCR4Q
PCR4Q = size.div(CFO4Q.shift(3), fill_value=None)*1000 # calculate PCR4Q(Market value diveded by 4 quarter accumulated CFO(CFO4Q))


#-------------------------------------------------------------------------------
# step10 Calculate Return
monthlyP = P.reindex(monthlyindex)
monthlyP = monthlyP.append(P.ix[0])
monthlyP = monthlyP.sort_index()

before1monthR = monthlyP/monthlyP.shift(1)-1
after1monthR = monthlyP.shift(-1)/monthlyP-1

'''

twoM_Return = monthlyP.shift(-2)/monthlyP-1
threeM_Return = monthlyP.shift(-3)/monthlyP-1
fourM_Return = monthlyP.shift(-4)/monthlyP-1
fiveM_Return = monthlyP.shift(-5)/monthlyP-1
sixM_Return = monthlyP.shift(-6)/monthlyP-1
oneY_Return = monthlyP.shift(-12)/monthlyP-1
twoY_Return = monthlyP.shift(-24)/monthlyP-1
'''
#dailyR = P/P.shift(1)-1

#-------------------------------------------------------------------------------
# step 11 calculate ROE ROA RoS DR

ROE_NI = NI4Q.shift(3)/totalequity.shift(3)
ROE_OP = OP4Q.shift(3)/totalequity.shift(3)

ROA_NI = NI4Q.shift(3)/totalasset.shift(3)
ROA_OP = OP4Q.shift(3)/totalasset.shift(3)

RoS_NI = NI4Q.shift(3)/Sales4Q.shift(3)
RoS_OP = OP4Q.shift(3)/Sales4Q.shift(3)

DR = totalliab.shift(3)/totalequity.shift(3)

#-------------------------------------------------------------------------------
# Drawdown
# before running this area, run step4 price data
window = 180 # range of days that of calculated maximum
#
Pmax = pd.rolling_max(P, window, min_periods=1) # calculate maximum value of stocks that of range for window
dd = P / Pmax - 1.0 # calculate drawdown of each stocks
mdd = dd.min() # maximum drawdown
dd = dd.reindex(monthlyindex) # reindexing to monthly data


#=======================================================================================#
#                                                                                       #
# Edited by Chang Yeon Lee                                                              #
#                                                                                       #
#=======================================================================================#




'''
#-------------------------------------------------------------------------------
# Drawdown
# before running this area, run step4 price data


#-------------------------------------------------------------------------------
highp= pd.read_excel("09.DG_highPrice.xlsx")
highp = highp.T
highp.pop('Item') # delete Item column
highp.pop('Calendar Basis') # delete Calendar Basis column
highp.pop('Frequency')# delete Frequency column
highp.pop('Portfolio') # delete Portfolio column
highp.pop('Non-Trading Day') # delete Non-Trading Day column
highp.pop('Include Weekend') # delete Include Weekend column
highp.pop('Term') # delete Term column
highp.pop('Kind') # delete Kind column
highp.pop('Item Name') # delete Item Name column
highp.pop('Symbol Name') # delete Symbol Name column
highp.index = highp.pop('Symbol') # Set index as Symbol column
highp = highp.sort_index(axis=0) # Sort by index(company code)
highp = highp.T # Transpose
highp.replace({0 : np.nan}) # Repalce value of zero to NaN

#-------------------------------------------------------------------------------
# set window
window = 30 # calculated number of days from today

Pmax = pd.rolling_max(highp, window, min_periods=1) # calculate maximum value of stocks that of range for window
dd = P / Pmax - 1.0 # calculate drawdown of each stocks
mdd = dd.min() # maximum drawdown
dd = dd.T

#-------------------------------------------------------------------------------
# calculate Drawdown by Sector
dd['FGSC'] = sector['CP10000500']# add FGSC column to the Drawdown DataFrame
dd['BM'] = sector['CP10001210']
ddsmall = dd[dd.BM == 'KOSDAQ SMALL']
ddsmall.pop('BM')
# divide sector
ddFGSC10 = ddsmall[ddsmall.FGSC == "FGSC.10"]
ddFGSC15 = ddsmall[ddsmall.FGSC == "FGSC.15"]
ddFGSC20 = ddsmall[ddsmall.FGSC == "FGSC.20"]
ddFGSC25 = ddsmall[ddsmall.FGSC == "FGSC.25"]
ddFGSC30 = ddsmall[ddsmall.FGSC == "FGSC.30"]
ddFGSC35 = ddsmall[ddsmall.FGSC == "FGSC.35"]
ddFGSC40 = ddsmall[ddsmall.FGSC == "FGSC.40"]
ddFGSC45 = ddsmall[ddsmall.FGSC == "FGSC.45"]
ddFGSC50 = ddsmall[ddsmall.FGSC == "FGSC.50"]
ddFGSC55 = ddsmall[ddsmall.FGSC == "FGSC.55"]
# drop value of NaN 
ddFGSC10.dropna(inplace=True) 
ddFGSC15.dropna(inplace=True)
ddFGSC20.dropna(inplace=True)
ddFGSC25.dropna(inplace=True)
ddFGSC30.dropna(inplace=True)
ddFGSC35.dropna(inplace=True)
ddFGSC40.dropna(inplace=True)
ddFGSC45.dropna(inplace=True)
ddFGSC50.dropna(inplace=True)
ddFGSC55.dropna(inplace=True)
# drop FGSC
ddFGSC10.pop('FGSC')
ddFGSC15.pop('FGSC')
ddFGSC20.pop('FGSC')
ddFGSC25.pop('FGSC')
ddFGSC30.pop('FGSC')
ddFGSC35.pop('FGSC')
ddFGSC40.pop('FGSC')
ddFGSC45.pop('FGSC')
ddFGSC50.pop('FGSC')
ddFGSC55.pop('FGSC')
# transpose
ddFGSC10 = ddFGSC10.T 
ddFGSC15 = ddFGSC15.T
ddFGSC20 = ddFGSC20.T
ddFGSC25 = ddFGSC25.T
ddFGSC30 = ddFGSC30.T
ddFGSC35 = ddFGSC35.T
ddFGSC40 = ddFGSC40.T
ddFGSC45 = ddFGSC45.T
ddFGSC50 = ddFGSC50.T
ddFGSC55 = ddFGSC55.T

ddFGSC10mean = ddFGSC10.mean(axis=1)
ddFGSC15mean = ddFGSC15.mean(axis=1)
ddFGSC20mean = ddFGSC20.mean(axis=1)
ddFGSC25mean = ddFGSC25.mean(axis=1)
ddFGSC30mean = ddFGSC30.mean(axis=1)
ddFGSC35mean = ddFGSC35.mean(axis=1)
ddFGSC40mean = ddFGSC40.mean(axis=1)
ddFGSC45mean = ddFGSC45.mean(axis=1)
ddFGSC50mean = ddFGSC50.mean(axis=1)
ddFGSC55mean = ddFGSC55.mean(axis=1)

# plotting
plt.plot(ddFGSC45mean, 'r-')
plt.legend(['FGSC45'], fontsize=10)
plt.show()

print('----- Mean of Drawdown -------')
print('FGSC15: {0:.2%}'.format(ddFGSC15mean.mean()))
print('FGSC20: {0:.2%}'.format(ddFGSC20mean.mean()))
print('FGSC25: {0:.2%}'.format(ddFGSC25mean.mean()))
print('FGSC30: {0:.2%}'.format(ddFGSC30mean.mean()))
print('FGSC35: {0:.2%}'.format(ddFGSC35mean.mean()))
print('FGSC45: {0:.2%}'.format(ddFGSC45mean.mean()))

print('----- Max Drawdown -------')
print('FGSC15: {0:.2%}'.format(ddFGSC15mean.min()))
print('FGSC20: {0:.2%}'.format(ddFGSC20mean.min()))
print('FGSC25: {0:.2%}'.format(ddFGSC25mean.min()))
print('FGSC30: {0:.2%}'.format(ddFGSC30mean.min()))
print('FGSC35: {0:.2%}'.format(ddFGSC35mean.min()))
print('FGSC45: {0:.2%}'.format(ddFGSC45mean.min()))
'''

#=======================================================================================#
#=======================================================================================#
#=======================================================================================#
#=======================================================================================#
#=======================================================================================#


# monthly Rebalancing 


#=======================================================================================#
#=======================================================================================#
t0 = time.time()

#target dataframe
#target=pd.DataFrame()
'''
targetP10 = pd.DataFrame()
targetP15 = pd.DataFrame()
targetP20 = pd.DataFrame()
targetP25 = pd.DataFrame()
targetP30 = pd.DataFrame()
targetP35 = pd.DataFrame()
targetP40 = pd.DataFrame()
targetP45 = pd.DataFrame()
targetP50 = pd.DataFrame()
targetP55 = pd.DataFrame()
'''
tgtrtn = pd.DataFrame()
tgt10rtn = pd.DataFrame()
tgt15rtn = pd.DataFrame()
tgt20rtn = pd.DataFrame()
tgt25rtn = pd.DataFrame()
tgt30rtn = pd.DataFrame()
tgt35rtn = pd.DataFrame()
tgt40rtn = pd.DataFrame()
tgt45rtn = pd.DataFrame()
tgt50rtn = pd.DataFrame()
tgt55rtn = pd.DataFrame()
#===================================================================

# create empty rtn0 dataframe of rate of return for each sector
seb10rtn = pd.DataFrame()
seb15rtn = pd.DataFrame()
seb20rtn = pd.DataFrame()
seb25rtn = pd.DataFrame()
seb30rtn = pd.DataFrame()
seb35rtn = pd.DataFrame()
seb40rtn = pd.DataFrame()
seb45rtn = pd.DataFrame()
seb50rtn = pd.DataFrame()
seb55rtn = pd.DataFrame()

#======================================================================================
# create empty dataframe of total stocks for each sector

seb10total = pd.DataFrame()
seb15total = pd.DataFrame()
seb20total = pd.DataFrame()
seb25total = pd.DataFrame()
seb30total = pd.DataFrame()
seb35total = pd.DataFrame()
seb40total = pd.DataFrame()
seb45total = pd.DataFrame()
seb50total = pd.DataFrame()
seb55total = pd.DataFrame()
#=================================================================

#======================================================================================
for date in size.index:
    temp = size[size.index==date]
    temp = temp.T
    temp.rename(columns={date : 'size'}, inplace=True)
    temp['sector'] = sector['CP10000500']
    temp['PER4QNI'] = PER4QNI[PER4QNI.index==date].T
    temp['PBR'] = PBR[PBR.index==date].T
    temp['fdate'] = date
    temp['coname'] = sector['coname']
    temp['price'] = P[P.index==date].T
    temp['Total Asset'] = totalasset[totalasset.index==date].T
    temp['Total Liab'] = totalliab[totalliab.index==date].T
    temp['Total Equity'] = totalequity[totalequity.index==date].T
    temp['NI4Q']= NI4Q[NI4Q.index==date].T
    temp['before1monthR'] = before1monthR[before1monthR.index==date].T
    temp['after1monthR'] = after1monthR[after1monthR.index==date].T
#    temp['2M_Rtn'] = twoM_Return[twoM_Return.index==date].T
#    temp['3M_Rtn'] = threeM_Return[threeM_Return.index==date].T
#    temp['4M_Rtn'] = fourM_Return[fourM_Return.index==date].T
#    temp['5M_Rtn'] = fiveM_Return[fiveM_Return.index==date].T
#    temp['6M_Rtn'] = sixM_Return[sixM_Return .index==date].T
#    temp['1Yr_Rtn'] = oneY_Return[oneY_Return.index==date].T
#    temp['2Yr_Rtn'] = twoY_Return[twoY_Return.index==date].T
    temp['ROE_NI'] = ROE_NI[ROE_NI.index==date].T
    temp['ROE_OP'] = ROE_OP[ROE_OP.index==date].T
    temp['ROA_NI'] = ROA_NI[ROA_NI.index==date].T
    temp['ROA_OP'] = ROA_OP[ROA_OP.index==date].T
    temp['RoS_OP'] = RoS_OP[RoS_OP.index==date].T
    temp['RoS_NI'] = RoS_NI[RoS_NI.index==date].T
    temp['PCR4Q'] = PCR4Q[PCR4Q.index==date].T
    temp['drawdown'] = dd[dd.index==date].T
    temp['DR'] = DR[DR.index==date].T
    temp['vaild'] = temp['size'] > 0 
    temp['size5'] = (temp['size'].rank() > np.size(temp.index)*0.05)
    temp['p500'] = temp['price'] > 500 # stocks which for price below 500 won
    temp['stop'] = stop[stop.index==date].T    
    temp = temp[temp.vaild == True] # 1st eliminate stocks which for not vaild    
    temp = temp[temp.size5 == True] # 2nd eliminate stocks which for market vaule below 5% of total market
    temp = temp[temp.p500 == True] # 3rd eliminate stocks which for price below 500
    temp = temp[temp.stop == "정상"] # 4th eliminate stocks which for transaction stop    
#===========================================================================================
#===========================================================================================
#===========================================================================================
#===========================================================================================    
    # sector 구분
    temp10 = pd.DataFrame(temp[temp.sector=="FGSC.10"]) # FGSC.10 에너지 dataframe 생성
    temp15 = pd.DataFrame(temp[temp.sector=="FGSC.15"]) # FGSC.15 소재 dataframe 생성
    temp20 = pd.DataFrame(temp[temp.sector=="FGSC.20"]) # FGSC.20 산업재 dataframe 생성
    temp25 = pd.DataFrame(temp[temp.sector=="FGSC.25"]) # FGSC.25 경기소비재 dataframe 생성
    temp30 = pd.DataFrame(temp[temp.sector=="FGSC.30"]) # FGSC.30 필수소비재 dataframe 생성
    temp35 = pd.DataFrame(temp[temp.sector=="FGSC.35"]) # FGSC.35 의료 dataframe 생성
    temp40 = pd.DataFrame(temp[temp.sector=="FGSC.40"]) # FGSC.40 금융 dataframe 생성
    temp45 = pd.DataFrame(temp[temp.sector=="FGSC.45"]) # FGSC.45 IT dataframe 생성
    temp50 = pd.DataFrame(temp[temp.sector=="FGSC.50"]) # FGSC.50 통신서비스 dataframe 생성
    temp55 = pd.DataFrame(temp[temp.sector=="FGSC.55"]) # FGSC.55 유틸리티 dataframe 생성    

    # size ranking 
    temp10['sizerank'] = temp10['size'].rank()
    temp15['sizerank'] = temp15['size'].rank()
    temp20['sizerank'] = temp20['size'].rank()
    temp25['sizerank'] = temp25['size'].rank()
    temp30['sizerank'] = temp30['size'].rank()
    temp35['sizerank'] = temp35['size'].rank()
    temp40['sizerank'] = temp40['size'].rank()
    temp45['sizerank'] = temp45['size'].rank()
    temp50['sizerank'] = temp50['size'].rank()
    temp55['sizerank'] = temp55['size'].rank()

    # negative per
    temp10['pernega'] = np.where(temp10['PER4QNI'] > 0, temp10['PER4QNI'].rank(), np.NAN)
    temp15['pernega'] = np.where(temp15['PER4QNI'] > 0, temp15['PER4QNI'].rank(), np.NAN)
    temp20['pernega'] = np.where(temp20['PER4QNI'] > 0, temp20['PER4QNI'].rank(), np.NAN)
    temp25['pernega'] = np.where(temp25['PER4QNI'] > 0, temp25['PER4QNI'].rank(), np.NAN)
    temp30['pernega'] = np.where(temp30['PER4QNI'] > 0, temp30['PER4QNI'].rank(), np.NAN)
    temp35['pernega'] = np.where(temp35['PER4QNI'] > 0, temp35['PER4QNI'].rank(), np.NAN)
    temp40['pernega'] = np.where(temp40['PER4QNI'] > 0, temp40['PER4QNI'].rank(), np.NAN)
    temp45['pernega'] = np.where(temp45['PER4QNI'] > 0, temp45['PER4QNI'].rank(), np.NAN)
    temp50['pernega'] = np.where(temp50['PER4QNI'] > 0, temp50['PER4QNI'].rank(), np.NAN)
    temp55['pernega'] = np.where(temp55['PER4QNI'] > 0, temp55['PER4QNI'].rank(), np.NAN)

    # negative pbr
    temp10['pbrnega'] = np.where(temp10['PBR'] > 0, temp10['PBR'].rank(), np.NAN)
    temp15['pbrnega'] = np.where(temp15['PBR'] > 0, temp15['PBR'].rank(), np.NAN)
    temp20['pbrnega'] = np.where(temp20['PBR'] > 0, temp20['PBR'].rank(), np.NAN)
    temp25['pbrnega'] = np.where(temp25['PBR'] > 0, temp25['PBR'].rank(), np.NAN)
    temp30['pbrnega'] = np.where(temp30['PBR'] > 0, temp30['PBR'].rank(), np.NAN)
    temp35['pbrnega'] = np.where(temp35['PBR'] > 0, temp35['PBR'].rank(), np.NAN)
    temp40['pbrnega'] = np.where(temp40['PBR'] > 0, temp40['PBR'].rank(), np.NAN)
    temp45['pbrnega'] = np.where(temp45['PBR'] > 0, temp45['PBR'].rank(), np.NAN)
    temp50['pbrnega'] = np.where(temp50['PBR'] > 0, temp50['PBR'].rank(), np.NAN)
    temp55['pbrnega'] = np.where(temp55['PBR'] > 0, temp55['PBR'].rank(), np.NAN)

    # negative PCR4Q
    temp10['PCR4Qnega'] = np.where(temp10['PCR4Q'] > 0, temp10['PCR4Q'].rank(), np.NAN)
    temp15['PCR4Qnega'] = np.where(temp15['PCR4Q'] > 0, temp15['PCR4Q'].rank(), np.NAN)
    temp20['PCR4Qnega'] = np.where(temp20['PCR4Q'] > 0, temp20['PCR4Q'].rank(), np.NAN)
    temp25['PCR4Qnega'] = np.where(temp25['PCR4Q'] > 0, temp25['PCR4Q'].rank(), np.NAN)
    temp30['PCR4Qnega'] = np.where(temp30['PCR4Q'] > 0, temp30['PCR4Q'].rank(), np.NAN)
    temp35['PCR4Qnega'] = np.where(temp35['PCR4Q'] > 0, temp35['PCR4Q'].rank(), np.NAN)
    temp40['PCR4Qnega'] = np.where(temp40['PCR4Q'] > 0, temp40['PCR4Q'].rank(), np.NAN)
    temp45['PCR4Qnega'] = np.where(temp45['PCR4Q'] > 0, temp45['PCR4Q'].rank(), np.NAN)
    temp50['PCR4Qnega'] = np.where(temp50['PCR4Q'] > 0, temp50['PCR4Q'].rank(), np.NAN)
    temp55['PCR4Qnega'] = np.where(temp55['PCR4Q'] > 0, temp55['PCR4Q'].rank(), np.NAN)

    # PER ranking
    temp10['perrank'] = np.where(temp10['pernega'] != np.NAN, temp10['pernega'].rank(), np.NAN)
    temp15['perrank'] = np.where(temp15['pernega'] != np.NAN, temp15['pernega'].rank(), np.NAN)
    temp20['perrank'] = np.where(temp20['pernega'] != np.NAN, temp20['pernega'].rank(), np.NAN)
    temp25['perrank'] = np.where(temp25['pernega'] != np.NAN, temp25['pernega'].rank(), np.NAN)
    temp30['perrank'] = np.where(temp30['pernega'] != np.NAN, temp30['pernega'].rank(), np.NAN)
    temp35['perrank'] = np.where(temp35['pernega'] != np.NAN, temp35['pernega'].rank(), np.NAN)
    temp40['perrank'] = np.where(temp40['pernega'] != np.NAN, temp40['pernega'].rank(), np.NAN)
    temp45['perrank'] = np.where(temp45['pernega'] != np.NAN, temp45['pernega'].rank(), np.NAN)
    temp50['perrank'] = np.where(temp50['pernega'] != np.NAN, temp50['pernega'].rank(), np.NAN)
    temp55['perrank'] = np.where(temp55['pernega'] != np.NAN, temp55['pernega'].rank(), np.NAN)
    
    # PBR ranking
    temp10['pbrrank'] = np.where(temp10['pbrnega'] != np.NAN, temp10['pbrnega'].rank(), np.NAN)
    temp15['pbrrank'] = np.where(temp15['pbrnega'] != np.NAN, temp15['pbrnega'].rank(), np.NAN)
    temp20['pbrrank'] = np.where(temp20['pbrnega'] != np.NAN, temp20['pbrnega'].rank(), np.NAN)
    temp25['pbrrank'] = np.where(temp25['pbrnega'] != np.NAN, temp25['pbrnega'].rank(), np.NAN)
    temp30['pbrrank'] = np.where(temp30['pbrnega'] != np.NAN, temp30['pbrnega'].rank(), np.NAN)
    temp35['pbrrank'] = np.where(temp35['pbrnega'] != np.NAN, temp35['pbrnega'].rank(), np.NAN)
    temp40['pbrrank'] = np.where(temp40['pbrnega'] != np.NAN, temp40['pbrnega'].rank(), np.NAN)
    temp45['pbrrank'] = np.where(temp45['pbrnega'] != np.NAN, temp45['pbrnega'].rank(), np.NAN)
    temp50['pbrrank'] = np.where(temp50['pbrnega'] != np.NAN, temp50['pbrnega'].rank(), np.NAN)
    temp55['pbrrank'] = np.where(temp55['pbrnega'] != np.NAN, temp55['pbrnega'].rank(), np.NAN)
    
    # PCR4Q ranking
    temp10['PCR4Qrank'] = np.where(temp10['PCR4Qnega'] != np.NAN, temp10['PCR4Qnega'].rank(), np.NAN)
    temp15['PCR4Qrank'] = np.where(temp15['PCR4Qnega'] != np.NAN, temp15['PCR4Qnega'].rank(), np.NAN)
    temp20['PCR4Qrank'] = np.where(temp20['PCR4Qnega'] != np.NAN, temp20['PCR4Qnega'].rank(), np.NAN)
    temp25['PCR4Qrank'] = np.where(temp25['PCR4Qnega'] != np.NAN, temp25['PCR4Qnega'].rank(), np.NAN)
    temp30['PCR4Qrank'] = np.where(temp30['PCR4Qnega'] != np.NAN, temp30['PCR4Qnega'].rank(), np.NAN)
    temp35['PCR4Qrank'] = np.where(temp35['PCR4Qnega'] != np.NAN, temp35['PCR4Qnega'].rank(), np.NAN)
    temp40['PCR4Qrank'] = np.where(temp40['PCR4Qnega'] != np.NAN, temp40['PCR4Qnega'].rank(), np.NAN)
    temp45['PCR4Qrank'] = np.where(temp45['PCR4Qnega'] != np.NAN, temp45['PCR4Qnega'].rank(), np.NAN)
    temp50['PCR4Qrank'] = np.where(temp50['PCR4Qnega'] != np.NAN, temp50['PCR4Qnega'].rank(), np.NAN)
    temp55['PCR4Qrank'] = np.where(temp55['PCR4Qnega'] != np.NAN, temp55['PCR4Qnega'].rank(), np.NAN)

  
   # size maximum
    temp10sizemax = temp10.sizerank.max()
    temp15sizemax = temp15.sizerank.max()
    temp20sizemax = temp20.sizerank.max()
    temp25sizemax = temp25.sizerank.max()
    temp30sizemax = temp30.sizerank.max()
    temp35sizemax = temp35.sizerank.max()
    temp40sizemax = temp40.sizerank.max()
    temp45sizemax = temp45.sizerank.max()
    temp50sizemax = temp50.sizerank.max()
    temp55sizemax = temp55.sizerank.max()

    # PER maximum
    temp10permax = temp10.perrank.max()
    temp15permax = temp15.perrank.max()
    temp20permax = temp20.perrank.max()
    temp25permax = temp25.perrank.max()
    temp30permax = temp30.perrank.max()
    temp35permax = temp35.perrank.max()
    temp40permax = temp40.perrank.max()
    temp45permax = temp45.perrank.max()
    temp50permax = temp50.perrank.max()
    temp55permax = temp55.perrank.max()
    
    # PBR maximum
    temp10pbrmax = temp10.pbrrank.max()
    temp15pbrmax = temp15.pbrrank.max()
    temp20pbrmax = temp20.pbrrank.max()
    temp25pbrmax = temp25.pbrrank.max()
    temp30pbrmax = temp30.pbrrank.max()
    temp35pbrmax = temp35.pbrrank.max()
    temp40pbrmax = temp40.pbrrank.max()
    temp45pbrmax = temp45.pbrrank.max()
    temp50pbrmax = temp50.pbrrank.max()
    temp55pbrmax = temp55.pbrrank.max()
    
    # PCR4Q maximum
    temp10PCR4Qmax = temp10.PCR4Qrank.max()
    temp15PCR4Qmax = temp15.PCR4Qrank.max()
    temp20PCR4Qmax = temp20.PCR4Qrank.max()
    temp25PCR4Qmax = temp25.PCR4Qrank.max()
    temp30PCR4Qmax = temp30.PCR4Qrank.max()
    temp35PCR4Qmax = temp35.PCR4Qrank.max()
    temp40PCR4Qmax = temp40.PCR4Qrank.max()
    temp45PCR4Qmax = temp45.PCR4Qrank.max()
    temp50PCR4Qmax = temp50.PCR4Qrank.max()
    temp55PCR4Qmax = temp55.PCR4Qrank.max()


    # size score
    '''
    # size0 and size1
    temp10['sizescore'] = np.where(temp10['sizerank'] < temp10sizemax/2, 0, 1)
    temp15['sizescore'] = np.where(temp15['sizerank'] < temp15sizemax/2, 0, 1)
    temp20['sizescore'] = np.where(temp20['sizerank'] < temp20sizemax/2, 0, 1)
    temp25['sizescore'] = np.where(temp25['sizerank'] < temp25sizemax/2, 0, 1)
    temp30['sizescore'] = np.where(temp30['sizerank'] < temp30sizemax/2, 0, 1)
    temp35['sizescore'] = np.where(temp35['sizerank'] < temp35sizemax/2, 0, 1)
    temp40['sizescore'] = np.where(temp40['sizerank'] < temp40sizemax/2, 0, 1)
    temp45['sizescore'] = np.where(temp45['sizerank'] < temp45sizemax/2, 0, 1)
    temp50['sizescore'] = np.where(temp50['sizerank'] < temp50sizemax/2, 0, 1)
    temp55['sizescore'] = np.where(temp55['sizerank'] < temp55sizemax/2, 0, 1)
    '''    
    # size0, size1 and size2
    temp10['sizescore'] = np.where(temp10['sizerank'] < temp10sizemax/3, 0, np.where(temp10['sizerank'] < temp10sizemax/3*2, 1, 2))
    temp15['sizescore'] = np.where(temp15['sizerank'] < temp15sizemax/3, 0, np.where(temp15['sizerank'] < temp15sizemax/3*2, 1, 2))
    temp20['sizescore'] = np.where(temp20['sizerank'] < temp20sizemax/3, 0, np.where(temp20['sizerank'] < temp20sizemax/3*2, 1, 2))
    temp25['sizescore'] = np.where(temp25['sizerank'] < temp25sizemax/3, 0, np.where(temp25['sizerank'] < temp25sizemax/3*2, 1, 2))
    temp30['sizescore'] = np.where(temp30['sizerank'] < temp30sizemax/3, 0, np.where(temp30['sizerank'] < temp30sizemax/3*2, 1, 2))
    temp35['sizescore'] = np.where(temp35['sizerank'] < temp35sizemax/3, 0, np.where(temp35['sizerank'] < temp35sizemax/3*2, 1, 2))
    temp40['sizescore'] = np.where(temp40['sizerank'] < temp40sizemax/3, 0, np.where(temp40['sizerank'] < temp40sizemax/3*2, 1, 2))
    temp45['sizescore'] = np.where(temp45['sizerank'] < temp45sizemax/3, 0, np.where(temp45['sizerank'] < temp45sizemax/3*2, 1, 2))
    temp50['sizescore'] = np.where(temp50['sizerank'] < temp50sizemax/3, 0, np.where(temp50['sizerank'] < temp50sizemax/3*2, 1, 2))
    temp55['sizescore'] = np.where(temp55['sizerank'] < temp55sizemax/3, 0, np.where(temp55['sizerank'] < temp55sizemax/3*2, 1, 2))
    
    # per score
    temp10['perscore'] = np.where(temp10['perrank'] < temp10permax/3, 0, np.where(temp10['perrank'] < temp10permax/3*2, 1, 2))
    temp15['perscore'] = np.where(temp15['perrank'] < temp15permax/3, 0, np.where(temp15['perrank'] < temp15permax/3*2, 1, 2))
    temp20['perscore'] = np.where(temp20['perrank'] < temp20permax/3, 0, np.where(temp20['perrank'] < temp20permax/3*2, 1, 2))
    temp25['perscore'] = np.where(temp25['perrank'] < temp25permax/3, 0, np.where(temp25['perrank'] < temp25permax/3*2, 1, 2))
    temp30['perscore'] = np.where(temp30['perrank'] < temp30permax/3, 0, np.where(temp30['perrank'] < temp30permax/3*2, 1, 2))
    temp35['perscore'] = np.where(temp35['perrank'] < temp35permax/3, 0, np.where(temp35['perrank'] < temp35permax/3*2, 1, 2))
    temp40['perscore'] = np.where(temp40['perrank'] < temp40permax/3, 0, np.where(temp40['perrank'] < temp40permax/3*2, 1, 2))
    temp45['perscore'] = np.where(temp45['perrank'] < temp45permax/3, 0, np.where(temp45['perrank'] < temp45permax/3*2, 1, 2))
    temp50['perscore'] = np.where(temp50['perrank'] < temp50permax/3, 0, np.where(temp50['perrank'] < temp50permax/3*2, 1, 2))
    temp55['perscore'] = np.where(temp55['perrank'] < temp55permax/3, 0, np.where(temp55['perrank'] < temp55permax/3*2, 1, 2))
    
    # pbr score
    temp10['pbrscore'] = np.where(temp10['pbrrank'] < temp10pbrmax/3, 0, np.where(temp10['pbrrank'] < temp10pbrmax/3*2, 1, 2))
    temp15['pbrscore'] = np.where(temp15['pbrrank'] < temp15pbrmax/3, 0, np.where(temp15['pbrrank'] < temp15pbrmax/3*2, 1, 2))
    temp20['pbrscore'] = np.where(temp20['pbrrank'] < temp20pbrmax/3, 0, np.where(temp20['pbrrank'] < temp20pbrmax/3*2, 1, 2))
    temp25['pbrscore'] = np.where(temp25['pbrrank'] < temp25pbrmax/3, 0, np.where(temp25['pbrrank'] < temp25pbrmax/3*2, 1, 2))
    temp30['pbrscore'] = np.where(temp30['pbrrank'] < temp30pbrmax/3, 0, np.where(temp30['pbrrank'] < temp30pbrmax/3*2, 1, 2))
    temp35['pbrscore'] = np.where(temp35['pbrrank'] < temp35pbrmax/3, 0, np.where(temp35['pbrrank'] < temp35pbrmax/3*2, 1, 2))
    temp40['pbrscore'] = np.where(temp40['pbrrank'] < temp40pbrmax/3, 0, np.where(temp40['pbrrank'] < temp40pbrmax/3*2, 1, 2))
    temp45['pbrscore'] = np.where(temp45['pbrrank'] < temp45pbrmax/3, 0, np.where(temp45['pbrrank'] < temp45pbrmax/3*2, 1, 2))
    temp50['pbrscore'] = np.where(temp50['pbrrank'] < temp50pbrmax/3, 0, np.where(temp50['pbrrank'] < temp50pbrmax/3*2, 1, 2))
    temp55['pbrscore'] = np.where(temp55['pbrrank'] < temp55pbrmax/3, 0, np.where(temp55['pbrrank'] < temp55pbrmax/3*2, 1, 2))
    
    # PCR4Q score
    temp10['PCR4Qscore'] = np.where(temp10['PCR4Qrank'] < temp10PCR4Qmax/3, 0, np.where(temp10['PCR4Qrank'] < temp10PCR4Qmax/3*2, 1, 2))
    temp15['PCR4Qscore'] = np.where(temp15['PCR4Qrank'] < temp15PCR4Qmax/3, 0, np.where(temp15['PCR4Qrank'] < temp15PCR4Qmax/3*2, 1, 2))
    temp20['PCR4Qscore'] = np.where(temp20['PCR4Qrank'] < temp20PCR4Qmax/3, 0, np.where(temp20['PCR4Qrank'] < temp20PCR4Qmax/3*2, 1, 2))
    temp25['PCR4Qscore'] = np.where(temp25['PCR4Qrank'] < temp25PCR4Qmax/3, 0, np.where(temp25['PCR4Qrank'] < temp25PCR4Qmax/3*2, 1, 2))
    temp30['PCR4Qscore'] = np.where(temp30['PCR4Qrank'] < temp30PCR4Qmax/3, 0, np.where(temp30['PCR4Qrank'] < temp30PCR4Qmax/3*2, 1, 2))
    temp35['PCR4Qscore'] = np.where(temp35['PCR4Qrank'] < temp35PCR4Qmax/3, 0, np.where(temp35['PCR4Qrank'] < temp35PCR4Qmax/3*2, 1, 2))
    temp40['PCR4Qscore'] = np.where(temp40['PCR4Qrank'] < temp40PCR4Qmax/3, 0, np.where(temp40['PCR4Qrank'] < temp40PCR4Qmax/3*2, 1, 2))
    temp45['PCR4Qscore'] = np.where(temp45['PCR4Qrank'] < temp45PCR4Qmax/3, 0, np.where(temp45['PCR4Qrank'] < temp45PCR4Qmax/3*2, 1, 2))
    temp50['PCR4Qscore'] = np.where(temp50['PCR4Qrank'] < temp50PCR4Qmax/3, 0, np.where(temp50['PCR4Qrank'] < temp50PCR4Qmax/3*2, 1, 2))
    temp55['PCR4Qscore'] = np.where(temp55['PCR4Qrank'] < temp55PCR4Qmax/3, 0, np.where(temp55['PCR4Qrank'] < temp55PCR4Qmax/3*2, 1, 2))
    
    # Drawdown score
#    temp10['drawdownscore'] = np.where(temp10['drawdownrank'] < temp10drawdownmax/3, 0, np.where(temp10['drawdownrank'] < temp10Drawdownmax/3*2, 1, 2))
#    temp15['drawdownscore'] = np.where(temp15['drawdownrank'] < temp15drawdownmax/3, 0, np.where(temp15['drawdownrank'] < temp15Drawdownmax/3*2, 1, 2))
#    temp20['drawdownscore'] = np.where(temp20['drawdownrank'] < temp20drawdownmax/3, 0, np.where(temp20['drawdownrank'] < temp20Drawdownmax/3*2, 1, 2))
#    temp25['drawdownscore'] = np.where(temp25['drawdownrank'] < temp25drawdownmax/3, 0, np.where(temp25['drawdownrank'] < temp25Drawdownmax/3*2, 1, 2))
#    temp30['drawdownscore'] = np.where(temp30['drawdownrank'] < temp30drawdownmax/3, 0, np.where(temp30['drawdownrank'] < temp30Drawdownmax/3*2, 1, 2))
#    temp35['drawdownscore'] = np.where(temp35['drawdownrank'] < temp35drawdownmax/3, 0, np.where(temp35['drawdownrank'] < temp35Drawdownmax/3*2, 1, 2))
#    temp40['drawdownscore'] = np.where(temp40['drawdownrank'] < temp40drawdownmax/3, 0, np.where(temp40['drawdownrank'] < temp40Drawdownmax/3*2, 1, 2))
#    temp45['drawdownscore'] = np.where(temp45['drawdownrank'] < temp45drawdownmax/3, 0, np.where(temp45['drawdownrank'] < temp45Drawdownmax/3*2, 1, 2))
#    temp50['drawdownscore'] = np.where(temp50['drawdownrank'] < temp50drawdownmax/3, 0, np.where(temp50['drawdownrank'] < temp50Drawdownmax/3*2, 1, 2))
#    temp55['drawdownscore'] = np.where(temp55['drawdownrank'] < temp55drawdownmax/3, 0, np.where(temp55['drawdownrank'] < temp55Drawdownmax/3*2, 1, 2))
    '''
    # sum score == Size+PER+PBR
    temp10['sumscore'] = temp10['perscore']+temp10['pbrscore']+temp10['sizescore']
    temp15['sumscore'] = temp15['perscore']+temp15['pbrscore']+temp15['sizescore']
    temp20['sumscore'] = temp20['perscore']+temp20['pbrscore']+temp20['sizescore']
    temp25['sumscore'] = temp25['perscore']+temp25['pbrscore']+temp25['sizescore']
    temp30['sumscore'] = temp30['perscore']+temp30['pbrscore']+temp30['sizescore']
    temp35['sumscore'] = temp35['perscore']+temp35['pbrscore']+temp35['sizescore']
    temp40['sumscore'] = temp40['perscore']+temp40['pbrscore']+temp40['sizescore']
    temp45['sumscore'] = temp45['perscore']+temp45['pbrscore']+temp45['sizescore']
    temp50['sumscore'] = temp50['perscore']+temp50['pbrscore']+temp50['sizescore']
    temp55['sumscore'] = temp55['perscore']+temp55['pbrscore']+temp55['sizescore']
    '''
    # sum score = Size
    temp10['sumscore'] = temp10['sizescore']
    temp15['sumscore'] = temp15['sizescore']
    temp20['sumscore'] = temp20['sizescore']
    temp25['sumscore'] = temp25['sizescore']
    temp30['sumscore'] = temp30['sizescore']
    temp35['sumscore'] = temp35['sizescore']
    temp40['sumscore'] = temp40['sizescore']
    temp45['sumscore'] = temp45['sizescore']
    temp50['sumscore'] = temp50['sizescore']
    temp55['sumscore'] = temp55['sizescore']
    
#=====================================================================================
# 원하는 데이터 별로 구분하는 구간
#=====================================================================================


#by Drawdown    
#    dd0se10 = temp10[temp10.sumscore==0][temp10.drawdownscore==0].dropna()
#    dd0se15 = temp15[temp15.sumscore==0][temp15.drawdownscore==0].dropna()
#    dd0se20 = temp20[temp20.sumscore==0][temp20.drawdownscore==0].dropna()
#    dd0se25 = temp25[temp25.sumscore==0][temp25.drawdownscore==0].dropna()
#    dd0se30 = temp30[temp30.sumscore==0][temp30.drawdownscore==0].dropna()
#    dd0se35 = temp35[temp35.sumscore==0][temp35.drawdownscore==0].dropna()
#    dd0se40 = temp40[temp40.sumscore==0][temp40.drawdownscore==0].dropna()
#    dd0se45 = temp45[temp45.sumscore==0][temp45.drawdownscore==0].dropna()
#    dd0se50 = temp50[temp50.sumscore==0][temp50.drawdownscore==0].dropna()
#    dd0se55 = temp55[temp55.sumscore==0][temp55.drawdownscore==0].dropna()

#    dd1se10 = temp10[temp10.sumscore==0][temp10.drawdownscore==1].dropna()
#    dd1se15 = temp15[temp15.sumscore==0][temp15.drawdownscore==1].dropna()
#    dd1se20 = temp20[temp20.sumscore==0][temp20.drawdownscore==1].dropna()
#    dd1se25 = temp25[temp25.sumscore==0][temp25.drawdownscore==1].dropna()
#    dd1se30 = temp30[temp30.sumscore==0][temp30.drawdownscore==1].dropna()
#    dd1se35 = temp35[temp35.sumscore==0][temp35.drawdownscore==1].dropna()
#    dd1se40 = temp40[temp40.sumscore==0][temp40.drawdownscore==1].dropna()
#    dd1se45 = temp45[temp45.sumscore==0][temp45.drawdownscore==1].dropna()
#    dd1se50 = temp50[temp50.sumscore==0][temp50.drawdownscore==1].dropna()
#    dd1se55 = temp55[temp55.sumscore==0][temp55.drawdownscore==1].dropna()
    
    seb10 = temp10[temp10.sumscore==0]
    seb15 = temp15[temp15.sumscore==0]
    seb20 = temp20[temp20.sumscore==0]
    seb25 = temp25[temp25.sumscore==0]
    seb30 = temp30[temp30.sumscore==0]
    seb35 = temp35[temp35.sumscore==0]
    seb40 = temp40[temp40.sumscore==0]
    seb45 = temp45[temp45.sumscore==0]
    seb50 = temp50[temp50.sumscore==0]
    seb55 = temp55[temp55.sumscore==0]
    
    # After SPP(size&PER&PBR) modeling, 
    # dependently classify by other indicators as below:
    #============================================================================  
    '''    
    # By rate of return of price
    #  before1monthRR ranking
    seb10['before1monthRrank'] = np.where(seb10['before1monthR'] != np.NAN, seb10['before1monthR'].rank(), np.NAN)
    seb15['before1monthRrank'] = np.where(seb15['before1monthR'] != np.NAN, seb15['before1monthR'].rank(), np.NAN)
    seb20['before1monthRrank'] = np.where(seb20['before1monthR'] != np.NAN, seb20['before1monthR'].rank(), np.NAN)
    seb25['before1monthRrank'] = np.where(seb25['before1monthR'] != np.NAN, seb25['before1monthR'].rank(), np.NAN)
    seb30['before1monthRrank'] = np.where(seb30['before1monthR'] != np.NAN, seb30['before1monthR'].rank(), np.NAN)
    seb35['before1monthRrank'] = np.where(seb35['before1monthR'] != np.NAN, seb35['before1monthR'].rank(), np.NAN)
    seb40['before1monthRrank'] = np.where(seb40['before1monthR'] != np.NAN, seb40['before1monthR'].rank(), np.NAN)
    seb45['before1monthRrank'] = np.where(seb45['before1monthR'] != np.NAN, seb45['before1monthR'].rank(), np.NAN)
    seb50['before1monthRrank'] = np.where(seb50['before1monthR'] != np.NAN, seb50['before1monthR'].rank(), np.NAN)
    seb55['before1monthRrank'] = np.where(seb55['before1monthR'] != np.NAN, seb55['before1monthR'].rank(), np.NAN)
    # before1monthR maximum
    seb10before1monthRmax = seb10.before1monthRrank.max()
    seb15before1monthRmax = seb15.before1monthRrank.max()
    seb20before1monthRmax = seb20.before1monthRrank.max()
    seb25before1monthRmax = seb25.before1monthRrank.max()
    seb30before1monthRmax = seb30.before1monthRrank.max()
    seb35before1monthRmax = seb35.before1monthRrank.max()
    seb40before1monthRmax = seb40.before1monthRrank.max()
    seb45before1monthRmax = seb45.before1monthRrank.max()
    seb50before1monthRmax = seb50.before1monthRrank.max()
    seb55before1monthRmax = seb55.before1monthRrank.max()    
    #before1monthR score
    seb10['before1monthRscore'] = np.where(seb10['before1monthRrank'] < seb10before1monthRmax/3, 0, np.where(seb10['before1monthRrank'] < seb10before1monthRmax/3*2, 1, 2))
    seb15['before1monthRscore'] = np.where(seb15['before1monthRrank'] < seb15before1monthRmax/3, 0, np.where(seb15['before1monthRrank'] < seb15before1monthRmax/3*2, 1, 2))
    seb20['before1monthRscore'] = np.where(seb20['before1monthRrank'] < seb20before1monthRmax/3, 0, np.where(seb20['before1monthRrank'] < seb20before1monthRmax/3*2, 1, 2))
    seb25['before1monthRscore'] = np.where(seb25['before1monthRrank'] < seb25before1monthRmax/3, 0, np.where(seb25['before1monthRrank'] < seb25before1monthRmax/3*2, 1, 2))
    seb30['before1monthRscore'] = np.where(seb30['before1monthRrank'] < seb30before1monthRmax/3, 0, np.where(seb30['before1monthRrank'] < seb30before1monthRmax/3*2, 1, 2))
    seb35['before1monthRscore'] = np.where(seb35['before1monthRrank'] < seb35before1monthRmax/3, 0, np.where(seb35['before1monthRrank'] < seb35before1monthRmax/3*2, 1, 2))
    seb40['before1monthRscore'] = np.where(seb40['before1monthRrank'] < seb40before1monthRmax/3, 0, np.where(seb40['before1monthRrank'] < seb40before1monthRmax/3*2, 1, 2))
    seb45['before1monthRscore'] = np.where(seb45['before1monthRrank'] < seb45before1monthRmax/3, 0, np.where(seb45['before1monthRrank'] < seb45before1monthRmax/3*2, 1, 2))
    seb50['before1monthRscore'] = np.where(seb50['before1monthRrank'] < seb50before1monthRmax/3, 0, np.where(seb50['before1monthRrank'] < seb50before1monthRmax/3*2, 1, 2))
    seb55['before1monthRscore'] = np.where(seb55['before1monthRrank'] < seb55before1monthRmax/3, 0, np.where(seb55['before1monthRrank'] < seb55before1monthRmax/3*2, 1, 2))
    #============================================================================  
    #  after1monthRR ranking
    seb10['after1monthRrank'] = np.where(seb10['after1monthR'] != np.NAN, seb10['after1monthR'].rank(), np.NAN)
    seb15['after1monthRrank'] = np.where(seb15['after1monthR'] != np.NAN, seb15['after1monthR'].rank(), np.NAN)
    seb20['after1monthRrank'] = np.where(seb20['after1monthR'] != np.NAN, seb20['after1monthR'].rank(), np.NAN)
    seb25['after1monthRrank'] = np.where(seb25['after1monthR'] != np.NAN, seb25['after1monthR'].rank(), np.NAN)
    seb30['after1monthRrank'] = np.where(seb30['after1monthR'] != np.NAN, seb30['after1monthR'].rank(), np.NAN)
    seb35['after1monthRrank'] = np.where(seb35['after1monthR'] != np.NAN, seb35['after1monthR'].rank(), np.NAN)
    seb40['after1monthRrank'] = np.where(seb40['after1monthR'] != np.NAN, seb40['after1monthR'].rank(), np.NAN)
    seb45['after1monthRrank'] = np.where(seb45['after1monthR'] != np.NAN, seb45['after1monthR'].rank(), np.NAN)
    seb50['after1monthRrank'] = np.where(seb50['after1monthR'] != np.NAN, seb50['after1monthR'].rank(), np.NAN)
    seb55['after1monthRrank'] = np.where(seb55['after1monthR'] != np.NAN, seb55['after1monthR'].rank(), np.NAN)
    # after1monthR maximum
    seb10after1monthRmax = seb10.after1monthRrank.max()
    seb15after1monthRmax = seb15.after1monthRrank.max()
    seb20after1monthRmax = seb20.after1monthRrank.max()
    seb25after1monthRmax = seb25.after1monthRrank.max()
    seb30after1monthRmax = seb30.after1monthRrank.max()
    seb35after1monthRmax = seb35.after1monthRrank.max()
    seb40after1monthRmax = seb40.after1monthRrank.max()
    seb45after1monthRmax = seb45.after1monthRrank.max()
    seb50after1monthRmax = seb50.after1monthRrank.max()
    seb55after1monthRmax = seb55.after1monthRrank.max()    
    #after1monthR score
    seb10['after1monthRscore'] = np.where(seb10['after1monthRrank'] < seb10after1monthRmax/3, 0, np.where(seb10['after1monthRrank'] < seb10after1monthRmax/3*2, 1, 2))
    seb15['after1monthRscore'] = np.where(seb15['after1monthRrank'] < seb15after1monthRmax/3, 0, np.where(seb15['after1monthRrank'] < seb15after1monthRmax/3*2, 1, 2))
    seb20['after1monthRscore'] = np.where(seb20['after1monthRrank'] < seb20after1monthRmax/3, 0, np.where(seb20['after1monthRrank'] < seb20after1monthRmax/3*2, 1, 2))
    seb25['after1monthRscore'] = np.where(seb25['after1monthRrank'] < seb25after1monthRmax/3, 0, np.where(seb25['after1monthRrank'] < seb25after1monthRmax/3*2, 1, 2))
    seb30['after1monthRscore'] = np.where(seb30['after1monthRrank'] < seb30after1monthRmax/3, 0, np.where(seb30['after1monthRrank'] < seb30after1monthRmax/3*2, 1, 2))
    seb35['after1monthRscore'] = np.where(seb35['after1monthRrank'] < seb35after1monthRmax/3, 0, np.where(seb35['after1monthRrank'] < seb35after1monthRmax/3*2, 1, 2))
    seb40['after1monthRscore'] = np.where(seb40['after1monthRrank'] < seb40after1monthRmax/3, 0, np.where(seb40['after1monthRrank'] < seb40after1monthRmax/3*2, 1, 2))
    seb45['after1monthRscore'] = np.where(seb45['after1monthRrank'] < seb45after1monthRmax/3, 0, np.where(seb45['after1monthRrank'] < seb45after1monthRmax/3*2, 1, 2))
    seb50['after1monthRscore'] = np.where(seb50['after1monthRrank'] < seb50after1monthRmax/3, 0, np.where(seb50['after1monthRrank'] < seb50after1monthRmax/3*2, 1, 2))
    seb55['after1monthRscore'] = np.where(seb55['after1monthRrank'] < seb55after1monthRmax/3, 0, np.where(seb55['after1monthRrank'] < seb55after1monthRmax/3*2, 1, 2))
    #============================================================================  
    
    # by ROE_OP
    # ROE_OP ranking
    seb10['ROE_OPrank'] = np.where(seb10['ROE_OP'] != np.NAN, seb10['ROE_OP'].rank(), np.NAN)
    seb15['ROE_OPrank'] = np.where(seb15['ROE_OP'] != np.NAN, seb15['ROE_OP'].rank(), np.NAN)
    seb20['ROE_OPrank'] = np.where(seb20['ROE_OP'] != np.NAN, seb20['ROE_OP'].rank(), np.NAN)
    seb25['ROE_OPrank'] = np.where(seb25['ROE_OP'] != np.NAN, seb25['ROE_OP'].rank(), np.NAN)
    seb30['ROE_OPrank'] = np.where(seb30['ROE_OP'] != np.NAN, seb30['ROE_OP'].rank(), np.NAN)
    seb35['ROE_OPrank'] = np.where(seb35['ROE_OP'] != np.NAN, seb35['ROE_OP'].rank(), np.NAN)
    seb40['ROE_OPrank'] = np.where(seb40['ROE_OP'] != np.NAN, seb40['ROE_OP'].rank(), np.NAN)
    seb45['ROE_OPrank'] = np.where(seb45['ROE_OP'] != np.NAN, seb45['ROE_OP'].rank(), np.NAN)
    seb50['ROE_OPrank'] = np.where(seb50['ROE_OP'] != np.NAN, seb50['ROE_OP'].rank(), np.NAN)
    seb55['ROE_OPrank'] = np.where(seb55['ROE_OP'] != np.NAN, seb55['ROE_OP'].rank(), np.NAN)
    # ROE_OP maximum
    seb10ROE_OPmax = seb10.ROE_OPrank.max()
    seb15ROE_OPmax = seb15.ROE_OPrank.max()
    seb20ROE_OPmax = seb20.ROE_OPrank.max()
    seb25ROE_OPmax = seb25.ROE_OPrank.max()
    seb30ROE_OPmax = seb30.ROE_OPrank.max()
    seb35ROE_OPmax = seb35.ROE_OPrank.max()
    seb40ROE_OPmax = seb40.ROE_OPrank.max()
    seb45ROE_OPmax = seb45.ROE_OPrank.max()
    seb50ROE_OPmax = seb50.ROE_OPrank.max()
    seb55ROE_OPmax = seb55.ROE_OPrank.max()    
    #ROE_OP score
    seb10['ROE_OPscore'] = np.where(seb10['ROE_OPrank'] < seb10ROE_OPmax/3, 0, np.where(seb10['ROE_OPrank'] < seb10ROE_OPmax/3*2, 1, 2))
    seb15['ROE_OPscore'] = np.where(seb15['ROE_OPrank'] < seb15ROE_OPmax/3, 0, np.where(seb15['ROE_OPrank'] < seb15ROE_OPmax/3*2, 1, 2))
    seb20['ROE_OPscore'] = np.where(seb20['ROE_OPrank'] < seb20ROE_OPmax/3, 0, np.where(seb20['ROE_OPrank'] < seb20ROE_OPmax/3*2, 1, 2))
    seb25['ROE_OPscore'] = np.where(seb25['ROE_OPrank'] < seb25ROE_OPmax/3, 0, np.where(seb25['ROE_OPrank'] < seb25ROE_OPmax/3*2, 1, 2))
    seb30['ROE_OPscore'] = np.where(seb30['ROE_OPrank'] < seb30ROE_OPmax/3, 0, np.where(seb30['ROE_OPrank'] < seb30ROE_OPmax/3*2, 1, 2))
    seb35['ROE_OPscore'] = np.where(seb35['ROE_OPrank'] < seb35ROE_OPmax/3, 0, np.where(seb35['ROE_OPrank'] < seb35ROE_OPmax/3*2, 1, 2))
    seb40['ROE_OPscore'] = np.where(seb40['ROE_OPrank'] < seb40ROE_OPmax/3, 0, np.where(seb40['ROE_OPrank'] < seb40ROE_OPmax/3*2, 1, 2))
    seb45['ROE_OPscore'] = np.where(seb45['ROE_OPrank'] < seb45ROE_OPmax/3, 0, np.where(seb45['ROE_OPrank'] < seb45ROE_OPmax/3*2, 1, 2))
    seb50['ROE_OPscore'] = np.where(seb50['ROE_OPrank'] < seb50ROE_OPmax/3, 0, np.where(seb50['ROE_OPrank'] < seb50ROE_OPmax/3*2, 1, 2))
    seb55['ROE_OPscore'] = np.where(seb55['ROE_OPrank'] < seb55ROE_OPmax/3, 0, np.where(seb55['ROE_OPrank'] < seb55ROE_OPmax/3*2, 1, 2))
    
    #============================================================================  
    # by drawdown
    # drawdown ranking
    seb10['drawdownrank'] = np.where(seb10['drawdown'] != np.NAN, seb10['drawdown'].rank(), np.NAN)
    seb15['drawdownrank'] = np.where(seb15['drawdown'] != np.NAN, seb15['drawdown'].rank(), np.NAN)
    seb20['drawdownrank'] = np.where(seb20['drawdown'] != np.NAN, seb20['drawdown'].rank(), np.NAN)
    seb25['drawdownrank'] = np.where(seb25['drawdown'] != np.NAN, seb25['drawdown'].rank(), np.NAN)
    seb30['drawdownrank'] = np.where(seb30['drawdown'] != np.NAN, seb30['drawdown'].rank(), np.NAN)
    seb35['drawdownrank'] = np.where(seb35['drawdown'] != np.NAN, seb35['drawdown'].rank(), np.NAN)
    seb40['drawdownrank'] = np.where(seb40['drawdown'] != np.NAN, seb40['drawdown'].rank(), np.NAN)
    seb45['drawdownrank'] = np.where(seb45['drawdown'] != np.NAN, seb45['drawdown'].rank(), np.NAN)
    seb50['drawdownrank'] = np.where(seb50['drawdown'] != np.NAN, seb50['drawdown'].rank(), np.NAN)
    seb55['drawdownrank'] = np.where(seb55['drawdown'] != np.NAN, seb55['drawdown'].rank(), np.NAN)
    # drawdown maximum
    seb10drawdownmax = seb10.drawdownrank.max()
    seb15drawdownmax = seb15.drawdownrank.max()
    seb20drawdownmax = seb20.drawdownrank.max()
    seb25drawdownmax = seb25.drawdownrank.max()
    seb30drawdownmax = seb30.drawdownrank.max()
    seb35drawdownmax = seb35.drawdownrank.max()
    seb40drawdownmax = seb40.drawdownrank.max()
    seb45drawdownmax = seb45.drawdownrank.max()
    seb50drawdownmax = seb50.drawdownrank.max()
    seb55drawdownmax = seb55.drawdownrank.max()    
    #drawdown score
    seb10['drawdownscore'] = np.where(seb10['drawdownrank'] < seb10drawdownmax/3, 0, np.where(seb10['drawdownrank'] < seb10drawdownmax/3*2, 1, 2))
    seb15['drawdownscore'] = np.where(seb15['drawdownrank'] < seb15drawdownmax/3, 0, np.where(seb15['drawdownrank'] < seb15drawdownmax/3*2, 1, 2))
    seb20['drawdownscore'] = np.where(seb20['drawdownrank'] < seb20drawdownmax/3, 0, np.where(seb20['drawdownrank'] < seb20drawdownmax/3*2, 1, 2))
    seb25['drawdownscore'] = np.where(seb25['drawdownrank'] < seb25drawdownmax/3, 0, np.where(seb25['drawdownrank'] < seb25drawdownmax/3*2, 1, 2))
    seb30['drawdownscore'] = np.where(seb30['drawdownrank'] < seb30drawdownmax/3, 0, np.where(seb30['drawdownrank'] < seb30drawdownmax/3*2, 1, 2))
    seb35['drawdownscore'] = np.where(seb35['drawdownrank'] < seb35drawdownmax/3, 0, np.where(seb35['drawdownrank'] < seb35drawdownmax/3*2, 1, 2))
    seb40['drawdownscore'] = np.where(seb40['drawdownrank'] < seb40drawdownmax/3, 0, np.where(seb40['drawdownrank'] < seb40drawdownmax/3*2, 1, 2))
    seb45['drawdownscore'] = np.where(seb45['drawdownrank'] < seb45drawdownmax/3, 0, np.where(seb45['drawdownrank'] < seb45drawdownmax/3*2, 1, 2))
    seb50['drawdownscore'] = np.where(seb50['drawdownrank'] < seb50drawdownmax/3, 0, np.where(seb50['drawdownrank'] < seb50drawdownmax/3*2, 1, 2))
    seb55['drawdownscore'] = np.where(seb55['drawdownrank'] < seb55drawdownmax/3, 0, np.where(seb55['drawdownrank'] < seb55drawdownmax/3*2, 1, 2))    
    
    #=======================================================================================    
    # by ROA_OP
    # ROA_OP ranking
    seb10['ROA_OPrank'] = np.where(seb10['ROA_OP'] != np.NAN, seb10['ROA_OP'].rank(), np.NAN)
    seb15['ROA_OPrank'] = np.where(seb15['ROA_OP'] != np.NAN, seb15['ROA_OP'].rank(), np.NAN)
    seb20['ROA_OPrank'] = np.where(seb20['ROA_OP'] != np.NAN, seb20['ROA_OP'].rank(), np.NAN)
    seb25['ROA_OPrank'] = np.where(seb25['ROA_OP'] != np.NAN, seb25['ROA_OP'].rank(), np.NAN)
    seb30['ROA_OPrank'] = np.where(seb30['ROA_OP'] != np.NAN, seb30['ROA_OP'].rank(), np.NAN)
    seb35['ROA_OPrank'] = np.where(seb35['ROA_OP'] != np.NAN, seb35['ROA_OP'].rank(), np.NAN)
    seb40['ROA_OPrank'] = np.where(seb40['ROA_OP'] != np.NAN, seb40['ROA_OP'].rank(), np.NAN)
    seb45['ROA_OPrank'] = np.where(seb45['ROA_OP'] != np.NAN, seb45['ROA_OP'].rank(), np.NAN)
    seb50['ROA_OPrank'] = np.where(seb50['ROA_OP'] != np.NAN, seb50['ROA_OP'].rank(), np.NAN)
    seb55['ROA_OPrank'] = np.where(seb55['ROA_OP'] != np.NAN, seb55['ROA_OP'].rank(), np.NAN)
    # ROA_OP maximum
    seb10ROA_OPmax = seb10.ROA_OPrank.max()
    seb15ROA_OPmax = seb15.ROA_OPrank.max()
    seb20ROA_OPmax = seb20.ROA_OPrank.max()
    seb25ROA_OPmax = seb25.ROA_OPrank.max()
    seb30ROA_OPmax = seb30.ROA_OPrank.max()
    seb35ROA_OPmax = seb35.ROA_OPrank.max()
    seb40ROA_OPmax = seb40.ROA_OPrank.max()
    seb45ROA_OPmax = seb45.ROA_OPrank.max()
    seb50ROA_OPmax = seb50.ROA_OPrank.max()
    seb55ROA_OPmax = seb55.ROA_OPrank.max()    
    #ROA_OP score
    seb10['ROA_OPscore'] = np.where(seb10['ROA_OPrank'] < seb10ROA_OPmax/3, 0, np.where(seb10['ROA_OPrank'] < seb10ROA_OPmax/3*2, 1, 2))
    seb15['ROA_OPscore'] = np.where(seb15['ROA_OPrank'] < seb15ROA_OPmax/3, 0, np.where(seb15['ROA_OPrank'] < seb15ROA_OPmax/3*2, 1, 2))
    seb20['ROA_OPscore'] = np.where(seb20['ROA_OPrank'] < seb20ROA_OPmax/3, 0, np.where(seb20['ROA_OPrank'] < seb20ROA_OPmax/3*2, 1, 2))
    seb25['ROA_OPscore'] = np.where(seb25['ROA_OPrank'] < seb25ROA_OPmax/3, 0, np.where(seb25['ROA_OPrank'] < seb25ROA_OPmax/3*2, 1, 2))
    seb30['ROA_OPscore'] = np.where(seb30['ROA_OPrank'] < seb30ROA_OPmax/3, 0, np.where(seb30['ROA_OPrank'] < seb30ROA_OPmax/3*2, 1, 2))
    seb35['ROA_OPscore'] = np.where(seb35['ROA_OPrank'] < seb35ROA_OPmax/3, 0, np.where(seb35['ROA_OPrank'] < seb35ROA_OPmax/3*2, 1, 2))
    seb40['ROA_OPscore'] = np.where(seb40['ROA_OPrank'] < seb40ROA_OPmax/3, 0, np.where(seb40['ROA_OPrank'] < seb40ROA_OPmax/3*2, 1, 2))
    seb45['ROA_OPscore'] = np.where(seb45['ROA_OPrank'] < seb45ROA_OPmax/3, 0, np.where(seb45['ROA_OPrank'] < seb45ROA_OPmax/3*2, 1, 2))
    seb50['ROA_OPscore'] = np.where(seb50['ROA_OPrank'] < seb50ROA_OPmax/3, 0, np.where(seb50['ROA_OPrank'] < seb50ROA_OPmax/3*2, 1, 2))
    seb55['ROA_OPscore'] = np.where(seb55['ROA_OPrank'] < seb55ROA_OPmax/3, 0, np.where(seb55['ROA_OPrank'] < seb55ROA_OPmax/3*2, 1, 2))
    
    #=======================================================================================    
    
    # by RoS_OP
    # RoS_OP ranking
    seb10['RoS_OPrank'] = np.where(seb10['RoS_OP'] != np.NAN, seb10['RoS_OP'].rank(), np.NAN)
    seb15['RoS_OPrank'] = np.where(seb15['RoS_OP'] != np.NAN, seb15['RoS_OP'].rank(), np.NAN)
    seb20['RoS_OPrank'] = np.where(seb20['RoS_OP'] != np.NAN, seb20['RoS_OP'].rank(), np.NAN)
    seb25['RoS_OPrank'] = np.where(seb25['RoS_OP'] != np.NAN, seb25['RoS_OP'].rank(), np.NAN)
    seb30['RoS_OPrank'] = np.where(seb30['RoS_OP'] != np.NAN, seb30['RoS_OP'].rank(), np.NAN)
    seb35['RoS_OPrank'] = np.where(seb35['RoS_OP'] != np.NAN, seb35['RoS_OP'].rank(), np.NAN)
    seb40['RoS_OPrank'] = np.where(seb40['RoS_OP'] != np.NAN, seb40['RoS_OP'].rank(), np.NAN)
    seb45['RoS_OPrank'] = np.where(seb45['RoS_OP'] != np.NAN, seb45['RoS_OP'].rank(), np.NAN)
    seb50['RoS_OPrank'] = np.where(seb50['RoS_OP'] != np.NAN, seb50['RoS_OP'].rank(), np.NAN)
    seb55['RoS_OPrank'] = np.where(seb55['RoS_OP'] != np.NAN, seb55['RoS_OP'].rank(), np.NAN)
    # RoS_OP maximum
    seb10RoS_OPmax = seb10.RoS_OPrank.max()
    seb15RoS_OPmax = seb15.RoS_OPrank.max()
    seb20RoS_OPmax = seb20.RoS_OPrank.max()
    seb25RoS_OPmax = seb25.RoS_OPrank.max()
    seb30RoS_OPmax = seb30.RoS_OPrank.max()
    seb35RoS_OPmax = seb35.RoS_OPrank.max()
    seb40RoS_OPmax = seb40.RoS_OPrank.max()
    seb45RoS_OPmax = seb45.RoS_OPrank.max()
    seb50RoS_OPmax = seb50.RoS_OPrank.max()
    seb55RoS_OPmax = seb55.RoS_OPrank.max()    
    #RoS_OP score
    seb10['RoS_OPscore'] = np.where(seb10['RoS_OPrank'] < seb10RoS_OPmax/3, 0, np.where(seb10['RoS_OPrank'] < seb10RoS_OPmax/3*2, 1, 2))
    seb15['RoS_OPscore'] = np.where(seb15['RoS_OPrank'] < seb15RoS_OPmax/3, 0, np.where(seb15['RoS_OPrank'] < seb15RoS_OPmax/3*2, 1, 2))
    seb20['RoS_OPscore'] = np.where(seb20['RoS_OPrank'] < seb20RoS_OPmax/3, 0, np.where(seb20['RoS_OPrank'] < seb20RoS_OPmax/3*2, 1, 2))
    seb25['RoS_OPscore'] = np.where(seb25['RoS_OPrank'] < seb25RoS_OPmax/3, 0, np.where(seb25['RoS_OPrank'] < seb25RoS_OPmax/3*2, 1, 2))
    seb30['RoS_OPscore'] = np.where(seb30['RoS_OPrank'] < seb30RoS_OPmax/3, 0, np.where(seb30['RoS_OPrank'] < seb30RoS_OPmax/3*2, 1, 2))
    seb35['RoS_OPscore'] = np.where(seb35['RoS_OPrank'] < seb35RoS_OPmax/3, 0, np.where(seb35['RoS_OPrank'] < seb35RoS_OPmax/3*2, 1, 2))
    seb40['RoS_OPscore'] = np.where(seb40['RoS_OPrank'] < seb40RoS_OPmax/3, 0, np.where(seb40['RoS_OPrank'] < seb40RoS_OPmax/3*2, 1, 2))
    seb45['RoS_OPscore'] = np.where(seb45['RoS_OPrank'] < seb45RoS_OPmax/3, 0, np.where(seb45['RoS_OPrank'] < seb45RoS_OPmax/3*2, 1, 2))
    seb50['RoS_OPscore'] = np.where(seb50['RoS_OPrank'] < seb50RoS_OPmax/3, 0, np.where(seb50['RoS_OPrank'] < seb50RoS_OPmax/3*2, 1, 2))
    seb55['RoS_OPscore'] = np.where(seb55['RoS_OPrank'] < seb55RoS_OPmax/3, 0, np.where(seb55['RoS_OPrank'] < seb55RoS_OPmax/3*2, 1, 2))
        
    #=======================================================================================    
    '''
    # total stocks of each sector
    seb10total = seb10total.append(seb10)
    seb15total = seb15total.append(seb15)
    seb20total = seb20total.append(seb20)
    seb25total = seb25total.append(seb25)
    seb30total = seb30total.append(seb30)
    seb35total = seb35total.append(seb35)
    seb40total = seb40total.append(seb40)
    seb45total = seb45total.append(seb45)
    seb50total = seb50total.append(seb50)
    seb55total = seb55total.append(seb55)
    '''
    #============================================================================
    # Select target indicator that you want to use
    #============================================================================          
    
     
    targetddscore=2
    targetbefore1monthRscore=0
    
    # before1monthRscore==0
    seb10 = seb10[seb10.before1monthRscore==targetbefore1monthRscore]
    seb15 = seb15[seb15.before1monthRscore==targetbefore1monthRscore]
    seb20 = seb20[seb20.before1monthRscore==targetbefore1monthRscore]
    seb25 = seb25[seb25.before1monthRscore==targetbefore1monthRscore]
    seb30 = seb30[seb30.before1monthRscore==targetbefore1monthRscore]
    seb35 = seb35[seb35.before1monthRscore==targetbefore1monthRscore]
    seb40 = seb40[seb40.before1monthRscore==targetbefore1monthRscore]
    seb45 = seb45[seb45.before1monthRscore==targetbefore1monthRscore]
    seb50 = seb50[seb50.before1monthRscore==targetbefore1monthRscore]
    seb55 = seb55[seb55.before1monthRscore==targetbefore1monthRscore]
    
    #============================================================================   
    # ROE_OPscore==0
    seb10 = seb10[seb10.ROE_OPscore==0]
    seb15 = seb15[seb15.ROE_OPscore==0]
    seb20 = seb20[seb20.ROE_OPscore==0]
    seb25 = seb25[seb25.ROE_OPscore==0]
    seb30 = seb30[seb30.ROE_OPscore==0]
    seb35 = seb35[seb35.ROE_OPscore==0]
    seb40 = seb40[seb40.ROE_OPscore==0]
    seb45 = seb45[seb45.ROE_OPscore==0]
    seb50 = seb50[seb50.ROE_OPscore==0]
    seb55 = seb55[seb55.ROE_OPscore==0]
    
    #============================================================================   
    # ROA_OPscore==0
    seb10 = seb10[seb10.ROA_OPscore==0]
    seb15 = seb15[seb15.ROA_OPscore==0]
    seb20 = seb20[seb20.ROA_OPscore==0]
    seb25 = seb25[seb25.ROA_OPscore==0]
    seb30 = seb30[seb30.ROA_OPscore==0]
    seb35 = seb35[seb35.ROA_OPscore==0]
    seb40 = seb40[seb40.ROA_OPscore==0]
    seb45 = seb45[seb45.ROA_OPscore==0]
    seb50 = seb50[seb50.ROA_OPscore==0]
    seb55 = seb55[seb55.ROA_OPscore==0]    
    
    #============================================================================   
    # RoS_OPscore==0
    tgtRoS_OPscore=0
    tgtseb10 = seb10[seb10.RoS_OPscore==tgtRoS_OPscore]
    tgtseb15 = seb15[seb15.RoS_OPscore==tgtRoS_OPscore]
    tgtseb20 = seb20[seb20.RoS_OPscore==tgtRoS_OPscore]
    tgtseb25 = seb25[seb25.RoS_OPscore==tgtRoS_OPscore]
    tgtseb30 = seb30[seb30.RoS_OPscore==tgtRoS_OPscore]
    tgtseb35 = seb35[seb35.RoS_OPscore==tgtRoS_OPscore]
    tgtseb40 = seb40[seb40.RoS_OPscore==tgtRoS_OPscore]
    tgtseb45 = seb45[seb45.RoS_OPscore==tgtRoS_OPscore]
    tgtseb50 = seb50[seb50.RoS_OPscore==tgtRoS_OPscore]
    tgtseb55 = seb55[seb55.RoS_OPscore==tgtRoS_OPscore] 
    
    #============================================================================  
    # drawdownscore==0
    tgtseb10 = seb10[seb10.drawdownscore==targetddscore]
    tgtseb15 = seb15[seb15.drawdownscore==targetddscore]
    tgtseb20 = seb20[seb20.drawdownscore==targetddscore]
    tgtseb25 = seb25[seb25.drawdownscore==targetddscore]
    tgtseb30 = seb30[seb30.drawdownscore==targetddscore]
    tgtseb35 = seb35[seb35.drawdownscore==targetddscore]
    tgtseb40 = seb40[seb40.drawdownscore==targetddscore]
    tgtseb45 = seb45[seb45.drawdownscore==targetddscore]
    tgtseb50 = seb50[seb50.drawdownscore==targetddscore]
    tgtseb55 = seb55[seb55.drawdownscore==targetddscore]    
        
    #============================================================================  
    # before1monthRscore & drawdownscore
    tgtbefore1monthRscore=0
    tgtddscore=2
    tgtseb10 = seb10[seb10.before1monthRscore==tgtbefore1monthRscore][seb10.drawdownscore==tgtddscore]
    tgtseb15 = seb15[seb15.before1monthRscore==tgtbefore1monthRscore][seb15.drawdownscore==tgtddscore]
    tgtseb20 = seb20[seb20.before1monthRscore==tgtbefore1monthRscore][seb20.drawdownscore==tgtddscore]
    tgtseb25 = seb25[seb25.before1monthRscore==tgtbefore1monthRscore][seb25.drawdownscore==tgtddscore]
    tgtseb30 = seb30[seb30.before1monthRscore==tgtbefore1monthRscore][seb30.drawdownscore==tgtddscore]
    tgtseb35 = seb35[seb35.before1monthRscore==tgtbefore1monthRscore][seb35.drawdownscore==tgtddscore]
    tgtseb40 = seb40[seb40.before1monthRscore==tgtbefore1monthRscore][seb40.drawdownscore==tgtddscore]
    tgtseb45 = seb45[seb45.before1monthRscore==tgtbefore1monthRscore][seb45.drawdownscore==tgtddscore]
    tgtseb50 = seb50[seb50.before1monthRscore==tgtbefore1monthRscore][seb50.drawdownscore==tgtddscore]
    tgtseb55 = seb55[seb55.before1monthRscore==tgtbefore1monthRscore][seb55.drawdownscore==tgtddscore] 
    
 
    #============================================================================      
    '''
    # target==all
    
    tgtseb10 = seb10
    tgtseb15 = seb15
    tgtseb20 = seb20
    tgtseb25 = seb25
    tgtseb30 = seb30
    tgtseb35 = seb35
    tgtseb40 = seb40
    tgtseb45 = seb45
    tgtseb50 = seb50
    tgtseb55 = seb55
    '''
    # target==after1monthR    
    tgtafter1monthRscore=2    
    tgtseb10 = seb10[seb10.after1monthRscore==tgtafter1monthRscore]
    tgtseb15 = seb15[seb15.after1monthRscore==tgtafter1monthRscore]
    tgtseb20 = seb20[seb20.after1monthRscore==tgtafter1monthRscore]
    tgtseb25 = seb25[seb25.after1monthRscore==tgtafter1monthRscore]
    tgtseb30 = seb30[seb30.after1monthRscore==tgtafter1monthRscore]
    tgtseb35 = seb35[seb35.after1monthRscore==tgtafter1monthRscore]
    tgtseb40 = seb40[seb40.after1monthRscore==tgtafter1monthRscore]
    tgtseb45 = seb45[seb45.after1monthRscore==tgtafter1monthRscore]
    tgtseb50 = seb50[seb50.after1monthRscore==tgtafter1monthRscore]
    tgtseb55 = seb55[seb55.after1monthRscore==tgtafter1monthRscore]   
    
    # target==before1monthR    
    tgtbefore1monthRscore=0

    tgtseb10 = seb10[seb10.before1monthRscore==tgtbefore1monthRscore]
    tgtseb15 = seb15[seb15.before1monthRscore==tgtbefore1monthRscore]
    tgtseb20 = seb20[seb20.before1monthRscore==tgtbefore1monthRscore]
    tgtseb25 = seb25[seb25.before1monthRscore==tgtbefore1monthRscore]
    tgtseb30 = seb30[seb30.before1monthRscore==tgtbefore1monthRscore]
    tgtseb35 = seb35[seb35.before1monthRscore==tgtbefore1monthRscore]
    tgtseb40 = seb40[seb40.before1monthRscore==tgtbefore1monthRscore]
    tgtseb45 = seb45[seb45.before1monthRscore==tgtbefore1monthRscore]
    tgtseb50 = seb50[seb50.before1monthRscore==tgtbefore1monthRscore]
    tgtseb55 = seb55[seb55.before1monthRscore==tgtbefore1monthRscore]   
    
    # target==drawdownscore
    tgtdrawdownscore=2

    tgtseb10 = seb10[seb10.drawdownscore==tgtdrawdownscore]
    tgtseb15 = seb15[seb15.drawdownscore==tgtdrawdownscore]
    tgtseb20 = seb20[seb20.drawdownscore==tgtdrawdownscore]
    tgtseb25 = seb25[seb25.drawdownscore==tgtdrawdownscore]
    tgtseb30 = seb30[seb30.drawdownscore==tgtdrawdownscore]
    tgtseb35 = seb35[seb35.drawdownscore==tgtdrawdownscore]
    tgtseb40 = seb40[seb40.drawdownscore==tgtdrawdownscore]
    tgtseb45 = seb45[seb45.drawdownscore==tgtdrawdownscore]
    tgtseb50 = seb50[seb50.drawdownscore==tgtdrawdownscore]
    tgtseb55 = seb55[seb55.drawdownscore==tgtdrawdownscore]  
    
    # target==ROE_OP
    tgtROE_OPscore=2

    tgtseb10 = seb10[seb10.ROE_OPscore==tgtROE_OPscore]
    tgtseb15 = seb15[seb15.ROE_OPscore==tgtROE_OPscore]
    tgtseb20 = seb20[seb20.ROE_OPscore==tgtROE_OPscore]
    tgtseb25 = seb25[seb25.ROE_OPscore==tgtROE_OPscore]
    tgtseb30 = seb30[seb30.ROE_OPscore==tgtROE_OPscore]
    tgtseb35 = seb35[seb35.ROE_OPscore==tgtROE_OPscore]
    tgtseb40 = seb40[seb40.ROE_OPscore==tgtROE_OPscore]
    tgtseb45 = seb45[seb45.ROE_OPscore==tgtROE_OPscore]
    tgtseb50 = seb50[seb50.ROE_OPscore==tgtROE_OPscore]
    tgtseb55 = seb55[seb55.ROE_OPscore==tgtROE_OPscore]  
    
    # target==ROE_OP & rtn
    tgtROE_OPscore=2
    tgtbefore1monthRscore=0
    
    tgtseb10 = seb10[seb10.ROE_OPscore==tgtROE_OPscore][seb10.before1monthRscore==tgtbefore1monthRscore]
    tgtseb15 = seb15[seb15.ROE_OPscore==tgtROE_OPscore][seb15.before1monthRscore==tgtbefore1monthRscore]
    tgtseb20 = seb20[seb20.ROE_OPscore==tgtROE_OPscore][seb20.before1monthRscore==tgtbefore1monthRscore]
    tgtseb25 = seb25[seb25.ROE_OPscore==tgtROE_OPscore][seb25.before1monthRscore==tgtbefore1monthRscore]
    tgtseb30 = seb30[seb30.ROE_OPscore==tgtROE_OPscore][seb30.before1monthRscore==tgtbefore1monthRscore]
    tgtseb35 = seb35[seb35.ROE_OPscore==tgtROE_OPscore][seb35.before1monthRscore==tgtbefore1monthRscore]
    tgtseb40 = seb40[seb40.ROE_OPscore==tgtROE_OPscore][seb40.before1monthRscore==tgtbefore1monthRscore]
    tgtseb45 = seb45[seb45.ROE_OPscore==tgtROE_OPscore][seb45.before1monthRscore==tgtbefore1monthRscore]
    tgtseb50 = seb50[seb50.ROE_OPscore==tgtROE_OPscore][seb50.before1monthRscore==tgtbefore1monthRscore]
    tgtseb55 = seb55[seb55.ROE_OPscore==tgtROE_OPscore][seb55.before1monthRscore==tgtbefore1monthRscore]  
    '''    
    #=============================================================================    
    
    # calculate return
    # by sector
    tgt10rtn = tgt10rtn.append(after1monthR[after1monthR.index==date][tgtseb10.index])
    tgt15rtn = tgt15rtn.append(after1monthR[after1monthR.index==date][tgtseb15.index])
    tgt20rtn = tgt20rtn.append(after1monthR[after1monthR.index==date][tgtseb20.index])
    tgt25rtn = tgt25rtn.append(after1monthR[after1monthR.index==date][tgtseb25.index])
    tgt30rtn = tgt30rtn.append(after1monthR[after1monthR.index==date][tgtseb30.index])
    tgt35rtn = tgt35rtn.append(after1monthR[after1monthR.index==date][tgtseb35.index])
    tgt40rtn = tgt40rtn.append(after1monthR[after1monthR.index==date][tgtseb40.index])
    tgt45rtn = tgt45rtn.append(after1monthR[after1monthR.index==date][tgtseb45.index])
    tgt50rtn = tgt50rtn.append(after1monthR[after1monthR.index==date][tgtseb50.index])
    tgt55rtn = tgt55rtn.append(after1monthR[after1monthR.index==date][tgtseb55.index])


   
#======================================================================================

# calculate mean return
meantgt10rtn = tgt10rtn.mean(axis=1)
meantgt15rtn = tgt15rtn.mean(axis=1)
meantgt20rtn = tgt20rtn.mean(axis=1)
meantgt25rtn = tgt25rtn.mean(axis=1)
meantgt30rtn = tgt30rtn.mean(axis=1)
meantgt35rtn = tgt35rtn.mean(axis=1)
meantgt40rtn = tgt40rtn.mean(axis=1)
meantgt45rtn = tgt45rtn.mean(axis=1)
meantgt50rtn = tgt50rtn.mean(axis=1)
meantgt55rtn = tgt55rtn.mean(axis=1)
#================================================================

# calculate cumulative mean return
cummeantgt10rtn = (meantgt10rtn+1).cumprod()
cummeantgt15rtn = (meantgt15rtn+1).cumprod()
cummeantgt20rtn = (meantgt20rtn+1).cumprod()
cummeantgt25rtn = (meantgt25rtn+1).cumprod()
cummeantgt30rtn = (meantgt30rtn+1).cumprod()
cummeantgt35rtn = (meantgt35rtn+1).cumprod()
cummeantgt40rtn = (meantgt40rtn+1).cumprod()
cummeantgt45rtn = (meantgt45rtn+1).cumprod()
cummeantgt50rtn = (meantgt50rtn+1).cumprod()
cummeantgt55rtn = (meantgt55rtn+1).cumprod()


# target portfolio    
#  10.에너지, 40.금융, 50,유틸리티, 55.통신서비스 제외
tgtrtn = pd.concat([tgt15rtn, tgt20rtn, tgt25rtn, tgt30rtn, tgt35rtn, tgt45rtn], axis=1)    
meantgtrtn = tgtrtn.mean(axis=1)
cummeantgtrtn = (meantgtrtn+1).cumprod()
#plotting
plt.plot(cummeantgt15rtn-1, 'r-')
plt.plot(cummeantgt20rtn-1, 'g-')
plt.plot(cummeantgt25rtn-1, 'b-')
plt.plot(cummeantgt30rtn-1, 'r--')
plt.plot(cummeantgt35rtn-1, 'g--')
plt.plot(cummeantgt45rtn-1, 'b--')
plt.plot(cummeantgtrtn-1, 'ro-')
plt.legend(['FGSC15', 'FGSC20', 'FGSC25', 'FGSC30', 'FGSC35', 'FGSC45', 'PF'], fontsize=10, loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
print("누적수익률 그래프")
print("===========================================")
print("FGSC15(소재):       {0:.2%}".format(cummeantgt15rtn[-2]-1))
print("FGSC20(산업재):     {0:.2%}".format(cummeantgt20rtn[-2]-1))
print("FGSC25(경기소비재): {0:.2%}".format(cummeantgt25rtn[-2]-1))
print("FGSC30(필수소비재): {0:.2%}".format(cummeantgt30rtn[-3]-1))
print("FGSC35(의료):       {0:.2%}".format(cummeantgt35rtn[-4]-1))
print("FGSC45(IT):         {0:.2%}".format(cummeantgt45rtn[-2]-1))
print("ALL:                {0:.2%}".format(cummeantgtrtn[-2]-1))

#======================================================================================
print("computation time = %0.3f" % (time.time()-t0))
#======================================================================================

#======================================================================================
# total stocks to excel
totalstocks = seb10total.append([seb15total, seb20total, seb25total, seb30total, seb35total, seb45total])
totalstocks.to_excel('temptotalstocks_s.xlsx')
#======================================================================================

