import os
from Recipe import Recipe
import Plot

cookieURL = 'https://cooking.nytimes.com/recipes/1014826-quintessential-chocolate-chip-cookies'
pumpkinBreadURL = 'https://www.foodnetwork.com/recipes/pumpkin-bread-recipe-1957866'

rccc = Recipe(cookieURL)
rcpb = Recipe(pumpkinBreadURL)

# Plot.plotDV(rccc.getNF(), 'seaborn')

path = os.getcwd() + '\\CSV\\{}.csv'
rccc.exportCSV(path.format('chocolateChipCookies'))
rcpb.exportCSV(path.format('pumpkinBread'))