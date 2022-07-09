import from_tab
import Judge

'''
judge_stats.py will eventually contain the code for the alpha releases comandline interface, however during the 
developmental phase it holds the main function of the project enabeling testers to create, save, load, and analyze
.bias files by calling functions called in from_tab.py and Judge.py
'''

# convert a .testJudge.bias to a .bias file then analize the results 
def run_test_case_file (FILE_NAME):
	Judge.save(from_tab.get_test_judge(FILE_NAME))
	print(Judge.load('Lev2 Shuster2.bias'))


# URLS to three real judges records
Lev_WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729'
Dave_WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=147333' #random dave (short record for testing)
Jenn_WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=78399' #jenn
Sam_WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=191506' # sam
Laura_WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=26867' #laura

if __name__ == '__main__':
	# run_test_case_file('test_case_template.testJudge.bias')


	# Example of how to get and analize judge information without ever saving it as a .bias file
	print(from_tab.get_judge(Lev_WEBSITE_ADDRESS))

	# Example of how to save a new judge as a .bias file from a URL
	# Judge.save(from_tab.get_judge(Lev_WEBSITE_ADDRESS))

	# Examples to load judges who already have a local file
	# print(Judge.load('Lev Shuster.bias'))
	# print(Judge.load('Dave Kerpen.bias'))
	# print(Judge.load('Laura Livingston.bias'))
	# print(Judge.load('Sam Daily.bias'))
	# print(Judge.load('Jennifer Johnson.bias'))



