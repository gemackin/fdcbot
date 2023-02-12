# FoodData Cental Bot (fdcbot)

This program calculates nutrition facts on food products and recipes using the FoodDataCentral API provided by the USDA.

## Features

+ Searching foods by name from multiple databases
+ Converting resulting JSON into a usable datatype to store ID, name, nutrition facts, etc.
+ Option to load recipe from a given URL (if website is supported) and store as usable datatype
+ Data visualization of nutrition facts via bar chart or exporting to .csv file

## Classes

### FDCAPI
+ `modifyEnding(**kwargs)`: Sets tags[^1] for the API to search by
[^1]: Tags include: query, dataType, pageNumber, and pageSize
+ `load()`: Loads the webpage and saves it as JSON
+ `search(query)`: Reloads the API with a specific query
+ `searchID(id)`: Reloads the API with the JSON of a specified food
+ `get()`: Returns the JSON of the nth food item in the JSON

### Recipe

+ `addIngredient(product, amount)`: Adds an amount of an ingredient to this recipe
+ `scale(scalar)`: Multiplies this recipe by a scalar multiple
+ `getNF()`: Returns the nutrition facts of this recipe as a NutritionFacts object
+ `getDV(goal)`: Returns a Series of nutrients mapped to their percentages relative to the goal
+ `getDF()`: Returns this Recipe as a Pandas DataFrame with a totals row of nutrition facts at the bottom
+ `exportCSV(path)`: Exports this Recipe to a .CSV file (examples in CSV folder)

### Product
+ `toSeries()`: Returns this Product as a Series
+ `getDV(goal)`: Returns a Series of nutrients mapped to their percentages relative to the goal

### NutritionFacts
+ `addFood(food)`: Adds the nutrition facts for a food (as JSON)
+ `addNF(*args)`: Adds multiple other NutritionFacts objects to this and returns the result
+ `scale(scalar)`: Scales the nutrition facts contained within by a scalar multiple
+ `toSeries()`: Returns this NutritionFacts as a Series
+ `getDV(goal)`: Returns a Series of nutrients mapped to their percentages relative to the goal

### Amount
+ `convert(newUnit)`: Converts this amount to a different unit, scaling the value as necessary
+ `addAmt(*args)`: Returns an addition between this and multiple other amounts
+ `scale(scalar)`: Scales the value associated with this by a scalar multiple
+ `divAmt(divisor)`: Returns the ratio difference between this and another Amount
+ `exists()`: Returns whether any of this Amount's fields are null

### UserInterface
+ `search(query, choice, options)`: Loads a queried food product, allowing the user to choice from a given number of options, or simply choosing the nth item specified by 'choice'
+ `choose(index)`: Adds the nth food item in the loaded JSON to the stack
+ `get(index)`: Returns the nth most recent item from the stack
+ `pop(index)`: Returns the nth most recent item from the stack and deletes it
+ `len()`: Returns the number of items in the stack

## Appendable Lists and Dictionaries

+ `dvGoal` (NutritionFacts.py): 
+ `units` (Amount.py): Maps accepted unit codes to their conversions to standardized amounts
+ `units` (RecipeUtils.py): List of accepted (mass) units and their corresponding unit codes
+ `substitutions` (RecipeUtils.py): List of ingredients that the search identifies incorrectly
+ `diffDataTypes` (RecipeUtils.py): List of ingredients that required searching non-branded databases
