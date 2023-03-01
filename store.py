
# uses pickle to save and load Judge objects as .bias files
# reference from https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
import argparse
import pickle
from typing import List
from structs import Debater, Judge

CACHENAME = "names.cache"

def saveJudge (judge: Judge, judge_file_name: str = ""):
	with open(validDotBiasFile(judge_file_name), 'wb') as judge_file:pickle.dump(judge, judge_file)
def loadJudge (judge_file_name: str):
	with open(judge_file_name, 'rb') as judge_file:return pickle.load(judge_file)
	
def saveNameCache (cache: List[Debater]):
	with open(CACHENAME, 'wb') as cache_file:pickle.dump(cache, cache_file)
def loadNameCache ():
	with open(CACHENAME, 'rb') as cache_file:return pickle.load(cache_file)

def validDotBiasFile (file_name: str)->str:
	if file_name.split('.')[-1] == 'bias':
		return file_name
	elif '.' not in file_name:
		return file_name+'.bias'
	else:
		raise argparse.ArgumentTypeError('File must be of type .bias')