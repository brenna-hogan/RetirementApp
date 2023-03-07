import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Retirement_Hist(P, split_equity, split_bond, lifetime, yre, legacy_capital):

    rolling_period = lifetime
    split_equity = split_equity/100
    split_bond = split_bond/100

    historical_data = pd.read_excel('histretSP.xls',sheet_name = "Returns by year", header = 17, skipfooter = 13)
    trials = int(len(historical_data)-rolling_period)

    principal_time = pd.DataFrame(0, index = range(lifetime), columns = range(trials))
    principal_time.iloc[0,:] = P
    years = list(historical_data.Year[0:int(len(historical_data)-rolling_period)])
    for k in range(trials):
        for i in range(1,lifetime):
            #principal_time[i, k] = principal_time[i-1, k] * (1 + historical_data.shift(-k)['S&P 500 (includes dividends)'][i] - historical_data.shift(-k)['Inflation Rate'][i]) + yre * (1 + historical_data.shift(-k)['Inflation Rate'][i])
            principal_time.iat[i, k] = split_equity*principal_time.iat[i-1, k] * (1 + historical_data.shift(-k)['S&P 500 (includes dividends)'][i] - historical_data.shift(-k)['Inflation Rate'][i]) + split_bond*principal_time.iat[i-1, k] * (1 + historical_data.shift(-k)['US T. Bond'][i] - historical_data.shift(-k)['Inflation Rate'][i]) + yre * (1 + historical_data.shift(-k)['Inflation Rate'][i])

    principal_time.columns = years

    sum_runs = 0
    count_successful = 0
    count_not_successful = 0
    for k in range(trials):
        sum_runs = sum_runs + principal_time.iat[-1, k]
        if int(principal_time.iat[-1, k]) >= legacy_capital:
            count_successful += 1
        else:
            count_not_successful += 1

    success_rate = round(count_successful / trials * 100, 1)
    failure_rate = count_not_successful / trials

    final_ave = int(sum_runs / trials)
    #final_median = int(principal_time.iloc[-1, :].median())
    final_min = min(principal_time.iloc[-1, :])
    final_max = max(principal_time.iloc[-1, :])

    worst_ind = principal_time.iloc[-1, :].idxmin()
    best_ind = principal_time.iloc[-1, :].idxmax()

    if len(principal_time.columns) % 2 != 0:
        mid = int(len(principal_time.columns) / 2)
        med_ind = principal_time.iloc[-1, :].sort_values(ascending=True).reset_index().iloc[mid]['index']
        final_median = int(principal_time[med_ind].iloc[-1])

    #print(final_ave, final_median, success_rate)
    #plt.plot(principal_time[worst_ind],'-')
    #plt.plot(principal_time[:,best_ind],'-')
    #plt.hist(principal_time.iloc[-1, :])
    #plt.show()
    return final_ave, final_median, success_rate, best_ind, worst_ind, med_ind, principal_time


if __name__ == "__main__":
    Retirement_Hist(6e6, 60, 40, 10, 0, 0)