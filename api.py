import json
from typing import List, Union
import urllib3
from structs import Debater, Gender
from urllib.request import urlopen

def loadCache() -> List[Debater]:
    print("figure out were cache will be stored")
    return []
cachedNames: List[Debater] = loadCache()

def getGender(name:str) -> Debater:
    name = name.lower()
    print("given name is ", name)
    cachedName = getGenderFromCache(name)
    return cachedName if cachedName else getGenderFromFreeAPI(name)
    
def getGenderFromFreeAPI(name:str) -> Debater:
    data = urlopen("https://api.genderize.io?"+"name[0]="+name).read()
    json_object = json.loads(data.decode('utf-8'))[0]
    # print(JSON_object)
    gender = Gender(json_object["gender"], json_object["probability"])
    debater = Debater(name, gender)
    cachedNames.append(debater) # may cause issue for multithreading
    return debater

def getGenderFromPremiumAPI(name:str) -> Gender:
    gender = Gender()
    return gender

def getGenderFromCache(name:str) -> Union[Debater, None]:
    cacheThatMatchesName = list(filter(lambda x: name is x, cachedNames))
    return cacheThatMatchesName[0] if cacheThatMatchesName else None