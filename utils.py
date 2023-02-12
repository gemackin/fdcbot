import Amount
from FDCAPI import FDCAPI
from recipeconverter import RecipeConverter

# Similar to split() but allows multiple delimiters
def delimit(string, *delimiters):
    parts = [string]
    for delimiter in delimiters:
        for i in range(len(parts)):
            newParts = parts[i].split(delimiter)
            parts[i:i] = newParts
            i += len(newParts)
    return parts

# Concatenates the values of a tuple into a string
def concatTuple(tup, begin="", between=" ", end=""):
    if not type(tup) is tuple:
        return tup
    for element in tup:
        begin += str(element) + between
    return begin[:-len(between)] + end

# Returns a food (as JSON) based on a string query for it 
def getFood(name, dtype = 'Branded'):
    fdcapi = FDCAPI()
    # Only Branded items because most others don't have sizes listed
    # Only 1 item per page to save time and resources
    fdcapi.modifyEnding(dataType = dtype, pageSize = 1)
    fdcapi.search(name)
    index = 0
    units = Amount.units.keys()
    while index < 5:
        food = fdcapi.get(index)
        weightString = food.get('packageWeight')
        size = Amount.Amount.strInit(weightString)
        # Testing if maybe metric conversion is necessary
        if not size.unit in units and weightString:
            weights = weightString.split('/')
            rc = RecipeConverter()
            i = 0
            while not size.unit in units and i < len(weights):
                try:
                    metricConversion = rc.convert_volume_to_mass(weights[i] + ' ' + name)
                    size = Amount.Amount.strInit(metricConversion)
                except:
                    pass
                i += 1
        if size.exists() and size.unit in units or not dtype == 'Branded':
            return food
        index += 1
    if dtype == 'Survey%20(FNDDS)':
        raise Exception('Food not found')
    else:
        return getFood(name, 'Survey%20(FNDDS)')

# Determines if a food (as JSON) has a valid serving size
# Not in use since I realized FDC's facts were by container, not serving size
def validServingSize(food, units):
    ssu = food.get('servingSizeUnit')
    return food.get('servingSize') and ssu and ssu.upper() in units

# Removes all parentheticals from strings
def removeParentheses(string):
    parenCount = 0
    i = 0
    while i < len(string):
        if string[i] == '(':
            parenCount += 1
        if string[i] == ')':
            parenCount -= 1
            if parenCount < 1:
                # Length of the replaced expression
                string = string[:string.find('(')-1] + string[i+1:]
                i = -1
        i += 1
    return string

# Making names of foods and nutrients look pretty :D
def formatName(name):
     return removeParentheses(name).split(',')[0]