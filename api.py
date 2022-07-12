from structs import Gender
cacheIsLoaded = False
def getGender(name:str) -> Gender:
    gender = Gender()
    return gender
    
def getGenderFromFreeAPI(name:str) -> Gender:
    gender = Gender()
    return gender

def getGenderFromPremiumAPI(name:str) -> Gender:
    gender = Gender()
    return gender

def loadCache():
    print("figure out were cache will be stored")

def getGenderFromCache(name:str) -> Gender:
    if not cacheIsLoaded: loadCache()
    gender = Gender()
    return gender