import FDCAPI
from Amount import Amount
import NutritionFacts as nf
import pandas as pd
import utils

class Product:
    # Constructs a Product based on a given food (as JSON)
    def __init__(self, food):
        self.fdcId = food.get('fdcId')
        self.desc = utils.removeParentheses(food.get('description').upper())
        try:
            self.brand = food.get('brandName')
            self.totalSize = Amount.strInit(food.get('packageWeight'))
            self.servingSize = Amount(food.get('servingSize'), food.get('servingSizeUnit'))
        except:
            pass
        if not self.totalSize.exists():
            if food.get('dataType') == 'Survey (FNDDS)':
                self.totalSize = Amount(100.0, 'G')
        # NOTE: FDC stores nutrition facts per *container*, not *serving*
        self.nutritionFacts = nf.NutritionFacts(food)

    def idInit(self, fdcId: int):
        return Product(FDCAPI.searchID(fdcId))
    
    def toSeries(self):
        tempDict = {
            'FDC ID': self.fdcId,
            'Description': self.desc,
            'Brand': self.brand,
            'Size': self.totalSize,
            'Serving size': self.servingSize
        }
        return pd.Series({**tempDict, **self.nutritionFacts.toSeries()})
    
    def getDV(self, goal=nf.dvGoal):
        return self.nutritionFacts.getDV(goal)