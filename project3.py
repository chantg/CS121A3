#After some research I learned that using the open object as a iterator is memory
#efficient. The program runs in O(n^2) +O(n) time since it needs to iterate throughe every
#word in the file in order to tokenize and then printing each token

import sys
import re
import os
import pymongo 

#Read line by line through the file and use regular expressions to split words
#\W splits by non word characters and _ is there for underscpore characters
def tokenize(file):
	tokens = {}
	with open(file, encoding = "utf8") as f:
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
							tokens[word.lower()] -=1;
						else:
							tokens[word.lower()] = -1;
				print(line)
	return tokens


#If the file path isn't found print "File not found to console"
try:
	#webpages must be in same directory
	rootDir = '.\webpages\WEBPAGES_RAW'
	i = 0;
	tokens = tokenize(".\\webpages\\WEBPAGES_RAW\\0\\103")
	#for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
		#fileList will be a list of all the files
	#	for item in fileList:
	#		print(item)
	#		i +=1
	#		print(dirName)
			#does the tokenizing
	#		tokens = tokenize(dirName + "\\" + item)
            #TODO store each tokenized word in a database with the tf-id
    
    #the lambda key in the sorted method call puts priority in sorting by the
    #most frequent words (highest value) and then alphabetically
	

	#client = pymongo.MongoClient("mongodb+srv://timothyChan:<Unrealgamer%5F1>@cs121-54zoj.mongodb.net/test?retryWrites=true")
	#db = client.test
	for key in sorted(tokens.items(), key = lambda l: (l[1],l[0])):
		print(key[0] + "\t" + str(abs(key[1])))
except OSError as e:
	print("File not found")