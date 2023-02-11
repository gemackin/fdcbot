from FDCAPI import FDCAPI
from Product import Product

# Default system view
class UserInterface:
    def __init__(self):
        self.fdcapi = FDCAPI()
        self.fdcapi.modifyEnding(dataType='Branded', pageSize=50)
        self.stack = []

    # Adds the JSON of a specified food to the stack
    def search(self, query=None, choice=0, options=1):
        self.fdcapi.modifyEnding(pageSize = options)
        if query is None:
            print('Query: ', end="")
            query = input()
        self.fdcapi.search(query)
        if not choice:
            return
        if choice < 1:
            for i in range(options):
                print('{}. {}'.format(i+1, self.fdcapi.get(i).get('description')))
            print('Enter a number: ', end="")
            choice = int(input())
        self.choose(choice)

    # Picks the nth food item from the loaded JSON and adds it to the stack
    def choose(self, index:int):
        self.stack.append(self.fdcapi.get(index - 1))
        # print('Successfully loaded FDC ID {}.'.format(self.stack[-fdcapi.dataJSON.get('foods')[index - 1]1].get('fdcId')))
        self.stack.append(Product(self.stack.pop()))
        # print('Successfully loaded \"{}\".'.format(self.stack[-1].desc))

    # Returns the nth most recent search
    def get(self, index=0):
        return self.stack[-(index+1)]
    
    # Removes the nth most recent search from the stack and returns it
    def pop(self):
        return self.stack.pop()
    
    # Returns size of stack
    def size(self):
        return len(self.stack)