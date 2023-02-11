from urllib.request import urlopen
import json

class FDCAPI:
    def __init__(self):
        # The API is free if you want to use it. You don't need to steal my key
        self.key = '8usVAivbuFGYPabUM4Kis8okwoXqLv9hWgCrZxPl'
        self.url = 'https://api.nal.usda.gov/fdc/v1/'
        self.tags = {'pageNumber': 1, 'pageSize': 50}
        self.modifyEnding()
    
    # Updates the URL tags
    # Allowed arguments: dataType, query, pageNumber, pageSize
    def modifyEnding(self, **kwargs):
        self.tags.update(kwargs)

    # Loads the JSON for the current URL
    # I try to use this method sparingly and with low pageSize since it is pretty slow
    def load(self):
        response = urlopen(self.url + self.path.format(k=self.key, q=self.query) + self.getEnding())
        self.dataJSON = json.loads(response.read())
        return self.dataJSON
    
    # Searches a string query and loads the page
    def search(self, query):
        self.path = 'foods/search?api_key={k}&query={q}'
        self.query = query.replace(' ', '%20')
        self.tags['pageNumber'] = 1
        return self.load()

    # Searches for a specific FDC ID and loads the page
    def searchID(self, id):
        self.path = 'food/{q}?api_key={k}'
        self.query = id
        self.tags['pageNumber'] = 1
        return self.load()
    
    # Gives the updates URL ending based on 'tags'
    def getEnding(self):
        ending = ''
        for key, value in self.tags.items():
            ending += '&{}={}'.format(key, value)
        return ending
    
    # Gets the nth food item from the JSON
    def get(self, index):
        perPage = self.tags.get('pageSize')
        page = int(index / perPage) + 1
        newIndex = index - (page - 1) * perPage

        if page == self.tags.get('pageNumber'):
            return self.dataJSON.get('foods')[newIndex]
        
        # Turning the page if the search result is on a different page
        if page < self.dataJSON.get('totalPages'):
            self.modifyEnding(pageNumber = page)
            self.load()
            return self.dataJSON.get('foods')[newIndex]
        
        raise IndexError('End of search results')
