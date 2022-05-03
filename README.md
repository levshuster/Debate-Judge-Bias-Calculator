# Introduction

I’ve spent six years in competitive academic debate as a judge, team captain,  and competitor. One of the unique things about debate is the role of a judge. In the wider world judges determine if someone slides into a base before being tagged or decides if someone has broken a rule, but in debate, the judge decides who is more convincing. This introduces a huge amount of freedom to the judge and means that there is a huge amount of room for bias in the judge’s decision (as any participant will attest to). Also caused by this degree of freedom is any decision a judge makes will anger one of the two teams, so coaches quickly learn to dismiss crestfallen teenagers when they attribute their loss to a judge’s prejudice. 

This project started in 2021 year when I stumbled across an API that takes a name and returns the gender the name likely belongs to. Because there are thousands of debate tournaments who posted the results of every round on the same website (including the names of debaters and judges), I decided to collect the information of every debate round a given judge has overseen and use the API to determine if said judge systematically votes for male debaters over female debaters (which would be a sign of sexism in a judge’s decision). From there I could consider the roster of judges at a given tournament or league to compare the amount of bias at different tournaments or leagues.

If you have any interest in learning about the rampant discrimination in United States Debate here are some great articles. 
TLDR: there is a disgusting amount of sexism in debate which causes girls to be forced out of the activity at depressing rates. There has been quantitative research on the effect of sexism but no substantial work on the effect and existance of discriminatory Judges within the activity.
https://sarahisomcenter.org/blog/2019/11/20/combatting-sexism-in-speech-and-debate-programs
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715996
https://www.semanticscholar.org/paper/Gender-Disparities-in-Competitive-High-School-New-Tartakovsky/28818fee3ee742cbb88eabb93644ebf8ea8e4370

# How do you Quantify Discrimination?

Desktop program that aims to measure sign of debate judge bias from tabroom records.
![image](https://user-images.githubusercontent.com/87684029/166580109-79c750e5-221a-4048-9bfa-5331ec036ae9.png)

# Timeline

# Example Scenarios using Command Line Interface

## Student 

## Tournament Organizer

Task: I want to identify which judges in at my tournament I should keep the closest eye on or only use when no other judges are available

Application of Debate-Judge_Bias-Caculator: 
1. Use the Collect_Judge_List [Tabroom_URL] [Destination.txt] where Tabroom_URL is the link to your roster of judges for the upcoming tournament. This will save a text file that lists all the judges you wish to analyze 
2. Use the Batch_Scrape_Judging_record [List_of_judges.txt] command to collect the needed information on each judge named in the given text file and save it locally as a collection of .bias files
3. Use the return_bias_pvalue_less_than [List_of_judges.txt] [pvalue_ceiling] to print all the judges with a p-value less than a given p-value 

Result: Debate-Judge_Bias-Caculator produces a list of judges who are most likely to let their internal sexism affect their judging decisions. As such these judges should be kept away from new debaters, should be closely watched, 

## League Leadership

Task: I want to identify which judges in my league might most benif from anti-bias training

Application of Debate-Judge_Bias-Caculator: 
1. Use the Collect_Judge_List [Tabroom_URL] [Destination.txt] to save a text file that lists all the judges you wish to analyze or manually enter the names of judges you wish to analyze in a new textfile 
2. Use the Batch_Scrape_Judging_record [List_of_judges.txt] command to collect the needed information on each judge named in the given text file and save it locally as a collection of .bias files
3. Use the return_bias_pvalue_less_than [List_of_judges.txt] [pvalue_ceiling] to print all the judges with a p-value less than p_value_ceiling 

Result: Debate-Judge_Bias-Caculator produces a list of judges who are most likely to let their internal sexism affect their judging decisions.

# Index of Files
