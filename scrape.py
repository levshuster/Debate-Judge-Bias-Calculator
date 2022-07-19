from urllib.request import urlopen
import re #regular expressions
from structs import Round, Judge, Team, Debater
from api import getGender
import pandas as pd
from typing import Dict, List, Union
import asyncio
BASEURL = "https://www.tabroom.com"
FIRST = True

# returns a judge without a record
def paradigmHTML2JudgeObject(html: str, url)-> Judge:
    paradimText = {"lastChanged":"", "paradigm":""}
    
    name = re.search("<h3>(.*)</h3>", html)
    name = str(name.group())[4:-5] if name else ""
    print("name is ", name)
    # x = re.search('<p>(.*)</p>', html)
    html = html.split(">\n\t\t\t\t\t<h5>Paradigm Statement</h5>\n\t\t\t\t</span>\n\n\t\t\t\t<span class=\"half rightalign semibold bluetext\">\n\t\t\t\t\t\t", 1)[1]
    html = html.split("</p>\n\t\t\t</div>\n\t\t</div>\n\n\t<div", 1)[0]
    paradimText["lastChanged"]= html.split("\n", 1)[0].split("Last changed ", 1)[1]
    paradimText["paradigm"]= re.sub("<.{0,7}>", "", html.split("ltborderbottom\">\n\t\t\t\t<p>", 1)[1])
    return Judge(name, paradimText, None, url)

async def getCompetetors(url:str) -> Team:
    html = urlopen(BASEURL+url).read().decode('utf-8')
    # print("\n\n\n", url)
    html = re.sub("\thref   = \"(.*)\"\n\t*> ", "> \\1\t", re.sub("\t|\n", "", html))
    names = re.search("<h4 class=\"nospace semibold\">(.*)</h4", html)
    names = re.search(">.*<", str(names.group()) if names else "")
    names = str(names.group()) if names else ""
    team= Team()
    debaters:List[asyncio.Task[Debater]] = list(map(lambda name: asyncio.create_task(getGender(name.split(" ")[0])), names[1:-1].split("&amp;")))    
    
    # team.debaters = list(map(lambda debater: await debater, debaters))
    debaters2: List[Debater] = []
    for debater in debaters:
        debaters2.append(await debater)
        print("ended thread")
    team.debaters = debaters2
    return team
    
async def makeRound(counter, judge, case) -> Union[Round, None]:
    # try: # catches issues with tabroom and the api
    aff = asyncio.create_task(getCompetetors(case["Aff"].split("\t")[0]))
    neg = asyncio.create_task(getCompetetors(case["Neg"].split("\t")[0]))
    # await asyncio.gather(aff, neg)
    print("thread ended\n thread ended")
    newRound: Round = Round(judge, case["Tournament"], case["Lv"], case["Date"], case["Ev"], case["Rd"].split(" ")[0], await aff, await neg, str(case["Vote"]), str(case["Result"]))
    print(newRound)
    print(newRound.getGendersWeighting(0.7))
    return newRound
    # except:
    #     print("error in row ", counter)

async def paradigmHTML2Record(html:str, judge: Judge) -> List[Round]:
    html = re.sub("\thref   = \"(.*)\"\n\t*> ", "> \\1\t", html)
    recordTable = pd.read_html(html)[0]
    # print(str(recordTable))
    rounds: List[Round] = []
    counter = 0
    newRoundTask: list[asyncio.Task[Union[Round, None]]] = list(map(lambda row: asyncio.create_task(makeRound(counter, judge, row[1])), recordTable.iterrows()))
    # for row in recordTable.iterrows():
    #     newRoundTask.append = asyncio.create_task(makeRound(counter, judge, row[1]))
    for row in newRoundTask:
        newRound: Union[Round, None] = await row
        print("thread ended")
        rounds.append(newRound) if newRound else None
        counter += 1

    return rounds

def getParadigmFromJudgeId(judgeId: int) -> Judge:
    url = BASEURL+"/index/paradigm.mhtml?judge_person_id=" + str(judgeId)
    with urlopen(url) as response:
        body:str = response.read().decode('utf-8')
    judge = paradigmHTML2JudgeObject(body, url)
    judge.record=asyncio.run(paradigmHTML2Record(body, judge))
    # judge.record=paradigmHTML2Record(body, judge)  
    return judge
