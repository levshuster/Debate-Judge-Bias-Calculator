
from fractions import Fraction # used to beatify the results of the output of analysis
import datetime # used to store the date when the paradigm was last ubdated
import pickle # used to save and load judges

import Gender # used to acsess the api to determin the gender of a first name and caculate the round score
from Gender import vote_for_more_woman

# In CLI this will be an optional flag but for now if you want the results in clear spoken fractions set to true if you want the results in fractions use False
# EX of USE_PERCENTAGE = True 	--> "Ballots for woman 33% of the time \n ballots for men 67% of the time"
# EX of USE_PERCENTAGE = False 	--> "for every 33 Ballots for woman there are 67 ballots for men"
USE_PERCENTAGE = True


#takes in a integer representing a percentage and resturns a explanation of the fraction
def fraction_to_statment (percentage, left_side = 'thing a', right_side = 'thing b'):
	if not USE_PERCENTAGE and percentage%100 != 0:
		a, b = str(Fraction(int(percentage), 100)).split('/')
		return 'for every '+a+' '+left_side + ' there are ' + str(int(b)-int(a)) +' ' + right_side
	return str(left_side)+' '+ str(percentage)+'% of the time\n'+str(right_side)+' '+str(100-int(percentage)) +'% of the time'


# object to hold the inforamtion corrisponding to one debate round
class Round:
	def __init__(self, division, date, aff, neg, vote, result):
		self.division = division
		year, month, day = date.split('-')
		self.date = datetime.date(int(year), int(month), int(day))
		self.aff = aff
		self.neg = neg
		self.vote = vote
		self.result = result

		#MM vs MM and FF vs FF and F? vs MM... are thrown out
		#if FF win over FM then +.5	if MM win over FM then -.5
		#if FF win over MM then +1	if MM win over FF then -1

		# caculates the round score (see How do you Quantify Discrimination? section in readme file)
		try:
			self.vote_for_more_woman = Gender.vote_for_more_woman(aff, neg, vote)
			# if sucsessfully caculate round score set to zero (set to 1 if one of the gender api calls returns a results witha low certinty)
			self.failed_to_find_gender = 0

		except:
			self.vote_for_more_woman = 0
			self.failed_to_find_gender = 1
	def __str__(self):
		return str(self.division) + '\t' + str(self.date) + '\t' + str(self.vote) + '\t' + str(self.result) + '\t' + str(self.vote_for_more_woman)
	


class Judge:
	# in the CLI this will be a flag but for now determins how much information should be printed for debugging purposes
	SHOULD_PRINT_LONG = False

	def __init__(self, name = 'no name', paradigm = '''no paradigm''', paradigm_updated='no paradigm', tournaments = list(), rounds = list(), recorded_rounds = 0 ):
		self.name = name
		self.paradigm = paradigm
		self.paradigm_updated = paradigm_updated
		self.tournaments = tournaments
		self.rounds = rounds
		self.recorded_rounds = recorded_rounds
		self.failed_to_find_gender = 0

		# counts the number of times that the api call was able to confidantly retrun the gender for all the debaters first names
		for i in rounds:
			self.failed_to_find_gender += i.failed_to_find_gender
	
	# for finals and elimation rounds, more than one judge is assigned to preside over a single round
	# this function determins how often a judge agrees with the majority
	# if the judge often disagrees with the majority there is evidence that they are a contrarian, super progressive, supper lay, or otherwise unusual
	def align_with_panal_percentage(self, start_date=None, end_date=None):
		decision_aligns_with_majority = 0
		panel_participation = 0
		for i in self.rounds:

			# allows for CLI to specific an interval inwhich to caculate
			# say a judge has been judging for 6 years in the first years they were a lay judge and as such often disagreed with the majority
			# if they have since became a normal judge and now normally agree with the majority this allows the user to filter out the judges early record
			if start_date == None or start_date <= i.date:
				if end_date == None or end_date >= i.date:

					if i.result: 
						panel_participation += 1
						if i.vote in i.result.split()[0] or i.vote in i.result:
							decision_aligns_with_majority += 1
		# if the judge has never been on a panel return result that signals they have never disagreed with a panel
		if panel_participation == 0:
			return 100
		
		# return percentage * 100 so it is easier to print
		else:
			return decision_aligns_with_majority/panel_participation*100

	# this generates the percentage of ballots given to men vs given to woman
	def winning_gender_bias(self, start_date=None, end_date=None):
		woman_win_counter = 0
		man_win_counter = 0
		for i in self.rounds:
			if start_date == None or start_date <= i.date:
				if end_date == None or end_date >= i.date:
					if self.SHOULD_PRINT_LONG:print(i)
					if i.vote_for_more_woman >0:
						woman_win_counter += i.vote_for_more_woman
					elif i.vote_for_more_woman <0:
						man_win_counter -= i.vote_for_more_woman
		if woman_win_counter == 0 and man_win_counter == 0:
			print("\n\n**For the upcoming Judge, Woman win persentage is likely in error because incomplete data was scraped, make sure you have not surpased you 1000 api call limit**")
			woman_win_counter = 1
			man_win_counter = 1

		# create a table so both a boolean to show which side won more often and the percentage can be returned
		rslts = {'woman_win_percentage':int(woman_win_counter/(woman_win_counter+man_win_counter)*100), 'number_of_ballots_diffrence':abs(woman_win_counter-man_win_counter)}
		if (man_win_counter>woman_win_counter):
			rslts['male_bias']=True
		else:			
			rslts['male_bias']=False
		return rslts

	# to determin if there is a consitant bias towards the affermative or the negative 
	def aff_ballot_percentage(self, start_date=None, end_date=None):
		aff_counter = 0
		neg_counter = 0
		for i in self.rounds:
			print('round triggered')

			# allows for CLI to specific an interval inwhich to caculate
			# say a judge has been judging for 6 years in the first years they were a lay judge and as such often prefered the affermative (as lay juges are liable to do)
			# similarly if this years topic has sertain types of judges biased towards one side you can filter by just the time since this has been the topic at tournaments
			if start_date == None or start_date <= i.date:
				if end_date == None or end_date >= i.date:

					print('get through date with: ', str(i.vote))
					if 'Aff' in str(i.vote) or 'Pro' in str(i.vote):
						print('aff vote triggered')
						aff_counter=1 + aff_counter
					elif str(i.vote) == 'Neg' or str(i.vote) == 'Con':
						neg_counter=1 + neg_counter

		return int(aff_counter/(aff_counter+neg_counter)*100)

	# when a specific caculation is not called for and one wants to get a general idea of the data they simply print the judge object
	def __str__(self):
		result = '\n\n\n'+self.name
		result += '\nAFFERMATIVE BIAS?\n'+fraction_to_statment(self.aff_ballot_percentage(), 'affirmative votes', 'negitive votes')
		result += '\n\nTENDENCY TO AGREE WITH MAJORITY\n'+fraction_to_statment(self.align_with_panal_percentage(), 'ballots who agree with majority of the panal', 'ballots who disagree with the majority of the judging panel')
		
		gender_bias_results = self.winning_gender_bias()
		result += '\n\nGENDER BIAS?\n'+fraction_to_statment(gender_bias_results['woman_win_percentage'], 'Ballots for woman', 'ballots for men')
		result += '\nthat bias rating is the result of an aditional ' + str(int(gender_bias_results['number_of_ballots_diffrence']))+" ballots out of "+ str(len(self.rounds)-self.failed_to_find_gender)

		if self.SHOULD_PRINT_LONG:
			result += '\n\n' + "paradigm last updated " + self.paradigm_updated +  "\n\n\nPARADIGM"+self.paradigm +'\n\n'+"PARTICIPATED AS A JUDGE IN:\n"
			for i in self.tournaments:
				result += i + '\n'
			
			# for i in self.rounds:
			# 	result += str(i)+'\n'
		return result

# uses pickle to save and load Judge objects as .bias files
# reference from https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
def save (judge):
	with open(judge.name+'.bias', 'wb') as judge_file:pickle.dump(judge, judge_file)
def load (judge_file_name):
	with open(judge_file_name, 'rb') as judge_file:return pickle.load(judge_file)
