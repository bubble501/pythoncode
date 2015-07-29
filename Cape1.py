#import packages
import pandas as pd
import pandas.io.data
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math
from __future__ import division

#import data
price=pd.read_csv('Pricesfinal.csv',index_col='Date',parse_dates=True)
cape=pd.read_csv('SevenYearCapeSame.csv',index_col='Date',parse_dates=True)

#generate returns
ret=(price-price.shift(1))/price.shift(1) #calculate returns
cape=cape.sort_index(axis=1) #sort by column name to alphabetical order
price=price.sort_index(axis=1) #do same for prices for moving averages
capeshift=cape.tshift(1) #lag cape by one to get signals
finalreturns=(ret.sort_index(axis=1))
priceshift=price.shift(1) #Lag prices to generate signals
returnshift=finalreturns.shift(1) #lag returns to generate signals
#benchmark=stats(finalreturns2)[0]

#match lengths
finalreturns2=finalreturns.ix[capeshift.index] #match index. This is my returns matrix. Always match indexes and then multiply this matrix with signals. This means that returns always start at 2003-01.
finalreturns2=finalreturns2.dropna()
capeshift=capeshift.ix[finalreturns2.index]

#get stats
def returnseries(x): #I will use this to pull the vector of returns
    monthlyaverage=x.sum(1)/(x!=0).sum(1) #average each month
    monthlyaverage=monthlyaverage.replace([np.inf,-np.inf], np.nan) #turns inf and -inf to nan
    monthlyaverage=pd.DataFrame(monthlyaverage) #convert from time series to 
    return(monthlyaverage) #Use to get vector of returns... may have to change NaN to 0's. I will graph this return series in R, because there is no performance analytics package equivalent in python


def newstats(x): #I will use this to compare the strategies and search for the optimal strategy
    monthlyaverage=x.sum(1)/(x!=0).sum(1) #average each month
    monthlyaverage=monthlyaverage.replace([np.inf,-np.inf], np.nan) #turns inf and -inf to nan
    columnmeans=monthlyaverage.mean(axis=0,skipna=True) #average of entire months
    standarddev=monthlyaverage.std(skipna = True) #sd of monthly returns
    sharpe=math.sqrt(12)*columnmeans/standarddev #compute sharpe ratio
    cumret=(1+(monthlyaverage)).prod(skipna=True)-1 #compute cumulative returns
    cmgr=(((1+(monthlyaverage)).prod(skipna=True))**(1/np.count_nonzero(~np.isnan(monthlyaverage))))-1 #compute CMGR
    df=[sharpe,cumret,cmgr]
    return(df)
    
matrixcolumns=['SR Strat', 'cumret', 'CMGR'] #the order my function'newstats' will output in

#get buy and hold returns
monthlyaveragefinalreturns=pd.DataFrame(finalreturns2.mean(1),columns=['Returns'])
#monthlyaveragefinalreturns.to_csv('C:\Users\eqiu\Documents\Data\monthlyaveragefinalreturns.csv')

#Strat 1.. long lowest 5 cape ratios
def rankcaperatios(cape1,x): #returns lowest x cape countries. Input cape and x
    rankedcape=cape1.rank(axis=1) #rank the cape values on the columns
    onesmatrix=pd.DataFrame(np.ones(rankedcape.shape),index=rankedcape.index,columns=rankedcape.columns) #generate ones matrix
    rankedcapelow=rankedcape[0:len(rankedcape)]<=x #lowest x values I set to true
    lowestx=onesmatrix*rankedcapelow #lowest x set to 1. Anything else is 0. In this example x=5
    rankedcapehigh=rankedcape[0:len(rankedcape)]>=rankedcape.shape[1]-x #pull out greatest x. In this example x=5
    highestx=-onesmatrix*rankedcapehigh #multiply -1's matrix to ranked cape high signals
    resultslong=lowestx*finalreturns2 #multiply returns to long signals
    resultsshort=highestx*finalreturns2 #multiply returns to short signals
    return(resultslong,resultsshort) #return the long side then the short side

strat1lowest=pd.DataFrame(np.zeros((9,3)),index=range(1,10),columns=matrixcolumns) #create zeros matrix for longs. The columns will always be 3
strat1lowest.index.name='Lowest Ranks' #label matrix
strat1highest=pd.DataFrame(np.zeros((9,3)),index=range(1,10),columns=matrixcolumns) #create zeros matrix for shorts.
strat1highest.index.name='Highest Ranks' #label matrix
for i in range(1,10): #check for optimization by looping the 10 lowest ranks
    strat1lowest.ix[i,:]=newstats(rankcaperatios(capeshift,i)[0]) #this output has all of the different possible combinaions for ranks. Anything from 5-9 seems like a good choice
for i in range(1,10): #check for optimization by looping the 10 lowest ranks
    strat1highest.ix[i,:]=newstats(rankcaperatios(capeshift,i)[1])
    
#Strat 2 long under x short over y
def capenumber(cape2,x=15,y=30): #x is for under, y is for over
    onesmatrix=pd.DataFrame(np.ones(cape2.shape),index=cape2.index,columns=cape2.columns) #generate ones matrix
    capeunder=cape2[0:len(cape2)]<=x #Go through all the rows. Set capes that are less than x to True, otherwise False. X defaults to 15
    underx=capeunder*onesmatrix #multiply by ones matrix to turn True to 1 and False to 0
    capeover=cape2[0:len(cape2)]>=y #Go through all the rows. Set capes that are greater than y to True, otherwise False. Y defaults to 30
    overy=capeover*-onesmatrix #multiply by negative ones matrix to turn True to -1 and False to 0. (To take negative position against high cape ratios)
    resultsunder=underx*finalreturns2 #multiply signals by returns
    resultsover=overy*finalreturns2 #multiply signals by returns
    return(resultsunder,resultsover,underx,overy) #pull returns for over strategy and under strategy. Also pull signals. Will save time later

strat2under=pd.DataFrame(np.zeros((16,3)),index=range(5,21),columns=matrixcolumns) 
strat2under.index.name='Cape ratios under' #label matrix
for i in range(5,21):
    strat2under.ix[i,:]=newstats(capenumber(capeshift,x=i)[0])

strat2over=pd.DataFrame(np.zeros((6,3)),index=range(30,36),columns=matrixcolumns)
strat2over.index.name='Cape ratios over'
for i in range(30,36):
    strat2over.ix[i,:]=newstats(capenumber(capeshift,y=i)[1])
