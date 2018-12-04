#After some research I learned that using the open object as a iterator is memory
#efficient. The program runs in O(n^2) +O(n) time since it needs to iterate throughe every
#word in the file in order to tokenize and then printing each token

import sys
import re
import os
import pymongo 
from pymongo import MongoClient
import math
from urllib.request import urlopen
from bs4 import BeautifulSoup
import string
import inspect
import nltk


#Read line by line through the file and use regular expressions to split words
#\W splits by non word characters and _ is there for underscpore characters
def tfidf(tf, df, n):
	idf_weight = math.log10((n/df))
	tf_weight = 1 + math.log10(tf)

	return tf_weight * idf_weight

def tokenize(file):
	tokens = {}
	rootDir = file
	k= 0
	for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
		#fileList will be a list of all the files
		fileID = dirName.split("\\")
		i=0
		for item in fileList:
			k +=1
			with open(os.path.dirname(os.path.abspath(inspect.stack()[0][1]))+ dirName[1:] + "\\" + item) as f:
					#iterate through every line in the file
				soup = BeautifulSoup(open(os.path.dirname(os.path.abspath(inspect.stack()[0][1]))+ dirName[1:] + "\\" + item , encoding="utf8"), "html.parser")
				text_tokens = nltk.tokenize.word_tokenize(soup.get_text())
				text_tokens = [t for t in text_tokens if not re.match('[' + string.punctuation + ']+', t)]
				for word in text_tokens:
					if(word.lower() in tokens):
						tokens[word.lower()][0] +=1;
						if (fileID[len(fileID)-1] +"/" + str(i)) not in tokens[word.lower()][1]:
							tokens[word.lower()][1][str(fileID[len(fileID)-1]) +"/"+ str(i)] = 1
						else:
							tokens[word.lower()][1][str(fileID[len(fileID)-1]) +"/"+str(i)] += 1
					else:
						doc_dict = {str(fileID[len(fileID)-1]) +"/"+str(i): 1}
						tokens[word.lower()] = [1, doc_dict]
				
				i +=1
			#if k > 3: #limits first 20 docs for testing, remove when submitting
	for term in tokens:
		for doc_id in tokens[term][1]:
			tokens[term][1][str(doc_id)] = tfidf(tokens[term][1][doc_id], len(tokens[term][1]), k)
	return tokens


#If the file path isn't found print "File not found to console"
try:
	#webpages must be in same directory
			#print(dirName)
			#does the tokenizing
	tokens = tokenize('.\\webpages\\WEBPAGES_RAW')
            #TODO store each tokenized word in a database with the tf-id
    #the lambda key in the sorted method call puts priority in sorting by the
    #most frequent words (highest value) and then alphabetically
	client = pymongo.MongoClient("mongodb+srv://timothyChan:Unrealgamer%5F1@cs121-54zoj.mongodb.net/test?retryWrites=true")
	db = client['NLTK'] 
	
	web = db.Webpages
	
	web.insert_many({term : tokens[term][1]} for term in tokens)
	
except OSError as e:
	print("File not found")
