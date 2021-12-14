import from_tab
import Judge
# save as .bias.temp the whole time


WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729' #lev
# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=147333' #random dave (short record for testing)
#WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=78399' #jenn
FILE_NAME = 'all_aff_female.txt'
if __name__ == '__main__':
	# print(from_tab.get_judge(WEBSITE_ADDRESS))
	# print(from_tab.get_judge(WEBSITE_ADDRESS).align_with_panal_percentage())
	FILE_NAME = 'test_case_template.testJudge.bias'
	Judge.save(from_tab.get_test_judge(FILE_NAME))
	print(Judge.load('Lev2 Shuster2.bias'))
	
	# Judge.save(from_tab.get_judge(WEBSITE_ADDRESS))
	# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=26867' #laura
	
	# Judge.save(from_tab.get_judge(WEBSITE_ADDRESS))
	# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=191506' # sam
	# Judge.save(from_tab.get_judge(WEBSITE_ADDRESS))

	# print(Judge.load('Lev Shuster.bias'))
	# print(Judge.load('Dave Kerpen.bias'))
	# print(Judge.load('Laura Livingston.bias'))
	# print(Judge.load('Sam Daily.bias'))
	# print(Judge.load('Jennifer Johnson.bias'))





