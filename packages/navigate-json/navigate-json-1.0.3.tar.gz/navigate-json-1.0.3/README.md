# json_navigator




## Usage

from navJson import jsonParsing

### If the object you want to inspect is Python list, use the method below

If jsonToBeParsed is the variable name - 

returnedCollectionOfCodes, _ = jsonParsing.listParserAndCodeCreator( jsonToBeParsed, 
																				  rootCode = "jsonToBeParsed", 
																				  collectionOfCodes = list() )


resultList = [  (code , eval(code) ) for code in returnedCollectionOfCodes   ]


### If it is a python dictionary, use below method

returnedCollectionOfCodes, _ = jsonParsing.jsonParserAndCodeCreator( jsonToBeParsed, rootCode = "jsonToBeParsed", collectionOfCodes = list() )


resultList = [  (code , eval(code) ) for code in returnedCollectionOfCodes   ]








