#After some research I learned that using the open object as a iterator is memory
#efficient. The program runs in O(n^2) +O(n) time since it needs to iterate throughe every
#word in the file in order to tokenize and then printing each token

import sys
import re
import os
import pymongo 
import math

#Read line by line through the file and use regular expressions to split words
#\W splits by non word characters and _ is there for underscpore characters
def tfidf(tf, df, n):
	tf_weight = 1 + math.log10(tf)
	idf_weight = math.log10((n/df))

	return tf_weight * idf_weight

def tokenize(file):
	tokens = {}
	rootDir = file
	i = 0;#
	
	for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
		#fileList will be a list of all the files
		temp = dirName.split("\\")
		print(temp[len(temp)-1])
		#for item in fileList:
			
				
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
	#db = client['test'] 
	
	#testing = db.testing
	
	#for term in tokens:
	#	testing.insert_one({term : tokens[term][1]})
	
except OSError as e:
	print("File not found")
