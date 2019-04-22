# MongoDB-API
API to interact with a MongoDB database filled with stock information for many companies. 

Running the ```crud.py``` file by its sill will allow you to execute database "Crud" functions in a command line
interacting with a MongoDB database. When combined with the ```api.py``` file you are able to query and update entries in 
the database using CURL statements. You can also generate a stock report by industry or by company type. The ```Stock.json```
file is included to allow you to run this application on your computer. In order for this application to work you must run 
the following command on a computer with MongoDB installed. ``` mongoimport --db market --collection stocks stocks.json```
