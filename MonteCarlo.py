import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Wealth in Retirement simulation - opensource version of Money Guide Pro 
Args:
-P = principal at time t0
-mean_return
-st_dev
-lifetime
-trials = number of trials in MC simulation
-inf = inflation
-yre = yearly retirement expenses (think of as yearly income drawn from portfolio)
"""
def Retirement_MC(P, mean_return, st_dev, lifetime, trials, inf, yre, legacy_capital):

    return_set = np.random.normal(loc=mean_return, scale=st_dev, size=(lifetime,trials))

    principal_time = pd.DataFrame(0, index=range(lifetime), columns=range(trials))
    principal_time.iloc[0, :] = P
    for k in range(trials):
        for i in range(1, lifetime):
            principal_time.iat[i, k] = principal_time.iat[i-1, k] * (1 + return_set[i, k]/100 - inf/100) + yre * (1 + inf/100)
    # Find average final principal among the trials
    # Success of retirement plan (i.e., don't run out of money)

    sum_runs = 0
    count_successful = 0
    count_not_successful = 0
    for k in range(trials): 
        sum_runs = sum_runs + principal_time.iat[-1,k]
        if int(principal_time.iat[-1,k]) >= legacy_capital:
            count_successful += 1
        else:
            count_not_successful += 1
            
    success_rate = round(count_successful / trials * 100, 1)
    failure_rate = count_not_successful/trials
    final_ave = int(sum_runs / trials)
    #final_median = int(principal_time.iloc[-1,:].median())
    final_min = principal_time.iloc[-1,:].min()
    final_max = principal_time.iloc[-1,:].max()
    worst_ind = principal_time.iloc[-1, :].idxmin()
    best_ind = principal_time.iloc[-1, :].idxmax()
    if len(principal_time.columns) % 2 != 0:
        mid = int(len(principal_time.columns) / 2)
        med_ind = principal_time.iloc[-1, :].sort_values(ascending=True).reset_index().iloc[mid]['index']
        final_median = int(principal_time[med_ind].iloc[-1])
    else:
        mid = int(len(principal_time.columns) / 2)
        med_ind = principal_time.iloc[-1, :].sort_values(ascending=True).reset_index().iloc[mid]['index']
        final_median = int(principal_time[med_ind].iloc[-1])

    plt.hist(principal_time.iloc[-1,:])

    return final_ave, final_median, success_rate, best_ind, worst_ind, med_ind, principal_time
    #plot histogram with ending balance
    #plt.hist(princ_time[:,lifetime-1],histtype=u'step', density=True)

    #plt.plot(principle_time[0,:],'-')
    #plt.ylim(0,12e6)
    #plt.show()
    
    

#principal
P = 6.3e6
#return parameters
mean_return = 11.16
st_dev = 27.53
lifetime = 30
#number of trials in MC
trials = 1000
#inflation
inf = 2.5
#yearly retirement expenses (can be net contributions - withdrawls)
yre = 0
#legacy capital
legacy_capital = 0
print(Retirement_MC(P, mean_return, st_dev, lifetime, trials, inf, yre, legacy_capital))





