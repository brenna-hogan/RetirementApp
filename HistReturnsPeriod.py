#Check how portfolio would have performed during a certain period
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Retirement_Hist_Period(P, split_equity, split_bond, lifetime, yre, legacy_capital, time1):

    split_equity = split_equity/100
    split_bond = split_bond/100

    historical_data = pd.read_excel('histretSP.xls',sheet_name = "Returns by year", header = 17, skipfooter = 13)

    loc1 = historical_data[historical_data.Year == time1].index[0]
    years = historical_data.Year[loc1:loc1+lifetime+1]

    principal_time = pd.Series(0, index = range((lifetime+1)), name = 'Principal ($)')
    principal_time[0] = P
    for k in range(loc1, loc1+lifetime):
        i = k-loc1+1
        #principal_time[i, k] = principal_time[i-1, k] * (1 + historical_data.shift(-k)['S&P 500 (includes dividends)'][i] - historical_data.shift(-k)['Inflation Rate'][i]) + yre * (1 + historical_data.shift(-k)['Inflation Rate'][i])
        principal_time[i] = split_equity*principal_time[i-1] * (1 + historical_data['S&P 500 (includes dividends)'][k] - historical_data['Inflation Rate'][k]) + split_bond*principal_time[i-1] * (1 + historical_data['US T. Bond'][k] - historical_data['Inflation Rate'][k]) + yre * (1 + historical_data['Inflation Rate'][k])

    if principal_time.iloc[-1] >= legacy_capital:
        success = True
    else:
        success = False
    yearvsprincipal = pd.concat([years.reset_index(drop = True), principal_time], axis = 1)
    #yearvsprincipal = yearvsprincipal.astype({"Year": "string"})
    #plt.plot(yearvsprincipal['Year'],yearvsprincipal['Principal ($)'])
    #plt.show()
    return yearvsprincipal, success

if __name__ == "__main__":
    Retirement_Hist_Period(6e6, 100, 0, 10, 0, 0, 2012)