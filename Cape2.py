'''
This is a continutation of my Cape Series. 
This code will deal with two momentum strategies, a ranking strategy and a moving average one.
Please load data and help functions from the previous Cape post.
At the conclusion I will post the complete code of all of the strategies.
'''

#momentumstrat1 rolling 12 month not including current month returns. Pick top x
def momentumreturnrank(n): #go long highest n returns from past year
    rollingreturns=pd.rolling_apply(returnshift,12, lambda x:np.prod(1+x)-1) #rolling returns. Use returns shift to not get current month, because I lag everything back
    rollingreturns=rollingreturns.ix[finalreturns2.index] #match index
    rankedreturns=rollingreturns.rank(axis=1) #rank the returns on the columns
    onesmatrix=pd.DataFrame(np.ones(rankedreturns.shape),index=rankedreturns.index,columns=rankedreturns.columns) #generate ones matrix
    rankedreturnhighest=rankedreturns[0:len(rankedreturns)]>=rankedreturns.shape[1]-n #pull out greatest x. In this example x=5
    bestreturnssignals=onesmatrix*rankedreturnhighest #highest n set to 1. Anything else is 0. In this example x=5
    resultslong=bestreturnssignals*finalreturns2 #get results
    return(resultslong,bestreturnssignals) #return results and signals. Signals will be used later

momentumstrat1=pd.DataFrame(np.zeros((20,3)),index=range(1,21),columns=matrixcolumns)  #create optimization
for i in range(1,21): #how many securities am I going to go long in... optimization
    momentumstrat1.ix[i,:]=newstats(momentumreturnrank(i)[0])
momentumstrat1 #here is how the strategy performed with various cutoffs. Seems to get better with higher cutoffs

#Momentumstrat2 with moving average... Max to 24 months. I have used both a moving average and an exponential moving average
def momentum(prices,n,func): #n is length of moving average, func is what type of moving average. either pd.rolling_mean or pd.EWMA
    MAmatrix=func(prices,n) #get moving averages
    MAmatrix=MAmatrix.ix[n:] #get rid of NaNs
    prices=prices.ix[MAmatrix.index] #match length between prices and moving averages
    momentumover=prices>=MAmatrix #go long when the prices are greater than or equal to the moving averages
    onesmatrix=pd.DataFrame(np.ones(MAmatrix.shape),index=MAmatrix.index,columns=MAmatrix.columns) #create a ones matrix
    momentumlongsignals=onesmatrix*momentumover #great long signals by multiplying 
    momentumlongsignals=momentumlongsignals.ix[finalreturns2.index] #match index of returns and signals
    MAlong=momentumlongsignals*finalreturns2 #multiply signals by returns to get results
    momentumunder=prices<=MAmatrix #go short when prices are less than or equal to moving average
    momentumshortsignals=-onesmatrix*momentumunder #multiply by -1 to simulate short side
    momentumshortsignals=momentumshortsignals.ix[finalreturns2.index] #match index
    MAshort=momentumshortsignals*finalreturns2 #multiply to get final return
    return(MAlong,MAshort,momentumlongsignals,momentumshortsignals) #return MAlong and MAshort which are returns matrix, but also return momentumlongsignals which are 1's and 0's. This will help later

momentumstrat2priceslongMA=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long prices using MA
momentumstrat2priceslongMA.index.name='Prices MA long'
momentumstrat2priceslongEMA=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long prices using EMA
momentumstrat2priceslongEMA.index.name='Prices EMA long'

momentumstrat2pricesshortMA=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #short prices using MA
momentumstrat2pricesshortMA.index.name='Prices MA short'
momentumstrat2pricesshortEMA=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #short prices using EMA
momentumstrat2pricesshortEMA.index.name='Prices EMA short'

for i in range(2,25): #loop from n=2 to n=25 to see optimization
    momentumstrat2priceslongMA.ix[i,:]=newstats(momentum(priceshift,i,pd.rolling_mean)[0]) #long with MA
    momentumstrat2priceslongEMA.ix[i,:]=newstats(momentum(priceshift,i,pd.ewma)[0]) #long with EMA
    momentumstrat2pricesshortMA.ix[i,:]=newstats(momentum(priceshift,i,pd.rolling_mean)[1]) #short with MA
    momentumstrat2pricesshortEMA.ix[i,:]=newstats(momentum(priceshift,i,pd.ewma)[1]) #short with EMA

momentumstrat2priceslongMA #all provide similar performance
