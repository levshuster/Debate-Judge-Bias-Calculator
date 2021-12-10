import from_tab
import Judge
# save as .bias.temp the whole time

# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729' #lev
# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=26867' #laura
# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=52549' #random todd
WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=191506' # sam
api_calls_so_far = 0
NUMBER_OF_API_CALLS_PER_JUDGE = 10

if __name__ == '__main__':
	# print(from_tab.get_judge(WEBSITE_ADDRESS))
	# print(from_tab.get_judge(WEBSITE_ADDRESS).align_with_panal_percentage())
	# Judge.save(from_tab.get_judge(WEBSITE_ADDRESS))
	print(Judge.load('Lev Shuster.bias'))
	# print(Judge.load('Todd Mincks.bias'))
	# print(Judge.load('Laura Livingston.bias'))
	print(Judge.load('Sam Daily.bias'))




