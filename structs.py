from typing import Dict, List, Union
from xmlrpc.client import DateTime
wordForAffermative = ['aff', 'gov']

class Gender:
    confidance: float
    gender: str #"male" | "female" | "nonbinary" | "unknown"
    
    def weight(self, gender: str) -> int:
        if gender == "male":
            return -1
        elif gender == "female":
            return 1
        else:
            return 0
            
    def getGender(self, confidanceThreshold:int) -> Union[None, int]:
        return  self.weight(self.gender) if confidanceThreshold <= self.confidance else None
    
    def __init__(self, gender:str="", confiance:float=0) -> None:
        self.confidance = confiance
        self.gender = gender if gender else "Unknown"
        
    def __str__(self) -> str:
        return self.gender+'\t'+str(self.confidance)

class Age:
    confidance: int
    age: int 
    def getAge(self, confidance_threshold:int) -> Union[int, None]:
        return self.age if confidance_threshold <= self.confidance else None 

class Debater:
    name: str
    gender: Gender
    
    def __init__(self, name, gender) -> None:
        self.name = name
        self.gender = gender  
    
    def __eq__(self, other): # : Union[Debater, str]
        if isinstance(other, Debater):
            return self.name == other.name
        elif isinstance(other, int):
            return other == self.name
    def __str__(self) -> str:
        return "name: "+self.name+"\tgender: "+str(self.gender)
# team is a pair or more of debaters not to be confused with a school which is a collection of teams
class Team:
    debaters: List[Debater]
    def getGenders(self, confidance_threshold) -> Union[int, None]:
        counter = 0
        for debater in self.debaters:
            debaterGender = debater.gender.getGender(confidance_threshold)
            if debaterGender is None:
                return None
            else:
                counter += debaterGender
        return counter
    
    def __str__(self) -> str:
        string =  ""
        for debater in self.debaters:
            string += str(debater) + "\n"
        return string


class Round:
    judge: object # specifically it should be a judge object
    tournamentName: str
    level: str # hs, ms etc.
    date: DateTime
    eventFormat: str # Jv, Nov, etc.
    eventRound: str # R1, Quart, etc.
    aff: Team
    neg: Team
    vote: str # when creating round, check to ensure that vote is either aff or neg and no other string
    result: Union[Dict[str, int], None] = {'aff':-1, 'neg':-1} # -1 means this is not a paneled round (default)
    
    def getResult(self, string) -> Union[Dict[str, int], None]:
        if "nan" in string: return None
        digit1:int = int(string[5])
        digit2:int = int(string[7])
        return {'aff':digit1, 'neg':digit2} if string.lower() in wordForAffermative else {'aff':digit2, 'neg':digit1}

    def __init__(self, judge, tournamentName, level, date, eventFormat, eventRound, aff: Team, neg: Team, vote: str, result):
        self.judge = judge
        self.tournamentName = tournamentName
        self.level = level
        self.date = date
        self.eventFormat = eventFormat
        self.eventRound = eventRound
        self.aff = aff
        self.neg = neg
        self.vote = vote.lower()
        self.result = self.getResult(result)
        
    def __str__(self):
        return "\n\nTournament name: " + self.tournamentName + "\n level " + self.level + "\n event format " + self.eventFormat + "\n event round " + self.eventRound + "\n vote " + self.vote + "\n result " + str(self.result) + "\n\n" + str(self.aff) + "\n\n" + str(self.neg)
        
    # assumes vote is either 'aff' or 'neg'
    def getGendersWeighting(self, confidance_threshold) -> int:
        winningCount = (self.aff if self.vote == 'aff' else self.neg).getGenders(confidance_threshold)
        loosingCount = (self.neg if self.vote == 'aff' else self.aff).getGenders(confidance_threshold)
        return winningCount - loosingCount if winningCount is not None and loosingCount is not None else 0


class Judge:
    name: str
    paradigm: Dict[str, Union[DateTime, str]] #{"LastUpdated": DateTime, "Paradigm": str}
    gender: Gender
    age: Age
    url: str
    record: List[Round]
    
    def __init__(self, name, paradigm, gender, url) -> None:
        self.name = name
        self.paradigm = paradigm
        self.gender = gender
        self.url = url
        

class Tournament:
    judges: List[Judge]
    rounds: List[Round]
    
def getDivision(rounds: List[Round], division: str) -> List[Round]:
    return list(filter(lambda round: round.level == division, rounds))

def getFormat(rounds: List[Round], format: str) -> List[Round]:
    return list(filter(lambda round: round.eventFormat == format, rounds))
    
class League:
    tournaments: List[Tournament]
    judges: List[Dict[str, Union[Judge, int]]] # Array<{judge: judge, frequency: integer}>


    
def getCountWithinThreshold(rounds: List[Round], confidance_threshold: float) -> Dict[str, int]:
        withinThreshold = 0
        for round in rounds:
            if round.getGendersWeighting(confidance_threshold) != 0:
                withinThreshold += 1
        return {'total': len(rounds), 'withinThreshold': withinThreshold}
