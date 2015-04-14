"""
Toy implementation of a twenty questions game.
Designed for learning git, so was put together quickly
and deliberately contains many marked TODOs of varying
difficulty to fit the audience's desires/capabilities.

Usage (on command line):
	python twqs.py
"""

import sys
import twqs_data

def choose_best_question(possibleQuestions, answersToQuestions):
	""""Pulls the question from the top of priority queue
	and returns it, removing it from the list of 
	possible questions."""
	possibleQuestions.sort(key=lambda q: q[0], reverse=True) 
	
	question_to_ask = [0,'','']
	while question_to_ask[1] not in answersToQuestions and len(possibleQuestions) > 0:
		question_to_ask = possibleQuestions.pop()
	
	if len(possibleQuestions) == 0:
		return False
	else:
		return question_to_ask

def get_user_input(qnum, question):
	"""Request a yes/no answer from the user and validates its receipt."""
	answer = ''
	while answer != "y" and answer != "n":
		answer = raw_input(str(qnum) + ") " + question[2] + " (y/n) >> ") 
		"Come on, this is a game!" """"Gives user feedback that they're not giving valid answers"""

	return answer

def update_answer_likelihoods(question, userYn, answersToQuestions, possibleAnswers):
	"""Removes any answers that are impossible and updates the 
	likelihoods of the remainder."""
	# TODO: Don't remove impossible answers -- just decrement their likelihood (in case
	#       the data is wrong or misleading -- quite possible)
	# TODO: Update to use probabilistic/Bayesian updating rather than points-based updating
	# TODO: Refactor to use more efficient data structures
	# TODO: Improve documentation
	qId = question[1]
	assert qId in answersToQuestions
	for locOfAnswer, [_, lhsJoinLabel] in enumerate(possibleAnswers):
		for rightYn, rhsJoinLabel in answersToQuestions[qId]:
			# If good, increment the points
			if lhsJoinLabel == rhsJoinLabel and rightYn == userYn:
				possibleAnswers[locOfAnswer][0] += 1
			# If no good, remove from the possible answers and update the 
			# list of possible answers to questions
			if lhsJoinLabel == rhsJoinLabel and rightYn != userYn:
				possibleAnswers.pop(locOfAnswer)
				for q in answersToQuestions:
					for ans,lab in answersToQuestions[q]:
						if lhsJoinLabel == lab:
							answersToQuestions[q].remove([ans,lab])
							
def update_question_priorities(answersToQuestions, possibleQuestions):
	# TODO: Reimplement to be more efficient
	mapQuestionToGoodness = {}
	for q in answersToQuestions:
		listForQ = answersToQuestions[q]
		numYes = 0
		numNo = 0
		for yn,_ in listForQ:
			if yn == 'y':
				numYes += 1
			elif yn == 'n':
				numNo += 1
			else:
				# TODO: Turn me into smart error handling
				sys.exit("Corrupted data! Values may only be 'n' or 'y'.")
		if numYes + numNo > 0:
			mapQuestionToGoodness[q] = abs(numYes - numNo)/len(listForQ)
	
	for qItem in possibleQuestions:
		id = qItem[1]
		if id in mapQuestionToGoodness:
			qItem[0] = mapQuestionToGoodness[id]
		else:
			qItem[0] = float("inf")
		
def get_guess(possibleAnswers):
	# TODO: Improve documentation
	if len(possibleAnswers) > 0:
		possibleAnswers.sort(key=lambda q: q[0]) 
		return possibleAnswers.pop()
	else:
		return False
	
def run_game():
	# TODO: Improve documentation
	print "Would you like to play a game?"
	answersToQuestions, possibleAnswers, possibleQuestions = twqs_data.load_data()
	update_question_priorities(answersToQuestions, possibleQuestions)
	
	# TODO: Ensure we actually have 20 questions (not an off-by-one bug)
	# RESOLVED: Ended range with 21 instead of 20 - DH 2015-04-13
	for qnum in range(1,21):
		question = choose_best_question(possibleQuestions, answersToQuestions)
		if len(possibleAnswers) > 1:
			if question:
				answer = get_user_input(qnum, question)
				update_answer_likelihoods(question, answer, answersToQuestions, possibleAnswers)
				update_question_priorities(answersToQuestions, possibleQuestions)
			else:
				print "You've exhausted me. I have no clue as to what more to ask. You win."
				break
	
	guess = get_guess(possibleAnswers)
	if guess:
		print "Is it " + guess[1] + "?"
	else:
		print "I have no idea. Guessing games are hard. You win."

		
run_game()

# TODOs: Nice-to-haves that could also be added in...
# -- Ability to learn new objects based on the answers given
# -- Flag for --debug mode that prints the sorted likelihoods of each question
#    and answer after each interaction
# -- Ability to start a new game without restarting the application (wrapper script)
# -- Additional script that adds ability to fill out more fields for the objects
#    that aren't complete (could augment to be smart script that feeds the objects & 
#    the questions in the most useful order)
# -- Refactor so scopes are limited, there is a clearer main, etc. (best practices)
# -- Anything else you can think of
