from MonteCarlo import Retirement_MC
from HistReturns import Retirement_Hist
from HistReturnsPeriod import Retirement_Hist_Period
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components


def inputs():
    option = st.sidebar.selectbox("Type of Simulation", options = ('Monte Carlo', 'Historical Returns', 'Historical Returns by Period'))
    st.sidebar.write('You selected:', option +'.', 'Read more about simulation types here.')
    return option

def main():
    option = inputs()
    if option == 'Monte Carlo':
        st.sidebar.header("Inputs")
        st.sidebar.write("Please input $ amounts **without** commas")
        principal = st.sidebar.number_input('Principal ($)', value=int())
        lifetime = st.sidebar.number_input('Lifetime (years)', value=30)
        yre = st.sidebar.number_input('Yearly Retirement Contributions/Expenses ($)*', value=int())
        st.sidebar.write("*if net yearly expenses, please include negative sign (-)")
        legacy_capital = st.sidebar.number_input('Legacy Capital ($)', value=int())

        st.sidebar.header("Parameters of Distribution")
        mean_return = st.sidebar.number_input('Mean (%)', value = 11.2)
        st_dev = st.sidebar.number_input('Standard Deviation (%)', value = 18)
        trials = st.sidebar.number_input('Number of Trials', value = 1001)
        inf = st.sidebar.number_input('Rate of Inflation (%)', value = 2.5)

        button = st.sidebar.button('Run simulation!')
        if button:
            final_ave, final_median, success_rate, best_ind, worst_ind, med_ind, data = Retirement_MC(principal, mean_return, st_dev, lifetime,
                                                                        trials, inf, yre, legacy_capital)
            st.header(f'Your success rate is {success_rate}%')
            st.header(f'Time Evolution of Principal')
            st.write(f'Mean: $ {final_ave:,}')
            st.write(f'Median: $ {final_median:,}')

            fig = plt.figure()
            plt.plot(data[best_ind][:], color = 'green', label = "Best")
            plt.plot(data[med_ind][:], color = 'yellow', label = "Median")
            plt.plot(data[worst_ind][:], color= 'red', label = "Worst")
            plt.legend(loc = "upper left")
            plt.xlabel("Years")
            plt.ylabel("Principal ($)")
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)

    if option == 'Historical Returns':
        st.sidebar.header("Inputs")
        st.sidebar.write("Please input $ amounts **without** commas")
        principal = st.sidebar.number_input('Principal ($)', value=int())
        lifetime = st.sidebar.number_input('Lifetime (years)', value=30)
        yre = st.sidebar.number_input('Yearly Retirement Contributions/Expenses ($)*', value=int())
        st.sidebar.write("*if net yearly expenses, please include negative sign (-)")
        legacy_capital = st.sidebar.number_input('Legacy Capital ($)', value=int())

        split_equity = st.sidebar.number_input('Equity Split (%)', value = 60)
        split_bond = st.sidebar.number_input('Bond Split (%)', value = 40)
        if split_equity + split_bond != 100:
            st.error('Equity + Bond Split must equal 100%!', icon="🚨")

        button = st.sidebar.button('Run simulation!')
        if button:
            final_ave, final_median, success_rate, best_ind, worst_ind, med_ind, data = Retirement_Hist(principal, split_equity, split_bond, lifetime, yre, legacy_capital)
            st.header(f'Your success rate is {success_rate}%')
            st.header(f'Time Evolution of Principal')
            st.write(f'Mean: $ {final_ave:,}')
            st.write(f'Median: $ {final_median:,}')
            st.write(f'Best {lifetime}-year period: **:green[{best_ind} - {best_ind + lifetime}]**')
            st.write(f'Worst {lifetime}-year period: **:red[{worst_ind} - {worst_ind + lifetime}]**')


            fig = plt.figure()
            plt.plot(data[best_ind][:], color = 'green', label = "Best")
            plt.plot(data[med_ind][:], color = 'yellow', label = "Median")
            plt.plot(data[worst_ind][:], color= 'red', label = "Worst")
            plt.legend(loc = "upper left")
            plt.xlabel("Years")
            plt.ylabel("Principal ($)")
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)

    if option == 'Historical Returns by Period':
        st.sidebar.header("Inputs")
        st.sidebar.write("Please input $ amounts **without** commas")
        principal = st.sidebar.number_input('Principal ($)', value=int())
        lifetime = st.sidebar.number_input('Lifetime (years)', value=30)
        yre = st.sidebar.number_input('Yearly Retirement Contributions/Expenses ($)*', value=int())
        st.sidebar.write("*if net yearly expenses, please include negative sign (-)")
        legacy_capital = st.sidebar.number_input('Legacy Capital ($)', value=int())

        start_year = st.sidebar.number_input('Start Year*', value = 1928)
        st.sidebar.write("*Data available from 1928 to 2022")
        split_equity = st.sidebar.number_input('Equity Split (%)', value = 60)
        split_bond = st.sidebar.number_input('Bond Split (%)', value = 40)
        if split_equity + split_bond != 100:
            st.error('Equity + Bond Split must equal 100%!', icon="🚨")
        if start_year + lifetime > 2022:
            st.error('Period falls outside of available data. Please enter a Start Year + Lifetime which end before the beginning of 2023.',icon="🚨")

        button = st.sidebar.button('Run simulation!')

        if button:
            data, success = Retirement_Hist_Period(principal, split_equity, split_bond, lifetime, yre, legacy_capital, start_year)
            st.header(f'Time Evolution of Principal')
            st.subheader(f'from {start_year} - {start_year + lifetime}')
            if success == True:
                st.write("You were successful! :balloon:")
            else:
                st.write("You were not successful. :frowning:")
            fig, ax = plt.subplots()
            plt.plot(data["Year"], data["Principal ($)"])
            ax.xaxis.set_major_formatter('{x:1.0f}')
            plt.xlabel("Year")
            plt.ylabel("Principal ($)")
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)

    st.sidebar.write("Made in Streamlit by Dr. Brenna Hogan :sparkles:")



if __name__ == '__main__':
    main()