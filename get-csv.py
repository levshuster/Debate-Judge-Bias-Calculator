import os
from selenium import webdriver
from selenium.webdriver.common.by import By
# from Judge import judge

class judge:
	def __init__(self, name = 'no name', paradigm = '''no paradigm''', paradigm_updated='no paradigm', tournaments = list() ):
		self.name = name
		self.paradigm = paradigm
		self.paradigm_updated = paradigm_updated
		self.tournaments = tournaments
 


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

	new_judge = judge()

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
				for td in row.find_elements(By.XPATH, ".//td[@class='nospace'][1]"):
					tournament = td.text
					if len(new_judge.tournaments) == 0 or tournament != new_judge.tournaments[-1]:
						new_judge.tournaments.append(tournament)
						print(tournament)
		except Exception as e: 
			print(e)
			print("issue iterating through judging record table")
	except:
		print("Issue finding table")
	driver.quit()
except Exception as e: 
	print(e)
	driver.quit()
	print("Issue opening website address")
		