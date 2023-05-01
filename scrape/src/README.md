# Index of Files

**.bias** files contain the debate round information needed to generate a judge object. By saving a file after collecting information on a judge but before saving information on a judge this decreases the amount of duplicate API calls and web scraping

**.testJudge.bias** contains the debate round information needed to generate a judge object from arbitrary inputs. This is used for debugging purposes 

**test_case_template.testJudge.bias** contains the information needed to create your own testJudge.bias file 

**judge_stats.py** will eventually contain the code for the alpha releases command line interface, however during the developmental phase it holds the main function of the project enabling testers to create, save, load, and analyze .bias files by calling functions called in from_tab.py and Judge.py

**Gender.py** provides the functionality to acsess the API who determins the gender and certainty of a given name and the file has a function to take the results of the API call and caculate the round score (see the How do you Quantify Discrimination? heading in the readme file)

**from_tab.py** offers functions charged with scrapping tabroom to get a list of all the rounds a judge has presided over, another part of this file scrapes all the names of competitors in each round

**judge.py** handles the loading, analyzing and saving of judge objects 

