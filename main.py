import os
from Recipe import Recipe
import Plot

url = 'https://cooking.nytimes.com/recipes/1014826-quintessential-chocolate-chip-cookies'
rc = Recipe(url)

# Plot.plotDV(rc.getNF(), 'seaborn')

path = os.getcwd() + '\\CSV\\file.csv'
rc.exportCSV(path)