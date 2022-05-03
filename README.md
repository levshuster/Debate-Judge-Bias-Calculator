# Introduction

I’ve spent six years in competitive academic debate as a judge, team captain,  and competitor. One of the unique things about debate is the role of a judge. In the wider world judges determine if someone slides into a base before being tagged or decides if someone has broken a rule, but in debate, the judge decides who is more convincing. This introduces a huge amount of freedom to the judge and means that there is a huge amount of room for bias in the judge’s decision (as any participant will attest to). Also caused by this degree of freedom is any decision a judge makes will anger one of the two teams, so coaches quickly learn to dismiss crestfallen teenagers when they attribute their loss to a judge’s prejudice. 

This project started in 2021 year when I stumbled across an API that takes a name and returns the gender the name likely belongs to. Because there are thousands of debate tournaments who posted the results of every round on the same website (including the names of debaters and judges), I decided to collect the information of every debate round a given judge has overseen and use the API to determine if said judge systematically votes for male debaters over female debaters (which would be a sign of sexism in a judge’s decision). From there I could consider the roster of judges at a given tournament or league to compare the amount of bias at different tournaments or leagues.

If you have any interest in learning about the rampant discrimination in United States Debate here are some great articles. 
TLDR: there is a disgusting amount of sexism in debate which causes girls to be forced out of the activity at depressing rates. There has been quantitative research on the effect of sexism but no substantial work on the effect and existance of discriminatory Judges within the activity.
https://sarahisomcenter.org/blog/2019/11/20/combatting-sexism-in-speech-and-debate-programs
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715996
https://www.semanticscholar.org/paper/Gender-Disparities-in-Competitive-High-School-New-Tartakovsky/28818fee3ee742cbb88eabb93644ebf8ea8e4370

# Judge-Bias-Calculator

Desktop program that aims to measure sign of debate judge bias from tabroom records.
![image](https://user-images.githubusercontent.com/87684029/166580109-79c750e5-221a-4048-9bfa-5331ec036ae9.png)

# Todo

- [ ] add round and division ('jv' and R4) line 90 in from_tab.py

- [ ] must add way to simulate panel decision line 131 in from_tab.py

- [ ] add try case file could not be found line 139 in from_tab.py

