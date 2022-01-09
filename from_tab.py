import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import Judge
import concurrent.futures
import urllib.request


#used so that you can parse "full judging record" by row before going by line to populate a judge object with round objects
class Table:
	def __init__(self, division = list(), date = list(), aff=list(), neg = list(), vote = list(), result = list() ):
		self.division = division
		self.date = date
		self.aff = aff
		self.neg = neg
		self.vote = vote
		self.result = result
	
	def make_round(self, counter):
		print('aff is', self.aff[counter])
		print(self.division[counter], self.date[counter], self.aff[counter], self.neg[counter], self.vote[counter], self.result[counter])
		return Judge.Round(self.division[counter], self.date[counter], self.aff[counter], self.neg[counter], self.vote[counter], self.result[counter])

	def single_thread_to_round_list(self):
		rounds = list()
		for i in range(len(self.division)):
			print('starting round', i)
			rounds.append(self.make_round(i))
		return rounds
	def to_round_list(self):
		rounds_proceses = list()
		rounds = list()
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




#Handles Test files
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
		
		# add round and division ('jv' and R4)
		
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
	#add try case file could not be found
	print("started files to dict")
	test_case_file = open(file_name, "r")
	header = ''
	lines = list()
	dictonary = {'test':True}
	for line in test_case_file:
		# print(line)
		if '#' != line[0:1]:
			if '--' == line[0:2]:
				temp = process_section(header, lines)
				dictonary.update(temp)
				header = line[2:-3]
				# print("found header ", header )
				lines = list()
			else:
				# print("content because ", line[0:2], "douesn't equal '--'")
				lines.append(line)
	temp = process_section(header, lines)
	dictonary.update(temp)
	print("found header ", header )
	test_case_file.close()
	return dictonary



def get_test_judge(file_name):
	test_case = test_file_to_dict(file_name)
	new_judge = Judge.Judge()
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
		# USe PhantomJS for speed (not working yet)
		# driver = webdriver.PhantomJS(executable_path=phantomjs_path)
		# driver = webdriver.phantomjs()
		# driver.set_window_size(1120, 550)

		# Open the website
		try:
			driver.get(WEBSITE_ADDRESS)

			names = list()

			# get name, paradigm, and date of update
			# //*[@id="content"]/div[3]/div[1]/span[1]/h4

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
			print('start 1')
			u2 = urllib.request.urlopen(WEBSITE_ADDRESS, timeout=30) # timeout=30
			print('end')
			# for i in range(len(u2.readlines())):
			# 	print(i,"   ", u2.readlines()[i])
			counter = 0
			raw_names = ''
			names = list()
			next_line = 0
			for lines in u2.readlines():
				# print("for loop")
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




def get_judge (WEBSITE_ADDRESS):
	# Using Chrome to access web for debuging
	driver = webdriver.Chrome()

	# USe PhantomJS for speed (not working yet)
	# driver = webdriver.PhantomJS(executable_path=phantomjs_path)
	# driver = webdriver.phantomjs()
	# driver.set_window_size(1120, 550)

	# Open the website
	# try:
	driver.get(WEBSITE_ADDRESS)

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
	new_judge.name, new_judge.paradigm_updated = paradigm_update_and_author.split(' ParadigmLast changed ')
	# print("name is " +new_judge.name)
	# print("date is " +new_judge.paradigm_updated)

	paradigm_text = paradigm_text.replace('<p>', '',)
	paradigm_text = paradigm_text.replace('</p>', '',)
	paradigm_text = paradigm_text.replace('</strong>', '',)
	paradigm_text = paradigm_text.replace('<strong>', '',)
	new_judge.paradigm = paradigm_text
	# print(new_judge.paradigm)

	try:
		table = driver.find_element(By.ID, 'record')
		# remove try then code runs reliably
		try:
			for row in table.find_elements(By.XPATH, ".//tr"):
				# identify tournaments judge has participated in
				for td in row.find_elements(By.XPATH, ".//td[@class='nospace'][1]"):
					tournament = td.text
					if len(new_judge.tournaments) == 0 or tournament != new_judge.tournaments[-1]:
						new_judge.tournaments.append(tournament)
						# print(tournament)
				table = Table()
				# Identify division
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap centeralign'][1]"):
					table.division.append(td.text)
				# Identify date
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][1]"):
					table.date.append(td.text)
					# print(td.text)
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
					# print(td.get_attribute('href'))
					# print(td.text)
				# identify vote
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][2]"):
					table.vote.append(td.text)
					# print(td.text)
				# identify result
				for td in row.find_elements(By.XPATH, ".//td[@class='nowrap'][3]"):
					table.result.append(td.text)
					# print(td.text)

		except Exception as e: 
			print(e)
			print("issue iterating through judging record table")
	except:
		print("Issue finding table")
	driver.quit()
	print("finished reading judge")
	new_judge.rounds = table.to_round_list()
	new_judge.recorded_rounds = len(table.division)
	print("made judge")
	print("found data on ", len(new_judge.rounds), " out of ", new_judge.recorded_rounds)
	return new_judge

	# except Exception as e: 
	# 	print(e)
	# 	driver.quit()
	# 	print("Issue opening website address")
		