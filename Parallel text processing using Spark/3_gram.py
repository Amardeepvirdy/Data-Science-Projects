
import sys
import csv
import re
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("myapp")
sc = SparkContext(conf=conf)

text_file = sc.textFile("input")

mydict = {}
reader = csv.reader(open('new_lemmatizer.csv'), delimiter = ',')
i = 0
for row in reader:
	key = row[0]
	if key in mydict:
		pass
	mydict[key] = filter(None, row[1:])

def mapper_stub(word1, word2, word3):
	word1 = " ".join(re.findall("[a-zA-Z]+", word1))
	word1 = word1.replace("j", "i")
	word1 = word1.replace("v", "u")
	word2 = " ".join(re.findall("[a-zA-Z]+", word2))
	word2 = word2.replace("j", "i")
	word2 = word2.replace("v", "u")
	word3 = " ".join(re.findall("[a-zA-Z]+", word3))
	word3 = word3.replace("j", "i")
	word3 = word3.replace("v", "u")
	if word1 in mydict:
		if mydict[word1] != "":
			word1 = mydict[word1]
	else:
		word1 = [word1]
	if word2 in mydict:
		if mydict[word2] != "":
			word2 = mydict[word2]
	else:
		word2 = [word2]
	if word3 in mydict:
		if mydict[word3] != "":
			word3 = mydict[word3]
	else:
		word3 = [word3]
	return word1, word2, word3
	
def mapper(line):
	try:
		line = str(unicode(line))
	except:
		line = line
	line = line.strip()
	mylist = []
	if(len(line.split(">")) <= 1):
		return [((('random', 'random', 'random'), ['random']))]
	location, words = line.split(">")
	location = location + ">"
	words = words.split()
	for i in range(0, len(words)):
		for j in range(i+1, len(words)):
			for k in range(j+1, len(words)):
				pair1, pair2, pair3 = mapper_stub(words[i], words[j], words[k])
				for val1 in pair1:
					for val2 in pair2:
						for val3 in pair3:
							mylist.append(((val1, val2, val3), [location]))
	if mylist:
		return mylist
	return [(('random', 'random', 'random'), ['random'])]
	
		
counts = text_file.flatMap(mapper).sortByKey().reduceByKey(lambda a, b: a+b)
counts.saveAsTextFile("output3")
