import sys
import os
from recipeconverter import RecipeConverter
import NutritionFacts as nf
import pandas as pd
import RecipeUtils

class Recipe:
    def __init__(self, url=None):
        # {Product: Amount}
        self.ingredients = {}
        if url:
            # Temporarily disabling printing to console
            mystdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            # This following function loves to print to console and I don't want it to
            rc = RecipeConverter()
            originalRC = rc.convert_recipe_from_url(url)
            # Re-enabling printing to console
            sys.stdout = mystdout
            for line in originalRC[0].split('\n'):
                kvPair = RecipeUtils.parseLine(line)
                self.addIngredient(kvPair[0], kvPair[1])
        else:
            self.nutritionFacts = nf.NutritionFacts()

    # Multiples the amounts of all ingredients by a scalar multiple
    def scale(self, scalar):
        for key in self.ingredients.keys():
            self.ingredients[key] = self.ingredients.get(key).scale(scalar)
    
    # Sums the nutrition facts based on their comparative amounts
    # NOTE: FDC calculates nutrition facts per *container*, not *serving*
    def getNF(self):
        self.nutritionFacts = nf.NutritionFacts()
        for ing, amt in self.ingredients.items():
            if ing.totalSize:
                numServings = amt.divAmt(ing.totalSize)
            else:
                numServings = amt.value
            self.nutritionFacts.addNF(ing.nutritionFacts.scale(numServings))
        return self.nutritionFacts
    
    # Returns a series representing the percentages daily value of this recipe
    def getDV(self, goal=nf.dvGoal):
        return self.getNF().getDV(goal)
    
    # Adds an ingredient and its amount to this recipe
    def addIngredient(self, product, amount):
        self.ingredients[product] = amount.addAmt(self.ingredients.get(product))
    
    # Returns this recipe as a DataFrame of nutrition facts
    def getDF(self):
        rows = [self.getNF().toSeries()]
        for ing, amt in self.ingredients.items():
            # FDC's nutrition facts are based on total size
            if ing.totalSize.exists():
                numServings = amt.divAmt(ing.totalSize)
            else:
                numServings = amt.value
            ingNF = ing.nutritionFacts.scale(numServings)
            self.nutritionFacts.addNF(ingNF)
            seriesStart = pd.Series({
                'FDC ID': ing.fdcId,
                'Name': ing.desc,
                'Brand': ing.brand,
                'Amount': amt
            })
            temp = pd.concat([seriesStart, ingNF.toSeries()])
            rows.append(temp)
        self.nfdf = pd.concat(rows, axis=1).T

        # Reindexing to put names and IDs first
        self.nfdf = pd.concat([self.nfdf.iloc[:,-4:], self.nfdf.iloc[:,:-4]], axis=1)
        # Putting the totals row on the bottom
        firstRow = self.nfdf.iloc[0,]
        self.nfdf = self.nfdf.iloc[1:,]
        self.nfdf.loc[len(self.nfdf.index) + 1] = firstRow
        return self.nfdf
    
    # Exports this recipe as a .CSV file
    def exportCSV(self, path):
        self.getDF()
        return self.nfdf.to_csv(path, index = False)
