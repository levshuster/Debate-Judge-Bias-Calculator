class gender
    double: confidance
    tuple: gender-male, female, nonbinary
    getGender() take in a threshold and returns male, female, nonbinary, or unknown
    
class age
    double: confidance
    integer: age
    getGender() take in a threshold and returns an int or unknown

Class debater
    string:  name
    duple: gender
    
class team
    1 or more debaters (iteratable)
    getgenders() takes in a threshold and returns an integer (+2 mean all female) or null
    
class round
    tuple teams {aff: team, neg: team}
    judge judge
    string: tournamentName
    string: level
    string: date
    tuple: format - policy, ld, etc
    tuple: division - varsity, novice, etc.
    string: round - Octas, R5, R1, etc. 
    Array<{aff: integer, neg: integer}>: result
    tuple: vote - aff or neg
    getGenderWeighting() takes in a threshold and returns an integer or null (+4 means an all female team   beat an all male team) 
    
class judge
    string: name
    Array<{date: Date, text: string}>: paradigm
    gender: gender
    age: age
    Array<round>: record
    
class tournament
    Array<judge>: judges
    Array<round>: rounds
    Array<string>:leagues
    getDivision() takes in an array of rounds and a string and returns an array of rounds with a divsion property that matches the string
    getFormat() takes in an array of rounds and a string and returns an array of rounds with a format property that matches the string
    
class league
    Array<tournament>
    Array<{judge: judge, frequency: integer}>
    
def scrapeRound(Array<url:string>): round

def scrapeJudge(string: url): judge

def scrapeTournament(string: url): tournament

def getGender(name:string): gender

# next steps
- make multithreaded
- getGender can intelegently switch between cached names, free and payed api requests
- when creating a round, fucntion will check to see if teams already exist before creating new teams
- create scrape tournament
- create scrape league
- export as json
- export as csv
- export washington debate leage as kaggle dataset
- export as sql
- create gui
