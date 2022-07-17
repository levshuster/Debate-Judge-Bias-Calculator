import json, store
from typing import List, Union
from structs import Debater, Gender
from urllib.request import urlopen

def loadCache() -> List[Debater]:
    cachedNames = []
    try:
        cachedNames = store.loadNameCache()
    except:
        print("No Cache Found")
    return cachedNames
    
cachedNames: List[Debater] = loadCache()

def saveCache() -> None:
    store.saveNameCache(cachedNames)
    
def getGender(name:str) -> Debater:
    name = name.lower()
    cachedName = getGenderFromCache(name)
    # return cachedName if cachedName else getGenderFromFreeAPI(name)
    return getGenderFromFreeAPI(name)
    
def getGenderFromFreeAPI(name:str) -> Debater:
    data = urlopen("https://api.genderize.io?"+"name[0]="+name).read()
    json_object = json.loads(data.decode('utf-8'))[0]
    # print(json_object)
    gender = Gender(json_object["gender"], json_object["probability"])
    debater = Debater(name, gender)
    cachedNames.append(debater) # may cause issue for multithreading
    return debater

def getGenderFromPremiumAPI(name:str) -> Gender:
    gender = Gender()
    return gender

def getGenderFromCache(name:str) -> Union[Debater, None]:
    # print("looking for "+name+"\n in ")
    # for i in cachedNames:
    #     print(i)
    cacheThatMatchesName = list(filter(lambda x: name == x.name, cachedNames))
    print ("\n\n\n\nTHE MATCHING CACHE IS "+str(cacheThatMatchesName[0]) if cacheThatMatchesName else "no cache found")
    return cacheThatMatchesName[0] if cacheThatMatchesName else None