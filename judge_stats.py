WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729'
import from_tab
import Judge

# WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729' #lev
WEBSITE_ADDRESS = 'https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=26867' #laura
# print(from_tab.get_judge(WEBSITE_ADDRESS))
# print(from_tab.get_judge(WEBSITE_ADDRESS).align_with_panal_percentage())
Judge.save(from_tab.get_judge(WEBSITE_ADDRESS))
# print(Judge.load('Lev Shuster.bias'))
