import sys
import re
import os
import pymongo 
import math
import json

def index_search(query):#when calling from main, change parameters to add testing, then you can call access db functions in this function
	client = pymongo.MongoClient("mongodb+srv://timothyChan:Unrealgamer%5F1@cs121-54zoj.mongodb.net/test?retryWrites=true")#remove when integrating
	db = client['test']#remove when intergrating
	testing = db.testing#remove when integrating
	
	results = testing.find({query.lower():{'$exists': True}}, {'_id': 0})
	return results

#main execution	
quit = "n"
bookkeeping_file = open('.\\webpages\\WEBPAGES_RAW\\bookkeeping.json', encoding = "utf8")
bookkeeping = json.load(bookkeeping_file)
bookkeeping_file.close()

while quit == "n":	
	doc_list = []
	query = input("Enter a search term: ")
	for document in index_search(query):#should only return 1 document in final verson
		for item in document.values():
			for thing in item:
				doc_list.append("0/" + thing) #final version will just be thing
	urls = 0
	for docid in doc_list:
		if urls >19:
			break
		urls += 1 
		print(bookkeeping[docid])#print the urls associated with the docid
	quit = input("Do you want to quit? Enter y or n: ")#keep searching until you are done