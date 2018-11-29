import sys
import re
import os
import pymongo 
from pymongo import MongoClient
import math
import json

def index_search(query):#when calling from main, change parameters to add testing, then you can call access db functions in this function
	client = MongoClient("mongodb://localhost:27017")
	db = client['CS121'] 
	testing = db.Webpages
	
	results = testing.find({query.lower():{'$exists': True}}, {'_id': 0})
	return results

#main execution	
quit = "n"
bookkeeping_file = open('.\\webpages\\WEBPAGES_RAW\\bookkeeping.json', encoding = "utf8")
bookkeeping = json.load(bookkeeping_file)
bookkeeping_file.close()
file = open("search.txt", "a")
while quit == "n":	
	doc_list = []
	query = input("Enter a search term: ")
	for document in index_search(query):#should only return 1 document in final verson
		for item in document.values():
			for thing in item:
				doc_list.append(thing) #final version will just be thing
	urls = 0
	file.write(query + "\n")
	for docid in doc_list:
		if urls >19:
			break
		urls += 1 
		file.write(bookkeeping[docid]+"\n")
		print(bookkeeping[docid]+"\n")#print the urls associated with the docid
	quit = input("Do you want to quit? Enter y or n: ")#keep searching until you are done