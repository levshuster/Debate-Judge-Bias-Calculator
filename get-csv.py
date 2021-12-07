import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import Judge



 
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
		return Judge.Round(self.division[counter], self.date[counter], self.aff[counter], self.neg[counter], self.vote[counter], self.result[counter])

	def to_round_list(self):
		rounds = list()
		for i in range(len(self.division)):
			rounds.append(self.make_round(i))
		return rounds



WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729'

# Using Chrome to access web for debuging
driver = webdriver.Chrome()

# USe PhantomJS for speed (not working yet)
# driver = webdriver.PhantomJS(executable_path=phantomjs_path)
# driver = webdriver.phantomjs()
# driver.set_window_size(1120, 550)

# Open the website
try:
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

	new_judge.rounds = table.to_round_list()
	print(new_judge)
	driver.quit()
except Exception as e: 
	print(e)
	driver.quit()
	print("Issue opening website address")
		