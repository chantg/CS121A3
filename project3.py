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
	rootDir = file#
	i = 0;#

	for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
		#fileList will be a list of all the files
		for item in fileList:
#			print(item)

			with open(dirName + "\\" + item, encoding = "utf8") as f:
					#iterate through every line in the file
					
					for line in f:
						
						words = re.split(r"[\W_]+", line)
					#iterate through every word on the line
						for word in words:
							if(word != ""):
								#if it exists decrement the pointer. It was easier to sort
								#the words with negative values as after a sort on their values
								#the keys are in alphabetical order
								if(word.lower() in tokens):
									tokens[word.lower()][0] -=1;
									if i not in tokens[word.lower()][1]:
										tokens[word.lower()][1][i] = 1
									else:
										tokens[word.lower()][1][i] += 1
								else:
									doc_dict = {i: 1}
									tokens[word.lower()] = [-1, doc_dict]
			i +=1						
			if i > 20:#limits first 20 docs for testing, remove when submitting
				for term in tokens:
					for doc_id in tokens[term][1]:
						tokens[term][1][doc_id] = tfidf(tokens[term][1][doc_id], len(tokens[term][1]), i-1)
				
				return tokens#print(line)
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

	client = pymongo.MongoClient("mongodb+srv://timothyChan:<Unrealgamer%5F1>@cs121-54zoj.mongodb.net/test?retryWrites=true")
	db = client.test
	sorted_tokens = sorted(tokens.items(), key = lambda l: (l[1][0],l[0]))
	for x in range(len(sorted_tokens)):
			sorted_tokens[x] = [sorted_tokens[x][0], sorted_tokens[x][1][0], sorted_tokens[x][1][1]]
	for key in sorted_tokens:
			print(key[0] + "\t" + str(abs(key[1])) + "\t" + str(key[2]))
except OSError as e:
	print("File not found")
