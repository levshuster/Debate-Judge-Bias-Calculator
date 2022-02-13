import requests, json
import from_tab

USE_API = True
SERTAINTY_THREASHOLD = 0.7

# The MIT License (MIT)
# Copyright (c) 2013 block8437/acceptable-security
# https://github.com/acceptable-security/gender.py
def getGenders(names):
	print("api call")
	url = ""
	cnt = 0
	if not isinstance(names,list):
		names = [names,]
	
	for name in names:
		if url == "":
			url = "name[0]=" + name
		else:
			cnt += 1
			url = url + "&name[" + str(cnt) + "]=" + name
		

	req = requests.get("https://api.genderize.io?" + url)
	results = json.loads(req.text)
	
	retrn = []
	for result in results:
		print(result)
		if result == 'error':
			print('max api calls reached')
			retrn.append((u'None',u'0.0',0.0))
			
		elif result["gender"] is not None:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			retrn.append((u'None',u'0.0',0.0))
		
	return retrn



#MM vs MM and FF vs FF and F? vs MM... are thrown out (0)
#if FF win over FM then +.5	if MM win over FM then -.5
#if FF win over MM then +1	if MM win over FF then -1
def vote_for_more_woman(aff_url, neg_url, vote):
	#if statment to account for test files
	if isinstance(aff_url, list):
		print('is list    vote is"'+vote+'"')
		print('\n\n         gender ballance is ', getGenderBalance(aff_url + neg_url, vote))
		return getGenderBalance(aff_url + neg_url, vote)
	else:
		print('not list')
		aff_names = from_tab.getCompetitors(aff_url)
		neg_names = from_tab.getCompetitors(neg_url)
		if USE_API:
			return getGenderBalance(getGenders(aff_names+neg_names), vote)
		else: return 100

def getGenderBalance(genders_of_names=list(), vote=None):
	print('gender of names is', genders_of_names)
	number_of_debators = len(genders_of_names)

	#put winning team first and remove rounds that don't end in normal ballot
	if "Neg" in vote or 'Con' in vote:
		count_step=-1
		count_start = number_of_debators
		count_end = 0
		print("neg win")
	elif 'Aff' in vote or 'Pro' in vote:
		count_step=1
		count_start = -1
		count_end = number_of_debators-1
		print("aff win")
	else:
		print('else case triggered')
		return 0

	print(number_of_debators)

	# removes names that are not clearly femine or masculine
	for i in genders_of_names:
		if float(i[1])<SERTAINTY_THREASHOLD:
			print(i, "doesn't meet the sertainty threashold")
			return 0
	print('finished unsertanty filter\n\n')
	# handles Lincon Douglas Debate, Big Questions, etc.
	print(count_start)
	print('gender of names ', genders_of_names[count_start])
	if number_of_debators == 2 :
		if genders_of_names[count_start][0] == 'male':
			return -1
		else:
			return 1 
	#handle policy, pofo, etc.
	elif number_of_debators == 4:
		counter = count_start
		gender_list = list()
		while counter != count_end:
			counter += count_step
			if genders_of_names[counter][0] == 'male':
				gender_list.append(-1)
			else:
				gender_list.append(1)
		print(gender_list)
		print((gender_list[0]+gender_list[1]-gender_list[2]-gender_list[3])/4)
		return (gender_list[0]+gender_list[1]-gender_list[2]-gender_list[3])/4 #this won't make any sence until you write out all the possibilites
	else: #debate forms with any other number of debaters get ignored
		return 0
# print(getGenderBalance(['Aimen', 'Harini', 'Felix', 'Ethan'], 'Neg'))
# [('male', 0.95, 1007), ('female', 0.94, 2752), ('female', 0.96, 1251), ('male', 0.99, 6598)


