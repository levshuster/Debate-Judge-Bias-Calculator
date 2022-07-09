from multiprocessing.dummy import Array
import string
from typing import Dict, List, Union
from xmlrpc.client import DateTime
import functools

class Gender:
    confidance: int
    gender: str #"male" | "female" | "nonbinary"
    
    def weight(self, gender: str) -> int:
        if gender == "male":
            return -1
        elif gender == "female":
            return 1
        else:
            return 0
            
    def getGender(self, confidance_threshold:int) -> Union[None, int]:
        return  self.weight(self.gender) if confidance_threshold <= self.confidance else None 

class Age:
    confidance: int
    age: int 
    def getAge(self, confidance_threshold:int) -> Union[int, None]:
        return self.age if confidance_threshold <= self.confidance else None 

class Debater:
    name: str
    gender: Gender
    
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

class Round:
    judge: object # specifically it should be a judge object
    aff: Team
    neg: Team
    
    tournamentName: str
    level: str
    date: DateTime
    eventFormat: str
    division: str
    eventRound: str
    
    result = {'aff':-1, 'neg':-1} # -1 means this is not a paneled round (default)
    vote: str # when creating round, check to ensure that vote is eighter aff or neg and no other string

    # assumes vote is either 'aff' or 'neg'
    def getGendersWeighting(self, confidance_threshold) -> Union[int, None]:
        winningCount = (self.aff if self.vote == 'aff' else self.neg).getGenders(confidance_threshold)
        loosingCount = (self.neg if self.vote == 'aff' else self.aff).getGenders(confidance_threshold)
        return winningCount - loosingCount if winningCount is not None and loosingCount is not None else None


class Judge:
    name: str
    paradim: Dict[DateTime, str]
    gender: Gender
    age: Age
    record: List[Round]

