import recipeconverter as rc
from Amount import Amount
from Product import Product
import utils

# List of acceptable units to import
# Elements in each list are equal, with the unit code at the front
units = [
    ['g', 'gram', 'gramme'],
    ['mg', 'milligram', 'milligramme'],
    ['kg', 'kilogram', 'kilogramme'],
]

# List of ingredient names that the API gets wrong
substitutions = {
     'vanilla': 'vanilla extract' # This returned "Vanilla Cupcakes"
}

# List of ingredient names that are never branded
diffDataTypes = {
     'egg': 'Foundation',
     'water': 'Survey%20(FNDDS)',
     'oil': 'Survey%20(FNDDS)'
}

# Turns a unit string into a standardized code
# (ex: 'grams' -> 'G')
def getUnitCode(unit):
    for group in units:
            for element in group:
                if unit == element or unit == element + 's':
                     return group[0]
    return None

# Turns a line from the list of ingredients into usable datatypes
# (Ex. '1 gram cinnamon' -> 1.0, 'G', 'cinnamon')
def parseLine(line):
    words = line.split()
    try:
        value = float(words[0])
    except:
         value = None
         words.insert(0, '')
    unit = getUnitCode(words[1].lower())
    if not unit: # If unit is not recognized
        try:
             # Attempting metric conversion just in case
             metricConversion = rc.convert_volume_to_mass(line)
             if metricConversion == line:
                  raise Exception()
             return parseLine(metricConversion)
        except:
             pass
        words.insert(1, '') # Make the second word part of the food name
    name = utils.formatName(utils.concatTuple(tuple(words[2:])))

    for before, after in substitutions.items():
         if name.lower() == before:
              name = after
    print('Ingredient:', utils.formatName(line))

    dataType = 'Branded'
    for item in diffDataTypes.keys():
         if name.find(item) >= 0:
              dataType = diffDataTypes.get(item)
    
    try:
        product = Product(utils.getFood(name, dtype = dataType))
        print('--- Loaded "{}", '.format(utils.formatName(product.desc)), end = '')
    except:
         product = None
         print('--- Failed to load product, ', end = '')

    amount = Amount(value, unit)
    if not unit and product.servingSize.exists():
        try:
            amount = product.servingSize.scale(value)
        except:
             pass
    print(amount)

    return (product, amount)
