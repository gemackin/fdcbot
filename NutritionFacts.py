import FDCAPI
from Amount import Amount
import utils # delimit()
import pandas as pd # Series

# Recommended DV by the FDA as of 2/25/22
# This dictionary also serves as a list of nutrients to track
dvGoal = {
    'Energy': Amount(2000.0, 'KCAL'),
    'Protein': Amount(50.0, 'G'),
    'Carbohydrate, by difference': Amount(275.0, 'G'),
    'Fiber, total dietary': Amount(28.0, 'G'),
    'Sugars, total including NLEA': Amount(50.0, 'G'),
    'Total lipid (fat)': Amount(78.0, 'G'),
    'Cholesterol': Amount(300.0, 'MG'),
    'Vitamin A, IU': Amount(3000.0, 'IU'),
    'Vitamin C, total ascorbic acid': Amount(90.0, 'MG'),
    'Sodium, Na': Amount(2300.0, 'MG'),
    'Iron, Fe': Amount(18.0, 'MG'),
    'Magnesium, Mg': Amount(420.0, 'MG'),
    'Calcium, Ca': Amount(1300.0, 'MG'),
    'Potassium, K': Amount(4700.0, 'MG')
}

class NutritionFacts:
    def __init__(self, food=None, factsDict={}):
        self.facts = factsDict
        if food:
            self.addFood(food)

    # Constructor for specific FDC ID
    def idInit(fdcId:int):
        return NutritionFacts(FDCAPI.searchID(fdcId))
    
    # Adds the nutrition facts for a food (as JSON)
    def addFood(self, food):
        tempDict = self.facts.copy()
        for trackedNutrient in dvGoal:
            key = utils.delimit(trackedNutrient, ',', '(')[0].rstrip()
            for nutrient in food.get('foodNutrients'):
                if nutrient.get('nutrientName') == trackedNutrient:
                    value = Amount(nutrient.get('value'), nutrient.get('unitName'))
                    tempDict[key] = value.addAmt(tempDict.get(key))
            if tempDict.get(key) is None:
                tempDict[key] = Amount()
        self.facts = tempDict
    
    # align: 0 = combines label & unit; 1 = value & unit
    # concat: 0 = combines as tuple; 1 = combines as string
    def toSeries(self, align=True, concat=True, keep=False):
        if keep:
            return pd.Series(self.facts)
        tempDict = {}
        for fact, amount in self.facts.items():
            if align:
                key = fact
                value = str(amount)
            else:
                key = (fact, (amount.unit).lower())
                try:
                    value = amount.value
                except:
                    value = None
            if concat:
                key = utils.concatTuple(key, between=' (', end=')')
                value = utils.concatTuple(value)
            tempDict[key] = value
        return pd.Series(tempDict)
    
    # Adds the facts in another NutritionFacts object to this one
    def addNF(self, *args):
        tempDict = self.facts.copy()
        for arg in args:
            for key, value in arg.facts.items():
                tempDict[key] = value.addAmt(tempDict.get(key))
        self.facts = tempDict
        return self
    
    # Multiplies all nutrition facts by a scalar multiple
    def scale(self, scalar):
        tempDict = {}
        for key, value in self.facts.items():
            tempDict[key] = value.scale(scalar)
        return self

    # Returns nutrition facts as a Series of percentages daily value
    def getDV(self, goal=dvGoal):
        percentages = {}
        for key, value in goal.items():
            myKey = utils.delimit(key, ',', '(')[0].rstrip()
            reciprocal = value.divAmt(self.facts.get(myKey))
            if reciprocal:
                percentages[utils.formatName(key)] = 1 / reciprocal
            # Might need an else statement here
        return pd.Series(percentages)