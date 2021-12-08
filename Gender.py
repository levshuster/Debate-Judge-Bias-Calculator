import requests, json
import from_tab

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
		if result["gender"] is not None:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			retrn.append((u'None',u'0.0',0.0))
	return retrn



SERTAINTY_THREASHOLD = 0.7
#MM vs MM and FF vs FF and F? vs MM... are thrown out (0)
#if FF win over FM then +.5	if MM win over FM then -.5
#if FF win over MM then +1	if MM win over FF then -1
def vote_for_more_woman(aff_url, neg_url, vote):
	aff_names = from_tab.getCompetitors(aff_url)
	neg_names = from_tab.getCompetitors(neg_url)
	print(aff_names)
	print(neg_names)
	if aff_names and neg_names:
		return getGenderBalance(aff_names+neg_names, vote)
	else:
		return 0

def getGenderBalance(names=list(), vote=None):
	genders_of_names = getGenders(names)
	number_of_debators = len(genders_of_names)

	#put winning team first and remove rounds that don't end in normal ballot
	if vote == "Neg":
		count_step=-1
		count_start = number_of_debators
		count_end = 1
	elif vote == 'Aff':
		count_step=1
		count_start = -1
		count_end = number_of_debators-1
	else:
		return 0

	# removes names that are not clearly femine or masculine
	for i in genders_of_names:
		if i[1]<SERTAINTY_THREASHOLD:
			return 0

	# handles Lincon Douglas Debate, Big Questions, etc.
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
		print((gender_list[0]+gender_list[1]-gender_list[2]-gender_list[3])/4)
		return (gender_list[0]+gender_list[1]-gender_list[2]-gender_list[3])/4 #this won't make any sence until you write out all the possibilites
	else: #debate forms with any other number of debaters get ignored
		return 0
# print(getGenderBalance(["lev", "Todd", "Kendra","lev"], 'Aff'))
# [('male', 0.95, 1007), ('female', 0.94, 2752), ('female', 0.96, 1251), ('male', 0.99, 6598)


