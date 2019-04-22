import pprint
import datetime
import json
from bson import json_util, SON
from pymongo import MongoClient

# These setup the connection to the server and define the 
# database and collection to be used. 
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

# This function is used to create a document using the 
# insert function. It takes a document as an argument and 
# if the insert is successful it will return true. 
def insertDocument(document):
  try:
  	result = collection.insert(document)
  except OperationFailure as of:
  	abort(400, str(of))
  return True

# This function is used to read a document using the 
# find_one function. It takes the search criteria as an 
# argument and returns the found document
def readDocument(ticker):
  try:
    read = collection.find_one(ticker)
  except OperationFailure as of:
    abort(400, str(of))
  return read
    
# This function is used to update a document using the 
# update_one function. It takes a search criteria and the 
# information to be updated as arguments and has no return
def updateDocument(rDoc, uDoc):
  try:
    result = collection.update_one(rDoc, uDoc)
  except OperationFailure as of:
    abort(400, str(of))
    
# This function is used to delete a document using the 
# delete_one function. It takes the search criteria as an
# argument it then prints the document to be deleted and then deletes the 
# document. 
def deleteDocument(dDoc):
  try:
    pprint.pprint(collection.find_one(dDoc))
    result = collection.delete_one(dDoc)
  except OperationFailure as of:
    abort(400, str(of))
  
# This function is used to test and run the CRUD functions that we 
# created above
def crud():
	# This document is a test document that is used to test the 
	# functionality of the system 
  testDoc = {
        "Ticker" : "TEST",
        "Profit Margin" : 0.137,
        "Institutional Ownership" : 0.847,
        "EPS growth past 5 years" : 0.158,
        "Total Debt/Equity" : 0.56,
        "Current Ratio" : 3,
        "Return on Assets" : 0.089,
        "Sector" : "Healthcare",
        "P/S" : 2.54,
        "Change from Open" : -0.0148,
        "Performance (YTD)" : 0.2605,
        "Performance (Week)" : 0.0031,
        "Quick Ratio" : 2.3,
        "Insider Transactions" : -0.1352,
        "P/B" : 3.63,
        "EPS growth quarter over quarter" : -0.29,
        "Payout Ratio" : 0.162,
        "Performance (Quarter)" : 0.0928,
        "Forward P/E" : 16.11,
        "P/E" : 19.1,
        "200-Day Simple Moving Average" : 0.1062,
        "Shares Outstanding" : 339,
        "Earnings Date" : "2013-11-14T21:30:00Z",
        "52-Week High" : -0.0544,
        "P/Cash" : 7.45,
        "Change" : -0.0148,
        "Analyst Recom" : 1.6,
        "Volatility (Week)" : 0.0177,
        "Country" : "USA",
        "Return on Equity" : 0.182,
        "50-Day Low" : 0.0728,
        "Price" : 50.44,
        "50-Day High" : -0.0544,
        "Return on Investment" : 0.163,
        "Shares Float" : 330.21,
        "Dividend Yield" : 0.0094,
        "EPS growth next 5 years" : 0.0843,
        "Industry" : "Medical Laboratories & Research",
        "Beta" : 1.5,
        "Sales growth quarter over quarter" : -0.041,
        "Operating Margin" : 0.187,
        "EPS (ttm)" : 2.68,
        "PEG" : 2.27,
        "Float Short" : 0.008,
        "52-Week Low" : 0.4378,
        "Average True Range" : 0.86,
        "EPS growth next year" : 0.1194,
        "Sales growth past 5 years" : 0.048,
        "Company" : "Agilent Technologies Inc.",
        "Gap" : 0,
        "Relative Volume" : 0.79,
        "Volatility (Month)" : 0.0168,
        "Market Cap" : 17356.8,
        "Volume" : 1847978,
        "Gross Margin" : 0.512,
        "Short Ratio" : 1.03,
        "Performance (Half Year)" : 0.1439,
        "Relative Strength Index (14)" : 46.51,
        "Insider Ownership" : 0.001,
        "20-Day Simple Moving Average" : -0.0172,
        "Performance (Month)" : 0.0063,
        "P/Free Cash Flow" : 19.63,
        "Institutional Transactions" : -0.0074,
        "Performance (Year)" : 0.4242,
        "LT Debt/Equity" : 0.56,
        "Average Volume" : 2569.36,
        "EPS growth this year" : 0.147,
        "50-Day Simple Moving Average" : -0.0055
  }
  # this variable is used for the menu in this function
  choice = 0
  # This loop is used to provide the menu for this function to allow us which of 
  # the CRUD functions we would like to use
  while choice != 4:
  	# Print the menu and get the user input
    choice = input("\nPlease select an operation:\n1. Create New Document \n2. Update Existing Document\n3. Delete a Document\n4. Previous Menu\n")
    
    # Choice 1 will allow the user to use the create function. We can use the test document or 
    # enter our own document to be inserted. We will remove the option for the test document 
    # if we move this system into production. 
    if choice == 1:
      nextChoice = input("Press '1' to insert the test document or enter the value pairs to be created: ")
      if nextChoice == 1:
        print(testDoc)
        print("Insert result: ")
        print(insertDocument(testDoc))
      else:
        print("Insert result: ")
        print(insertDocument(nextChoice))

    # Choice 2 will allow the user to use the update fuction. We can use the test document or 
    # enter our own values for a Ticker and the Volume. The test document option will be removed 
    # in production we can also add other featues to update other than Volume if needed
    elif choice == 2:
      nextChoice = str(input("Press '1' to update the test document or enter the Ticker you would like to update and the Volume: "))
      if nextChoice == '1':
        rDoc = {"Ticker" : "TEST"}
        uDoc = {"$set" : {"Volume" : 1234567}}
        pprint.pprint(readDocument(rDoc))
        updateDocument(rDoc, uDoc)
        pprint.pprint(readDocument(rDoc))
      else:
        values = nextChoice.split()
        rDoc = {"Ticker" : values[0]}
        pprint.pprint(readDocument(rDoc))
        uDoc = {"$set" : {"Volume" : values[1]}}
        updateDocument(rDoc, uDoc)
        pprint.pprint(readDocument(rDoc))

    # Choice 3 allows the user to use the delete function. For testing we will delete the test document 
    # that we created above but we can also delete a user defined document as well. 
    elif choice == 3:
      nextChoice = input("Press '1' to delete the test document or enter the value pair for the document you would like to delete: ")
      if nextChoice == 1:
        deleteDocument(testDoc)
      else:
        deleteDocument(nextChoice)
    # This statement is just to help make the functionallity a little more user friendly. 
    elif choice > 4 or choice < 1:
      print("Invalid selection please try again\n")

# This function provides the functionallity to manipulate documents as requested. We are able to search 
# by 50-Day Simple Moving average, search by sector, or search by industry. 
def man():
  choice = 0
  while choice != 4:
    choice = int(input("Please select an operation:\n1. Search 50-Day Simple Moving Average\n2. Search by Industry\n3. Search by Sector\n4. Previous Menu\n"))
    if choice == 1:
      low = float(input("Please enter the low value: "))
      high = float(input("Please enter the high value: "))
      search = {"50-Day Simple Moving Average" : {"$gt" : low, "$lt" : high}}
      result = collection.find(search)
      results = str(result.count)
      print('There are', result.count(), 'results within that range.\n')
    elif choice == 2:
      industry = str(input("Please enter an industry: "))
      search = {"Industry" : industry}
      result = list(collection.find(search, projection={"_id" : False, "Ticker" : True}))
      pprint.pprint(result)
    elif choice == 3:
      sector = str(input("Please enter a sector: "))
      search = [{"$match" : {"Sector" : sector}}, {"$group" : {"_id" : "$Industry", "total": {"$sum" : "$Shares Outstanding"}}}]
      pprint.pprint(list(collection.aggregate(search)))                    
    elif choice == 4:
      break
    else:
      print("Invalid selection please try again\n")
  
        
      
if __name__ == '__main__':
  choice = 0
  print("Welcome to the Stock Market API\n Please make your selection")
  while choice != 3:
    choice = int(input("\n1. Manipulate Documents\n2. Retrieve Information\n3. Exit\n"))
    if choice == 1:
      crud()
    elif choice == 2:
      man()
    elif choice == 3:
      break
    else:
      print("Invalid Input please try again\n")
