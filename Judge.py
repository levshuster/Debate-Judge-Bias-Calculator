
from fractions import Fraction
import datetime


#takes in a intager representing a percentage and resturns a explanation of the fraction
def fraction_to_statment (percentage, left_side = 'thing a', right_side = 'thing b'):
	a, b = str(Fraction(int(percentage), 100)).split('/')
	return 'for every '+a+' '+left_side + ' there are ' + b +' ' + right_side
# print(fraction_to_statment(30, 'people eating', 'people not eating'))

# holds data for one debate round
class Round:
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
	SHOULD_PRINT_LONG = True
	def __init__(self, name = 'no name', paradigm = '''no paradigm''', paradigm_updated='no paradigm', tournaments = list(), rounds = list() ):
		self.name = name
		self.paradigm = paradigm
		self.paradigm_updated = paradigm_updated
		self.tournaments = tournaments
		self.rounds = rounds
	
	def __str__(self):
		result = self.name + '\t' + "paradigm last updated " + self.paradigm_updated
		if self.SHOULD_PRINT_LONG:
			result += '\n\n' +  "--PARADIGM--\n"+self.paradigm +'\n\n'+"--PARTICIPATED AS A JUDGE IN:--\n"
			for i in self.tournaments:
				result += i + '\n'
			
			for i in self.rounds:
				result += str(i)+'\n'
		return result
	def aff_neg_ballot_rate (start_date=None, end_date=None):
		return False