import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

# Plots the daily value of nutrients
def plotDV(nf, lib='pandas'):
    mysrs = nf.getDV().sort_values(na_position = 'first')
    mydf = pd.DataFrame([mysrs.index, mysrs]).transpose()
    mydf.columns = ['Nutrient', 'Percentage Daily Value']
    # mydf.sort_values('Percentage Daily Value', axis=0, na_position='first')
    match lib:
        case 'pandas':
            myplot = mysrs.plot.barh(color='green')
            # TO DO: Show percents on bars and on the x-axis
        case 'seaborn':
            mydf = mydf.iloc[::-1]
            mydf['Percentage Daily Value'] = mydf['Percentage Daily Value'] * 100
            ax = sns.barplot(x = 'Percentage Daily Value', y = 'Nutrient', data = mydf)
            ax.bar_label(ax.containers[0], fmt = '%d%%')
            ax.tick_params(labelsize = 8)
            ax.set(ylabel = None)
            ax.margins(x = 0.1)
    plt.title('Nutrients by Daily Value')
    plt.gcf().set_size_inches((7, 5))
    plt.subplots_adjust(top = 0.95, left = 0.15)
    plt.show()