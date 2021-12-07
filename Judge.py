
# holds data for one debate round
class Round:
	def __init__(self, division, date, aff, neg, vote, result):
		self.division = division
		self.date = date
		self.aff = aff
		self.neg = neg
		self.vote = vote
		self.result = result
	def __str__(self):
		return self.division + '\t' + self.date + '\t' + self.vote + '\t' + self.result


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
