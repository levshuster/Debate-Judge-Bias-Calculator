# -1 all male
# 0 one male one female or undeterminded
# all female
def getGenderBalance(names)
	if len(names) > 2:
		print("more than two names provided")
		exit()
	getGenders(names)
# getGenders(["Lev","Gail","Kendra", "Todd"])
# [('male', 0.95, 1007), ('female', 0.94, 2752), ('female', 0.96, 1251), ('male', 0.99, 6598)

# The MIT License (MIT)
# Copyright (c) 2013 block8437/acceptable-security
# https://github.com/acceptable-security/gender.py
import requests, json

def getGenders(names):
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
