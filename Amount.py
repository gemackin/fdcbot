# Essentially just a tuple of value and unit, but with added functionality
class Amount:
    def __init__(self, value=None, unit=None):
        self.value = value
        self.unit = unit
        if unit:
            # Trying to avoid confusion with 'g' vs. 'G'
            self.unit = unit.upper()
    
    # Constructs Amount based on a string (e.g. '1.5 kg')
    # Can also pick one of multiple measurements separated by slashes
    def strInit(string):
        try:
            strings = string.split('/')
        except:
            return Amount()
        if len(strings) == 1:
            split = strings[0].split()
            if split[1]:
                temp = split[1]
            else:
                temp = None
            return Amount(float(split[0]), temp)
        # This code only runs if there were multiple measurements
        amounts = []
        for string in strings:
            amounts.append(Amount.strInit(string))
        # Picking the best of multiple amounts
        # Precedence is given to units earlier in the 'units' dict ('G', 'MG', etc.)
        for unit in units.keys():
            for amount in amounts:
                if amount.unit == unit:
                    return amount
        return amounts[0]
        # # Gathering data for error message
        # unrecogUnits = ""
        # for amount in amounts:
        #     unrecogUnits += str(amount.unit) + ', '
        # raise Exception('Unrecognized units ({}).'.format(unrecogUnits[:-2]))
    
    # Converts this Amount to a new unit based on the 'units' conversion dict
    def convert(self, newUnit):
        # Equality check to save time and resources
        if self.unit == newUnit:
            return self
        # Can't convert from unit to unit if either unit doesn't exist
        if not (self.unit and self.value):
            return Amount(0, newUnit)
        if (self.unit in units) and (newUnit in units):
            stdUnit = units.get(self.unit)
            stdNewUnit = units.get(newUnit)
            if stdUnit.unit == stdNewUnit.unit:
                return Amount(self.value * stdUnit.value / stdNewUnit.value, newUnit)
            raise Exception('Units do not match ({}, {}).'\
                .format(stdUnit.unit, stdNewUnit.unit))
        else:
            raise Exception('Unrecognized units ({}, {}).'.format(self.unit, newUnit))
    
    # Returns the addition of multiple Amounts to this
    # Does not affect the value or unit of this object
    def addAmt(self, *args):
        sum = self.value
        for arg in args:
            if arg:
                if not self.exists():
                    self = arg
                    sum = arg.value
                else:
                    sum += arg.convert(self.unit).value
        return Amount(sum, self.unit)
    
    # Multiplies this Amount by a scalar multiple
    def scale(self, scalar):
        if scalar and self.value:
            self.value *= scalar
        return self
    
    # Divides this by another Amount
    # Used for finding percent daily value
    def divAmt(self, divisor):
        divisorReal = divisor and divisor.exists() and divisor.value != 0
        if not (self.unit and (self.unit in units) and divisorReal):
            return None
        return self.value / divisor.convert(self.unit).value
    
    def __str__(self):
        if not (self.value is None) and not self.unit:
            return str(round(self.value)) + ' units'
        if not self.exists():
            return ''
        return str(round(self.value)) + ' ' + self.unit.lower()
    
    def exists(self):
        return not (self.value is None) and self.unit
    
    def copy(self):
        return Amount(self.value, self.unit)

# Recognized units as converted to a standardized form
units = {
    'G': Amount(1.0, 'G'),
    'MG': Amount(0.001, 'G'),
    'KG': Amount(1000, 'G'),
    'OZ': Amount(28.34952, 'G'),
    'LB': Amount(453.592, 'G'),
    'LBS': Amount(453.592, 'G'),
    'KCAL': Amount(1.0, 'KCAL'),
    'KJ': Amount(0.239006, 'KCAL'),
    'IU': Amount(1.0, 'IU')
}