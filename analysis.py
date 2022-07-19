
import functools
from scrape import getParadigmFromJudgeId
from store import loadJudge, saveJudge
from structs import Judge, getCountWithinThreshold
import api

def printGenderBias(judge: Judge, confidanceThreshold: float) -> None:
    genderBias: list[int] = list(map(lambda a: a.getGendersWeighting(confidanceThreshold), judge.record))

    votesForMen = abs(sum(filter(lambda a: a < 0, genderBias)))
    votesForWomen = sum(filter(lambda a: a > 0, genderBias))
    
    if votesForWomen > votesForMen:
        genderWithMoreVotes: str ="woman"
    elif votesForWomen < votesForMen:
        genderWithMoreVotes = "men"
    else:
        genderWithMoreVotes = "neither"
    
    countWithinThreshold = getCountWithinThreshold(judge.record, confidanceThreshold)
    
    print("Out of %i rounds in %s's record, %i rounds had all particiapnts' names exceed the threshold of %f" % (countWithinThreshold["total"], judge.name, countWithinThreshold["withinThreshold"], confidanceThreshold))
    print("\nmen had %i votes and woman had %i votes which means %s had %i%% more votes" % (votesForMen, votesForWomen, genderWithMoreVotes, (abs(votesForMen - votesForWomen) / (votesForMen + votesForWomen) * 100) if votesForMen - votesForWomen else 0))



# lev = getParadigmFromJudgeId(105729)
# print(getCountWithinThreshold(lev.record, 0.7))
# saveJudge(lev)
# lev = loadJudge("Lev Shuster")
# print(getCountWithinThreshold(lev.record, 0.7))
# printGenderBias(lev, .7)
# api.saveCache()

# dave = getParadigmFromJudgeId(147333)
# print(getCountWithinThreshold(dave.record, 0.7))
# saveJudge(dave)
# dave = loadJudge("Dave Kerpen")
# printGenderBias(dave, .7)

# print(getCountWithinThreshold(dave.record, 0.7))
# api.saveCache()

laura = getParadigmFromJudgeId(26867)
saveJudge(laura)
api.saveCache()
printGenderBias(laura, .7)

