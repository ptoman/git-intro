"""
Support file for twqs, the twenty questions
toy application for git practice.  

This code performs file reading.
"""

import sys
import os

DATA_FOLDER = "data"

def load_answers():
	answerFiles = [f for f in os.listdir(os.getcwd() + "//" + DATA_FOLDER) if f.startswith('twqsanswers') and f.endswith(".csv")]

	possibleAnswers = []
	answersToQuestions = {}
	for filename in answerFiles:
		with open(os.getcwd() + "//" + DATA_FOLDER + "//" + filename, 'r') as answerfile:
			for line in answerfile:
				answerList = line.strip().split(",")
				# TODO: Check that we aren't getting multiple instances of the same item label (e.g., "cat" and "cat")
				label = answerList[0]
				possibleAnswers.append([1, label])
				for item in answerList[1:]:
					[id, val] = item.split(":")
					if val != "n" and val != "y":
						# TODO: Turn me into smart error handling
						sys.exit("Error in data! Values may only be 'n' or 'y'.")
					# TODO: Check that we aren't getting multiple conflicting answers for the same item
					if id not in answersToQuestions:
						answersToQuestions[id] = [];
					answersToQuestions[id].append([val, label])
	
	return answersToQuestions, possibleAnswers

def load_questions():
	questionFiles = [f for f in os.listdir(os.getcwd() + "//" + DATA_FOLDER) if f.startswith('twqsquestions') and f.endswith(".csv")]
	
	possibleQuestions = []
	for filename in questionFiles:
		with open(os.getcwd() + "//" + DATA_FOLDER + "//" + filename, 'r') as qfile:
			for line in qfile:
				questionline = line.strip().split(",")
				id = questionline[0]
				question_text = questionline[1]
				if id in possibleQuestions:
					# TODO: Turn me into smart error handling
					sys.exit("Error in data! Multiple questions have the same ID (" + str(id) + ").")
				possibleQuestions.append([0, id, question_text])
	
	return possibleQuestions
	
def load_data():
	#TODO: Refactor to ensure that...
	# -- every question id in the answerlist corresponds to a known question
	# -- there is an item in answersToQuestions for every known question
	map, a = load_answers()
	q = load_questions()
	return map, a, q