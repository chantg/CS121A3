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
	
	results = testing.find({query.lower():{'$exists': True}}, {'_id': 0})
	return results
   	
	
def search(top, bookkeeping):
	input = E1.get()
	print("Searched")
	print(input)
	temp = ""
	doc_list = []
	for document in index_search(input):#should only return 1 document in final verson
		for item in document.values():
			for thing in item:
				doc_list.append(thing) #final version will just be thing
	urls = 0
	for docid in doc_list:
		if urls >19:
			break
		urls += 1 
		temp += bookkeeping[docid] + "\n"
		print(bookkeeping[docid]+"\n")#print the urls associated with the docid		
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