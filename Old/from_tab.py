# used to scrape the dynamic portions of the website tabroom.com 
import os
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
ser = Service("/Users/levshuster/Desktop/Learning/Debate-Judge-Bias-Calculator/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

import Judge # handles the loading, analyzing and saving of judge objects

import concurrent.futures #handles paralelzation of the API calls and website scrapes to make the program roughly twenty times faster

import urllib.request #used to scrape static portions of the website tabroom.com

'''
from_tab.py scrapps tabroom to get a list of all the rounds a judge has prosided over, 
another part of this file scrapes all the names of competitors in each round
'''


'''Example table that the table object turns to a list of rounds
Tournament					Lv	Date		Ev	Rd	Aff		Neg			Vote
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	Octas	Eastview PS	Minnehaha OS		Aff
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	R5	Eastview PV	Century LZ		Neg
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	R4	Orono CM	Southwest SM		Neg
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	R3	Eastview SS	Mounds Park FL		Aff
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	R2	Mayo KV		Stillwater Area BM	Aff
Minnesota Classic State Debate Tournament	HS	12/3/2021	JV	R1	Southwest KM	Eastview CM		Neg
MN Classic Debate Tournament 3 Oct 16		HS	10/16/2021	JV	R3	Mounds Park AMB	Eastview SR		Neg
MN Classic Debate Tournament 3 Oct 16		HS	10/16/2021	JV	R2	Century WW	Mounds Park WN		Aff
'''

# Because the webscrapper reads down each column of a table before starting the next column to get a list of rounds inwhich each round is one row a table object is used
# To make a round, Judge.Round (scrapes the webpage that belongs to each individual debate round) is called which is why it makes sense to implement multithreading here
class Table:
	# takes each column of the judges record table as a list (see above for example)
	def __init__(self, division = list(), date = list(), aff=list(), neg = list(), vote = list(), result = list() ):
		self.division = division
		self.date = date
		self.aff = aff
		self.neg = neg
		self.vote = vote
		self.result = result
	
	# takes a counter which represents the row number and assembles all the data from all the columns and feeds it into Judge.Round to create a [debate] round object
	def make_round(self, counter):
		print('aff is', self.aff[counter])
		print(self.division[counter], self.date[counter], self.aff[counter], self.neg[counter], self.vote[counter], self.result[counter])
		return Judge.Round(self.division[counter], self.date[counter], self.aff[counter], self.neg[counter], self.vote[counter], self.result[counter])

	# runs make_round on every row
	def single_thread_to_round_list(self):
		rounds = list()
		for i in range(len(self.division)):
			print('starting round', i)
			rounds.append(self.make_round(i))
		return rounds
	
	# runs make_round on every row concurrently
	def to_round_list(self):
		rounds_proceses = list() #holds all the rounds currently being processed
		rounds = list() #holds the result of Judge.Rounds

		with concurrent.futures.ThreadPoolExecutor() as executor:
			for i in range(len(self.division)):
				try:
					rounds_proceses.append(executor.submit(self.make_round, i))
					print("starting round", i ,'out of', len(self.division))
				except:
					print("a team name thread couldn't be started")

		for i in rounds_proceses:
			print("finishing round", rounds_proceses.index(i) ,'out of', len(rounds_proceses))
			try:
				rounds.append(i.result())
			except Exception as e: 
				print(e)
				print("a team name result couldn't be found")
		return rounds



'''example of the type of file process_section handles
--Name--
Lev2 Shuster2

--Paradigm--
Paradigm Here
and also here

--Date of Paradigm Update--
9 November 2019 5:23 AM PST

--Rounds--
# Tournament, Level, Date, Level, Round, Aff Debater 1 is female, Aff Debater 2 is female, Neg Debater 1 is female, Neg Debater 2 is female, Vote
'''

''' but process_section is given one chunk at a time like
Header = "Paradigm"
lines = {"Paradigm Here", "and also here"}
'''
#Handles Test files
# decides how to process contents of a given section
# the lines list contain each line of the test file that belongs to the given section  
def process_section(header, lines):
	print('started ', header)

	if header == 'Name':
		big_line = ''
		for line in lines:
			big_line += line +' '
		return {'name':big_line.strip()}	
	
	if header == 'Paradigm':
		big_line = ''
		for line in lines:
			big_line += line +'\n'
		return {'paradigm':big_line}
	
	if header == 'Date of Paradigm Update':
		big_line = ''
		for line in lines:
			big_line += line +' '
		return {'date':big_line}
	
	if header == 'Rounds':
		print("rounds found")
		print(lines, len(lines))

		# create a table object
		table = Table()
		for round in lines:
			print('lentgh of the round is ', len(round))
			print("round is", round)
			if len(round) > 1:
				print('triggered one')
				print(round)
				round_elements = round.split(',')
				table.division.append(round_elements[1])
		for round in lines:
			if len(round) > 1:
				print('triggered two')
				round_elements = round.split(',')
				table.date.append(round_elements[2])
		
		# TODO add round and division ('jv' and R4)
		
		for round in lines:
			if len(round) > 1:
				round_elements = round.split(', ')

				aff_one = round_elements[6].split('-')
				first_gender = aff_one[0] 
				first_probability = float(aff_one[1])
				first_cases = int(aff_one[2])
				first_debater = [first_gender, first_probability, first_cases]

				aff_two = round_elements[6].split('-')
				two_gender = aff_two[0] 
				two_probability = float(aff_two[1])
				two_cases = int(aff_two[2])
				two_debater = [two_gender, two_probability, two_cases]

				table.aff.append([first_debater, two_debater])
		for round in lines:
			if len(round) > 1:
				round_elements = round.split(', ')

				neg_one = round_elements[7].split('-')
				first_gender = neg_one[0] 
				first_probability = float(neg_one[1])
				first_cases = int(neg_one[2])
				first_debater = [first_gender, first_probability, first_cases]

				neg_two = round_elements[8].split('-')
				two_gender = neg_two[0] 
				two_probability = float(neg_two[1])
				two_cases = int(neg_two[2])
				two_debater = [two_gender, two_probability, two_cases]

				table.neg.append([first_debater, two_debater])
		for round in lines:
			if len(round) > 1:
				round_elements = round.split(',')
				table.vote.append(round_elements[9])

				# must add way to simulate panel decision
				table.result.append(None)

		return {'table':table}
	else:
		return {}



def test_file_to_dict(file_name):
	#TODO add try case file could not be found
	print("started files to dict")


	test_case_file = open(file_name, "r")
	header = ''
	lines = list()
	dictonary = {'test':True}
	for line in test_case_file:
		# print(line)
		if '#' != line[0:1]: # if the testJudge.bias file doesn't start with a comment symbol...
			if '--' == line[0:2]: # if the line is a header line...
				temp = process_section(header, lines) # process all the contents belonging to the previous header
				dictonary.update(temp) # include newly processed content in the  dictonary 
				header = line[2:-3] # get name of header (remove --- Header Name ---)
				# print("found header ", header )
				lines = list() # Empty lines list so the contents of the new header are the only things being processed when the next header roles around
			else:
				# print("content because ", line[0:2], "douesn't equal '--'")
				lines.append(line) # add the condents of the line to the lines list so the next time a header is hit it can process all the content belonging to the previous header
	temp = process_section(header, lines) # process the content of the last header
	dictonary.update(temp)

	print("found header ", header )
	test_case_file.close()
	return dictonary # dictonary contains all the information needed to create a judge


# called instead of get judge to process the .testJudge.bias files
def get_test_judge(file_name):
	# creates a dictonary of all the needed  information to create a judge
	test_case = test_file_to_dict(file_name)

	# creates a new judge object to hold the information given by .testJudge.bias 
	new_judge = Judge.Judge()

	# populate new-judge with the values exstracted from the dictonary
	new_judge.name = test_case['name']
	new_judge.paradigm_updated = test_case['date']
	new_judge.paradigm = test_case['paradigm']
	new_judge.rounds = test_case['table'].single_thread_to_round_list()
	new_judge.recorded_rounds = len(new_judge.rounds)
	return new_judge


 



def getCompetitors(WEBSITE_ADDRESS):
	USE_SELENIUM = False
	if USE_SELENIUM:
		# Using Chrome to access web for debuging
		driver = webdriver.Chrome()
		print("finding competitors names")
		# Use PhantomJS for speed (not working yet):
		# driver = webdriver.PhantomJS(executable_path=phantomjs_path)
		# driver = webdriver.phantomjs()
		# driver.set_window_size(1120, 550)

		# Open the website
		try:
			driver.get(WEBSITE_ADDRESS)

			names = list()

			# get name, paradigm, and date of update
			raw_names = driver.find_element(By.XPATH, './/*[@id="content"]/div[3]/div[1]/span[1]/h4').text
			print(raw_names)
			split_raw_names = raw_names.split(" & ")
			for i in split_raw_names:
				try:
					names.append(i.split()[0])
				except:
					names.append(i)
					print("i'm triggered")
			driver.quit()
			return names

		except Exception as e: 
			print(e)
			driver.quit()
			return None
	else:
		try: 
			u2 = urllib.request.urlopen(WEBSITE_ADDRESS, timeout=30) # timeout=30
			# for i in range(len(u2.readlines())):
			# 	print(i,"   ", u2.readlines()[i])
			counter = 0
			raw_names = ''
			names = list()
			next_line = 0
			for lines in u2.readlines():
				if '<h4 class="nospace semibold">' in str(lines):
					next_line = 2
				elif next_line != 0:
						raw_names += str(lines)
						print (counter, lines)
						next_line -= next_line
				counter += 1
			# try:
			# 	debater_url = urllib.request.urlopen(WEBSITE_ADDRESS)
			# 	debater_names_html = debater_url.read().decode("utf8")
			# 	debater_url.close()
			# except Exception as e:
			# 	print(e)
			# 	print("issue using urllib to find debater's names")
			# 	debater_url.close()
			# 	return None

			# # print(debater_names_html)
			# index_of_start_of_names = debater_names_html.index('<h4 class="nospace semibold">')+27
			# index_of_end_of_names = debater_names_html.index('</h4>', index_of_start_of_names)
			# print('start index is', index_of_start_of_names)
			# print('end index is', index_of_end_of_names)
			# raw_names = debater_names_html[index_of_end_of_names:index_of_end_of_names]
			# print(raw_names)
			raw_names = raw_names.replace(r"\t", '').replace("b'", '').replace(r"\n'", '')
			split_raw_names = raw_names.split("&amp;")
			for i in split_raw_names:
				if "<span" in i:
						print("coulnd't handle ", raw_names)
						names.append('')
				else:
					try:
						names.append(i.split()[0])
					except:
						names.append(i)
						print("i'm triggered")
			print(names)
			return names
		except Exception as e: 
			print(e)
			print('trying again')
			return getCompetitors(WEBSITE_ADDRESS)



# called by judge-stats
# starts the entire web scraping project to create a judge object ready for analsis
def get_judge (WEBSITE_ADDRESS):

	#during development process I am using chrome as selinums browser instead of a headless web browser for debugging
	driver = webdriver.Chrome()

	# after I have a minimume viable project I will transition from chrome to phantomJS to accelerate the web scraping process
	# USe PhantomJS for speed (not working yet)
	# driver = webdriver.PhantomJS(executable_path=phantomjs_path)
	# driver = webdriver.phantomjs()
	# driver.set_window_size(1120, 550)

	# Open the website
	driver.get(WEBSITE_ADDRESS)
	
	# create a judge object to populate with judges name, judges paradigm, date when the paradim was updated, list of tournaments the 
	# judge has participated in, and list of [debate] rounds objects which the judge has overseen
	new_judge = Judge.Judge()

	# get name, paradigm, and date of update
	parts_paradigm = driver.find_elements(By.CLASS_NAME, 'ltborderbottom')
	paradigm_update_and_author_html = parts_paradigm[0]
	paradigm_text_html = parts_paradigm[1]

	paradigm_update_and_author = paradigm_update_and_author_html.get_attribute('innerHTML')
	paradigm_text = paradigm_text_html.get_attribute('innerHTML')

	paradigm_update_and_author = paradigm_update_and_author.replace('<span class="half">', '', 2)
	paradigm_update_and_author = paradigm_update_and_author.replace('</span>', '', 4)
	paradigm_update_and_author = paradigm_update_and_author.replace(' rightalign semibold bluetext">', '', 2)
	paradigm_update_and_author = paradigm_update_and_author.replace('<h4>', '', 2)
	paradigm_update_and_author = paradigm_update_and_author.replace('</h4>', '', 2)
	paradigm_update_and_author = paradigm_update_and_author.replace('<span class="half', '', 1)
	paradigm_update_and_author = paradigm_update_and_author.replace('\n', '')
	paradigm_update_and_author = paradigm_update_and_author.replace('\t', '')
	# actual set statment for name and paradim update date
	new_judge.name, new_judge.paradigm_updated = paradigm_update_and_author.split(' ParadigmLast changed ')

	paradigm_text = paradigm_text.replace('<p>', '',)
	paradigm_text = paradigm_text.replace('</p>', '',)
	paradigm_text = paradigm_text.replace('</strong>', '',)
	paradigm_text = paradigm_text.replace('<strong>', '',)
	# actual set statment for paradigm test
	new_judge.paradigm = paradigm_text

	# this try block collects all the needed information and sends it to this judges table object
	try:
		table = driver.find_element(By.ID, 'record')
		try:
			for row in table.find_elements(By.XPATH, ".//tr"):

				# identify tournaments judge has participated in
				for td in row.find_elements(By.XPATH, ".//td[@class='nospace'][1]"):
					tournament = td.text
					if len(new_judge.tournaments) == 0 or tournament != new_judge.tournaments[-1]:
						new_judge.tournaments.append(tournament)
				table = Table()

				# Identify division
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap centeralign'][1]"):
					table.division.append(td.text)

				# Identify date
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][1]"):
					table.date.append(td.text)
					
				# Identify aff url
				for td in row.find_elements(By.XPATH, ".//td[@class='nospace'][3]/a"):
					table.aff.append(td.get_attribute('href'))
					# print(td.get_attribute('href'))
					# print(td.text)
					#You might also need a wait condition for presence of all elements located by css selector.
					#elems = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sc-eYdvao.kvdWiq [href]")))
				
				# Identify neg url
				for td in row.find_elements(By.XPATH, ".//td[@class='nospace'][4]/a"):
					table.neg.append(td.get_attribute('href'))
				
				# identify vote
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][2]"):
					table.vote.append(td.text)

				# identify result
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][3]"):
					table.result.append(td.text)

		except Exception as e: 
			print(e)
			print("issue iterating through judging record table")
	except:
		print("Issue finding table")
	driver.quit()
	print("finished reading judge")

	# takes the result of the table object and stores it in the rounds list of the new_judge object
	new_judge.rounds = table.to_round_list()
	new_judge.recorded_rounds = len(table.division)

	print("made judge")
	print("found data on ", len(new_judge.rounds), " out of ", new_judge.recorded_rounds) #gives the sucess rate of the web scraping and api calls

	return new_judge # returns the new judge object to either be saved as a .bias file or anylised
