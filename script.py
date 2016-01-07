#!/usr/bin/python

import os
import sys

guessedPwd = ""
actualPwd = []
dictionary = ['is','to','of','the']
ctr = [0]*1000

outfile = ""

i = 0
j = 0
k = 0

# Function which uses brute force to find the list of possible passwords
def bruteForce():
	global guessedPwd, actualPwd
	for i in xrange(97,123):
		for j in xrange(97,123):
			for k in xrange(97,123):
				guessedPwd = chr(i)+chr(j)+chr(k)
				testCmd = "openssl enc -d -des-cbc -base64 -k "+guessedPwd+" -in "+outfile+" -out metaFile.txt"
				ret = os.system(testCmd)
				if(ret == 0):
					actualPwd.append(guessedPwd)

# Dictionary Attack
def dictAttack():
	global ctr
	maximum = 0
	ele = 0

	for i in xrange(0,len(actualPwd)):
		testCmd = "openssl enc -d -des-cbc -base64 -k "+actualPwd[i]+" -in "+outfile+" -out metaFile.txt"
		os.system(testCmd)
		fo = open("metaFile.txt","r+")
		temp = fo.read()
		fo.close()
		for j in xrange(0,len(dictionary)):
			temp2 = temp.split(dictionary[j])
			if (len(temp2) > 1):
				value = ctr[i] 
				value = value + len(temp2)
				ctr[i] = value
			elif (len(temp2) == 1):
				value = ctr[i] 
				value = value + 1
				ctr[i] = value

			if ctr[i] > maximum :
				maximum = ctr[i]
				ele = i

	print "Dictionary Scores for each password are below"
	print ctr

	print "The most realistic password =",actualPwd[ele]
	print "When this password is used the infile content is"

	testCmd = "openssl enc -d -des-cbc -base64 -k "+actualPwd[ele]+" -in "+outfile+" -out infile.txt"
	os.system(testCmd)
	
	os.system("cat infile.txt")

def main():
	global actualPwd, outfile

	fileName = raw_input("Enter just the name of the file on which the attack has to be performed\n")
	outfile = fileName+".txt"

	bruteForce()

	#actualPwd = ['afj', 'amb', 'ayf', 'bda', 'ble', 'blr', 'box', 'bro', 'bul', 'buq', 'cea', 'csr', 'csu', 'cwj', 'dwu', 'ezp', 'fof', 'fye', 'gay', 'gbx', 'gqa', 'hrf', 'htt', 'hzb', 'iji', 'ijt', 'jco', 'jng', 'kkp', 'kqr', 'kyj', 'lsh', 'lsp', 'mks', 'mqo', 'myd', 'nik', 'nrn', 'oir', 'opb', 'orl', 'oyf', 'pfx', 'pld', 'prg', 'pzf', 'qlr', 'qnf', 'qpk', 'qsz', 'qwr', 'rdm', 'rec', 'rgr', 'rud', 'rvf', 'sou', 'srs', 'udx', 'vkf', 'vnu', 'wky', 'xbt', 'xmq', 'xps', 'xqw', 'xrw', 'yds', 'ygr', 'yke', 'yni', 'ynz', 'yvl', 'zgh', 'zgx', 'zin', 'zju']

	print "Number of possible passwords =",len(actualPwd)
	print "The possible passwords are"
	print actualPwd

	dictAttack()

	print "The contents are saved in infile.txt."
	os.system("rm -rf metaFile.txt")

main()