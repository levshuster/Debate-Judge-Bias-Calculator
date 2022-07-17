
# uses pickle to save and load Judge objects as .bias files
# reference from https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
import pickle
from typing import List
from structs import Debater, Judge

CACHENAME = "names.cache"

def saveJudge (judge: Judge):
	with open(judge.name+'.bias', 'wb') as judge_file:pickle.dump(judge, judge_file)
def loadJudge (judge_file_name: str):
	with open(judge_file_name+'.bias', 'rb') as judge_file:return pickle.load(judge_file)
	
def saveNameCache (cache: List[Debater]):
	with open(CACHENAME, 'wb') as cache_file:pickle.dump(cache, cache_file)
def loadNameCache ():
	with open(CACHENAME, 'rb') as cache_file:return pickle.load(cache_file)
