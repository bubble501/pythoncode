'''
This is a continutation of my Cape Series. 
This code will deal with combining my value and momentum stratgies
Please load data and help functions from the first Cape post.
At the conclusion I will post the complete code of all of the strategies.
'''
#strat 5, Combine value and momentum
def valuemomentum(prices,n,func,cape,x,y): #value and momentum. momentum series, length, type, value series, value long, value short
    momentumlongsignals=momentum(prices,n,func)[2] #pull momentumlongsignals from previous momentum function, so I dont have to rewrite it
    capelongsignals=capenumber(capeshift,x)[2] #pull cape long signals from previous capenumber function, so I dont have to redo it
    combinedlongsignals=momentumlongsignals*capelongsignals #if both signals returned 1 (long) at same time, get signal for combined
    combinedlongreturns=combinedlongsignals*finalreturns2
    
    momentumshortsignals=momentum(prices,n,func)[3] #pull momentumshortsignals from previous momentum function, so I dont have to rewrite it
    capeshortsignals=capenumber(capeshift,y)[3]
    combinedshortsignals=momentumshortsignals*capeshortsignals
    combinedshortreturns=combinedshortsignals*finalreturns2

    combinedreturns=combinedlongreturns+combinedshortreturns
    return(combinedlongreturns,combinedshortreturns,combinedreturns)

strat4priceslongMACape15=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long returns using MA cape 15
strat4priceslongEMACape15=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long returns using EMA cape 15
strat4priceslongMACape20=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long returns using MA cape 20
strat4priceslongEMACape20=pd.DataFrame(np.zeros((23,3)),index=range(2,25),columns=matrixcolumns) #long returns using EMA cape 20
for i in range(2,25):
    strat4priceslongMACape15.ix[i,:]=newstats(valuemomentum(priceshift,i,pd.rolling_mean,capeshift,15,30)[0])
    strat4priceslongEMACape15.ix[i,:]=newstats(valuemomentum(priceshift,i,pd.ewma,capeshift,15,30)[0])
    strat4priceslongMACape20.ix[i,:]=newstats(valuemomentum(priceshift,i,pd.rolling_mean,capeshift,20,30)[0])
    strat4priceslongEMACape20.ix[i,:]=newstats(valuemomentum(priceshift,i,pd.ewma,capeshift,20,30)[0])
