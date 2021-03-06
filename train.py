from nltk import TweetTokenizer
import os
from math import log
import math
import re
from nltk import ngrams

#Maps word to [democratCount,republicanCount] list.
word_counts={}

#Function for sorting key words. 
def seperationFunction(d,r,alpha=0.1):
	alpha=0.1
	ratio=2*math.tanh(float(max(d,r))/(d+r))
	logarithm=log(max(d,r))
	logarithm=logarithm**alpha
	return ratio*logarithm
	#return d+r

def is_valid_word(string):
	return (re.search('[a-zA-Z]', string) is not None) and string[0] != '@' and string[0] != '#' and '://' not in string

def process_word(word,isDemocrat):
	global word_counts
	if word not in word_counts:
		if isDemocrat:
			word_counts[word]=[1,0]
		else:
			word_counts[word]=[0,1]
	else:
		if isDemocrat:
			word_counts[word][0]+=1
		else:
			word_counts[word][1]+=1

#PATH = 'convote_v1.1/data_stage_two/training_set/'
def process_all_files(PATH):
	tokenizer = TweetTokenizer()
	print("Processing directory "+PATH)
	for filename in os.listdir(PATH):
		print("Processing "+filename)
		with open(PATH+filename,'r') as file:
			if ".txt" in filename:
				for line in file:
					tokens = tokenizer.tokenize(line.lower())
					trigrams=ngrams(tokens,3)
					for gram in trigrams:
						if is_valid_word(gram[0]) and is_valid_word(gram[1]) and is_valid_word(gram[2]):
							isDemocrat=(filename[-5]=="d")
							process_word(gram,isDemocrat)

def process_file(PATH, isDemocrat):
	print("Processing " + PATH)
	with open(PATH,'r') as file:
		if ".txt" in PATH:
			for line in file:
				tokens = nltk.wordpunct_tokenize(line.lower())
				for word in tokens:
					if word.isalpha():
						process_word(word, isDemocrat)



# process_all_files('convote_v1.1/data_stage_two/training_set/')
# process_all_files('convote_v1.1/data_stage_one/training_set/')
# process_all_files('convote_v1.1/data_stage_one/development_set/')
# process_all_files('convote_v1.1/data_stage_two/development_set/')
# process_all_files('convote_v1.1/data_stage_three/training_set/')
# process_all_files('convote_v1.1/data_stage_three/development_set/')



def plotWords():
	differences=[]
	totalOccurances=[]
	for word in word_counts.keys():
		differences.append(abs(word_counts[word][0]-word_counts[word][1]))
		totalOccurances.append(word_counts[word][0]+word_counts[word][1])

	plt.scatter(differences,totalOccurances)
	plt.show()



def printWords(alpha=0.1):
	# process_all_files('convote_v1.1/data_stage_two/training_set/')
	# process_all_files('convote_v1.1/data_stage_one/training_set/')
	# process_all_files('convote_v1.1/data_stage_one/development_set/')
	# process_all_files('convote_v1.1/data_stage_two/development_set/')
	# process_all_files('convote_v1.1/data_stage_three/training_set/')
	# process_all_files('convote_v1.1/data_stage_three/development_set/')

	# process_all_files("training/texts/issues/abortion/")
	# process_all_files("training/texts/issues/israel/")

	#process_all_files('training/texts/tweets/')
	#process_all_files('training/texts/facebook/')
	process_all_files('training/new_crawl/trainingset/')

	maximumLiberal=0
	maximumCons=0
	for word in word_counts.keys():
		if word_counts[word][0]>maximumLiberal:
			maximumLiberal=word_counts[word][0]
		if word_counts[word][1]>maximumCons:
			maximumCons=word_counts[word][1]

	for word in word_counts.keys():
		word_counts[word][0]=word_counts[word][0]/maximumLiberal*50000
		word_counts[word][1]=word_counts[word][1]/maximumCons*50000


	words=sorted(word_counts.keys(), key=lambda x: seperationFunction(word_counts[x][0],word_counts[x][1]),reverse=True)

	outputfilename="Word_Counts.csv"
	target=open(outputfilename,'w')
	for word in words:
		target.write(word[0]+","+word[1]+","+word[2]+","+","+str(word_counts[word][0])+","+str(word_counts[word][1])+","+str(seperationFunction(word_counts[word][0],word_counts[word][1],alpha)))
		target.write("\n")


printWords()

