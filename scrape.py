from cgitb import reset
from urllib.request import urlopen
import re #regular expressions
from structs import Round, Judge, Team, Debater
from api import getGender
import pandas as pd
from typing import Dict, List, Union
BASEURL = "https://www.tabroom.com"
FIRST = True
# returns a judge without a record
def paradigmHTML2JudgeObject(html: str, url)-> Judge:
    paradimText = {"lastChanged":"", "paradigm":""}
    
    name = re.search("<h3>(.*)</h3>", html)
    name = str(name.group()) if name else ""
    
    # x = re.search('<p>(.*)</p>', html)
    html = html.split(">\n\t\t\t\t\t<h5>Paradigm Statement</h5>\n\t\t\t\t</span>\n\n\t\t\t\t<span class=\"half rightalign semibold bluetext\">\n\t\t\t\t\t\t", 1)[1]
    html = html.split("</p>\n\t\t\t</div>\n\t\t</div>\n\n\t<div", 1)[0]
    paradimText["lastChanged"]= html.split("\n", 1)[0].split("Last changed ", 1)[1]
    paradimText["paradigm"]= re.sub("<.{0,7}>", "", html.split("ltborderbottom\">\n\t\t\t\t<p>", 1)[1])
    return Judge(name, paradimText, None, url)

def getCompetetors(url:str) -> Team:
    html = urlopen(BASEURL+url).read().decode('utf-8')
    # print("\n\n\n", url)
    html = re.sub("\thref   = \"(.*)\"\n\t*> ", "> \\1\t", re.sub("\t|\n", "", html))
    names = re.search("<h4 class=\"nospace semibold\">(.*)</h4", html)
    names = re.search(">.*<", str(names.group()) if names else "")
    names = str(names.group()) if names else ""
    team= Team()
    debaters:List[Debater] = []

    for name in names[1:-1].split("&amp;"):
        debaters.append(Debater(name, getGender(name.split(" ")[0])))
    team.debaters = debaters
    return team

def paradigmHTML2Record(html:str, judge) -> List[Round]:
    html = re.sub("\thref   = \"(.*)\"\n\t*> ", "> \\1\t", html)
    recordTable = pd.read_html(html)[0]
    # print(str(recordTable))
    rounds: List[Round] = []
    first = True
    for row in recordTable.iterrows():
        if first:
            case = row[1]
            aff = getCompetetors(case["Aff"].split("\t")[0])
            neg = getCompetetors(case["Neg"].split("\t")[0])
            newRound = Round(judge, case["Tournament"], case["Lv"], case["Date"], case["Ev"], case["Rd"], aff, neg, case["Vote"], str(case["Result"]))
            rounds.append(newRound)
            # print(newRound)
            first = False
    return rounds

def getParadigmFromJudgeId(judgeId: int) -> Judge:
    url = BASEURL+"/index/paradigm.mhtml?judge_person_id=" + str(judgeId)
    with urlopen(url) as response:
        body:str = response.read().decode('utf-8')
    judge = paradigmHTML2JudgeObject(body, url)
    judge.record=paradigmHTML2Record(body, judge)  
    return judge

# print(getParadigmFromJudgeId(105729))
getParadigmFromJudgeId(105729)