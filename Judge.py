
from fractions import Fraction
import datetime
import pickle

USE_PERCENTAGE = False

#takes in a intager representing a percentage and resturns a explanation of the fraction
def fraction_to_statment (percentage, left_side = 'thing a', right_side = 'thing b'):
	if not USE_PERCENTAGE and percentage%100 != 0:
		a, b = str(Fraction(int(percentage), 100)).split('/')
		return 'for every '+a+' '+left_side + ' there are ' + str(int(b)-int(a)) +' ' + right_side
	return str(left_side)+' '+ str(percentage)+'% of the time\n'+str(right_side)+' '+str(100-int(percentage)) +'% of the time'
# print(fraction_to_statment(30, 'people eating', 'people not eating'))

# holds data for one debate round
class Round:
	aff_cumulative_gender = None
	neg_cumulative_gender = None

	def __init__(self, division, date, aff, neg, vote, result):
		self.division = division
		year, month, day = date.split('-')
		self.date = datetime.date(int(year), int(month), int(day))
		self.aff = aff
		self.neg = neg
		self.vote = vote
		self.result = result
	def __str__(self):
		return self.division + '\t' + str(self.date) + '\t' + self.vote + '\t' + self.result
	


class Judge:
	SHOULD_PRINT_LONG = False

	def __init__(self, name = 'no name', paradigm = '''no paradigm''', paradigm_updated='no paradigm', tournaments = list(), rounds = list() ):
		self.name = name
		self.paradigm = paradigm
		self.paradigm_updated = paradigm_updated
		self.tournaments = tournaments
		self.rounds = rounds
	
	def align_with_panal_percentage(self, start_date=None, end_date=None):
		decision_aligns_with_majority = 0
		panel_participation = 0
		for i in self.rounds:
			if start_date == None or start_date <= i.date:
				if end_date == None or end_date >= i.date:
					if i.result: 
						panel_participation += 1
						if i.result.split()[0] == i.vote:
							decision_aligns_with_majority += 1
		return decision_aligns_with_majority/panel_participation*100



	def aff_ballot_percentage(self, start_date=None, end_date=None):
		aff_counter = 0
		for i in self.rounds:
			if start_date == None or start_date <= i.date:
				if end_date == None or end_date >= i.date:
					if str(i.vote) == 'Aff':
						aff_counter=1 + aff_counter
					# elif str(i.vote) != 'Neg':
						# print("Each round must end with a Aff or Neg ballot, this ballot got a "+i.vote+" ballot")
		return int(aff_counter/len(self.rounds)*100)

	def __str__(self):
		result = self.name + '\t' + "paradigm last updated " + self.paradigm_updated
		result += '\nAFFERMATIVE BIAS?   '+fraction_to_statment(self.aff_ballot_percentage(), 'affirmative votes', 'negitive votes')
		result += '\nTENDENCY TO AGREE WITH MAJORITY   '+fraction_to_statment(self.align_with_panal_percentage(), 'agree with majority of panal', 'desenting vote in a judging panel')
		if self.SHOULD_PRINT_LONG:
			result += '\n\n' +  "--PARADIGM--\n"+self.paradigm +'\n\n'+"--PARTICIPATED AS A JUDGE IN:--\n"
			for i in self.tournaments:
				result += i + '\n'
			
			for i in self.rounds:
				result += str(i)+'\n'
		return result

#reference from https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
def save (judge):
	with open(judge.name+'.bias', 'wb') as judge_file:pickle.dump(judge, judge_file)
def load (judge_file_name):
	with open(judge_file_name, 'rb') as judge_file:return pickle.load(judge_file)
