import sys
import re
import os
import pymongo 
from pymongo import MongoClient
import math
import json
from tkinter import *

def index_search(query):#when calling from main, change parameters to add testing, then you can call access db functions in this function
	client = MongoClient("mongodb+srv://timothyChan:Unrealgamer%5F1@cs121-54zoj.mongodb.net/test?retryWrites=true")
	db = client['CS121'] 
	testing = db.Webpages
	
	results = []
	for query_term in query.lower().split():#support for multiple term queries
		results.append(testing.find({query_term:{'$exists': True}}, {'_id': 0}))
	return results#returns a cursor object that must be parsed for the data
   	
	
def search(top, bookkeeping):
	input = E1.get()
	print("Searched")
	print(input)
	temp = ""
	first_pass = True
	doc_dict = {}
	doc_dict2 = {}

	for term in index_search(input): #we have a result for each term in the query
		for postings_list in term:#dive deeper into the cursor object to get the info we need
			for item in postings_list.values(): #item is a {docid: tf-idf} dictionary
				if (first_pass == True): #first pass add all documents to the final results
					doc_dict = item.copy()
					first_pass = False
				else:#only include documents that have both terms
					for id in item:
						if id in doc_dict:
							doc_dict2[id] = doc_dict[id] + item[id]#add tf-idf from both documents in order to rank most relevat documents first
					doc_dict.clear()
					doc_dict = doc_dict2.copy()
					doc_dict2.clear()
					
	urls = 0
	for docid in sorted(doc_dict, key=doc_dict.get, reverse=True): #rank higher tf-idf document urls first
		if urls >19:
			break
		if docid in bookkeeping: #retreive the url from the bookkeeping file
			urls += 1 
			temp += bookkeeping[docid] + "\n"
		#print(bookkeeping[docid]+"\n")#print the urls associated with the docid		
	text = Text(top)
	text.insert(INSERT, temp)
	text.grid(row = 3, column = 0)

#main execution	
quit = "n"
bookkeeping_file = open('.\\webpages\\WEBPAGES_RAW\\bookkeeping.json', encoding = "utf8")
bookkeeping = json.load(bookkeeping_file)
bookkeeping_file.close()

top = Tk()

top.title("Search")

L1 = Label(top, text = "Search Entry")
L1.grid(row = 0, column = 0)
E1 = Entry(top, bd =5)
E1.grid(row = 0, column = 1)

B = Button(top, text ="Search", command = lambda: search(top,bookkeeping))

B.grid(row = 1, column = 1)

top.mainloop()