
from scrape import getParadigmFromJudgeId
from store import loadJudge, saveJudge
from structs import getCountWithinThreshold
import api

# lev = getParadigmFromJudgeId(105729)
# print(getCountWithinThreshold(lev.record, 0.7))
# saveJudge(lev)
# lev2 = loadJudge("Lev Shuster")
# print(getCountWithinThreshold(lev2.record, 0.7))
# api.saveCache()

dave = getParadigmFromJudgeId(147333)
print(getCountWithinThreshold(dave.record, 0.7))
saveJudge(lev)
dave2 = loadJudge("dave")
print(getCountWithinThreshold(dave2.record, 0.7))
api.saveCache()