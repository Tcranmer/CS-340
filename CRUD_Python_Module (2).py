# Example Python Code to Insert a Document 
# Cranmer, Thomas
# CS 340
# CRUD Python implementation for MongoDB 
# CRUD_Python_Module.py
# Edited 25Jul26
# Update 3 - 8Aug26

from pymongo import MongoClient 
from bson.objectid import ObjectId 
from pprint import pprint

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username=None, password=None): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        #
        if username is None and password is None:
            USER = 'aacuser' 
            PASS = 'Kazters2!' 
        else:
            USER = username
            PASS = password
            
        
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    
    def nextIndex(self):
        index = self.database.animals.find_one(sort=[("_id", pymongo.DESCENDING)]) # Finds latest ID
        
        print(index) # Print to identify latest entry
        
        return index # Return ID of latest entry
        
            
    # Create method
    # @param: self - for initializing the database and logging in; data - the data as a list to use to insert into database
    # @return: True - if insert/query was successful; False - if no data passed, or the insert failed/query did not find data 
    def create(self, data):
        if data is not None: # Ensures data is present 
            self.database.animals.insert_one(data)  # data should be dictionary 
            
            if self.query(data) != [] or self.query(data) != False: # after insert, sends data to query to ensure it was inserted
                return True
            
            else: # Otherwise returns false, and tells user it failed
                print("Insert failed!")
                return False
            
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 
            return False

    # Query Method - To find documents in database based on sent list in parameters
    # @param: self - for initalizing the database and logging in; data - the data is a list to search through database for
    # @return: True (along with print out of documents) - If item found; [] - If item not found
    def query(self, data):
        if data is not None:
            
            searchItem = list(self.database.animals.find(data)) # Cursor data of find turned into readable list
            emptyList = [] # Empty list utilized in event query did not find data
            itemFound = False # Flag for if statement to inform user if item found or not
            
            for foundItem in searchItem: # For list item in list to print queried data
                pprint(foundItem)
                itemFound = True # searchItem has items and loop is entered, so flag is raised
                
            if itemFound == False:
                
                print("Data not found")
                return emptyList
            
            else:
                print("Item found!")
                
                return searchItem
            
            
        else:
            raise Exception("Nothing passed to find! Please pass item to method")
            return False
    
    # Update method to update existing documents in database
    # @param: self - For initializing the database and logging in
    # @param: data - Initial document for updating
    # @param: updateData - Update data to change data
    # @return: output string - X items have been updated, can be 0; False - No data passed
    def update(self, data, updateData): 
        if data is not None: #Ensure data is present to pass to update, otherwise raises exception and returns False
            
            searchItem = list(self.database.animals.find(data)) # Saves instances of each document that matches provided data
            updatedItems = 0 # To track how many documents were updated
            
            for foundItem in searchItem:
                self.database.animals.update_one({"animal_id": foundItem["animal_id"]}, updateData) # Did not know until now that python did not like updateOne()
                updatedItems += 1
            
            return print(updatedItems, " updated")
        
        else:
            raise Exception("No data passed. Nothing was updated")
            return False
    
    # Delete method to delete existing documents in database
    # @param: self - For initializing the database and logging in; data - Document list to be deleted from database
    # @return: output string - X items have been deleted, can be 0; False - No data passed
    def delete(self, data):
        if data is not None:
            
            searchItem = list(self.database.animals.find(data)) # Saves instances of each document that matches provided data
            deletedItems = 0 # To track how many documents were updated
            
            for foundItem in searchItem: 
                self.database.animals.delete_one(data) # Same with deleteOne()
                deletedItems += 1
            
            return print(deletedItems, " deleted")
        
        else:
            raise Exception("No data passed. Nothing deleted")
            return False
        
# EOF CRUD_Python_Module.py