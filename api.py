#!/usr/bin/python
import json
import bottle
import crud
import pprint
from bson import json_util
from bottle import route, run, request, abort, post
from pymongo import MongoClient

# setup connection to mongo database
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

# set URI path for the create function of the REST server
# this function takes the POST message from the client to create
# a new document in the stock collection of the market database
@post('/stocks/api/v1.0/createStock', method='POST')
def post_create():
  try:
    result = request.json
    crud.insertDocument(result)
    return "\nDocument Successfully Created\n"
  except Exception as e:
    status = 500
    return repr(e)

# set URI path for the read function of the REST server
# this function takes a Ticker as an argument and calls the 
# read function from the other document I created and returns the 
# found document 
@route('/stocks/api/v1.0/readStock/<ticker>', method='GET')
def get_read(ticker):
  try: 
    document = {"Ticker" : ticker}
    read = crud.readDocument(document)
  except Exception as e:
       abort(404, str(e))
  return json.dumps(read, indent=4, default=json_util.default)

# set URI path for the update function of the REST server
# this function takes a Ticker and a Company as arguments. The Ticker
# is the search criteria and the Company is the value to be updated
@route('/stocks/api/v1.0/updateStock/<Ticker>/<Company>', method='GET')
def get_update(Ticker, Company):
  try:
    updateID = {"Ticker" : Ticker}
    updateVal = {"$set" : {"Company" : Company}}
    crud.updateDocument(updateID, updateVal)
    result = crud.readDocument(updateID)
  except Exception as e:
    abort(404, str(e))
  return json.dumps(result, indent=4, default=json_util.default)

# set the URI path for the delete function of the REST server
# this function takes a Ticker as an argument it is used as a 
# search criteria and then deletes the document if it is deleted
# it will return a statement that the document has been deleted.
@route('/stocks/api/v1.0/deleteStock/<Ticker>', method='GET')
def get_delete(Ticker):
  try:
    document = {"Ticker" : Ticker}
    result = crud.deleteDocument(document)
  except Exception as e:
    abort(404, str(e))
  return "\nDocument Deleted\n"

# set the URI path for the stock report function for the REST server 
# this function takes a string of tickers seperated by commas and 
# returns the stocks for those tickers. 
@route('/stocks/api/v1.0/stockReport/<ticker>', method='GET')
def get_stockReport(ticker):
  Tickers = ticker.split(',')
  print(Tickers)
  results = []
  for ticker in Tickers:
    document = {"Ticker" : ticker}
    read = crud.readDocument(document)
    results.append(read)
  return json.dumps(results, indent=4, default=json_util.default)

# set the URI path for the industry report for the REST server
# this function takes the industry as an argument and returns the top 5 
# companies in that industry.
@route('/stocks/api/v1.0/industryReport/<industry>')
def get_industryReport(industry):
  try: 
    read = list(collection.aggregate([{"$match" : {"Industry" : industry}}, {"$sort" : {"Profit Margin" : 1}}, {"$limit" : 5}]))
  except Exception as e:
       abort(404, str(e))
  return json.dumps(read, indent=4, default=json_util.default)

# start the server listening for connections 
if __name__ == '__main__':
  run(host='localhost', port=8080)
