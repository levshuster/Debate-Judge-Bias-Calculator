# Debate-Judge-Bias-Calculator
## A Scraping and Analysis Tool Helping Citizen Data Scientists to Analyze Debate Records Across Tournaments and Judges

## Introduction

Over Six years as a judge and competitor within academic debate, I've found the role of judges unique and fascinating. In other forms of competition, judges enforce rules or make judgments along a clearly defined rubric. In contrast, debate judges make a single decision (Which debated better upholds the resolution). The rubric they judge by is ephemeral, differs by judges (See judge adaptation and judge paradigms), and is partially defined within each round (See Framework, Value/Criterion, Kritik, .etc).  This unique role makes judges decision effectively unchecked.

The arbitrary nature of judges decision making combined with the deeply personal nature of debate cause debaters to frequently level complaints against Judges. This frequency may cause Coaches to prematurely dismiss their students' complaints. **This tool's aims to augment current discussions around the rampant bias debate is struggling to address augment existing conversations with statistical insights.**

Much of the debate community have long moved from running tournaments with paper to a central tournament management software: TabRoom. Because tournament records are public and standardized on TabRoom, A judges records can be reconstruct for the last decade. This tool explore tournament and judges records through a handful or lenses. 
- Does a judge have an Aff-Neg bias (may be helpful when debaters have a coin flip to pick sides)?
- How do different debate leagues retention rates compare across time?
- How does a school's debate drop-out rate compare to its league's drop-out rate?
- How often do judges vote against a panel (a proxy for how different is a judge's decision making from the "average" judge).
- Does a judge give more or less speaker points than their peers (may be helpful when picking judge preferences).
- **Does a tournament, school, or league have a record of gender discrimination in who quits, who wins, and who earns more speaker points (May provide a unique link for a Fem-K or related argument)**  
- **Do Judges appear to have a gender bias in their voting or assignment of speaker points?**

To find correlations related to the last two bullet points, we need to know the gender of debaters. Understandably, TabRoom does not publish this information. To approximate gender, we take a dataset of all people born in the USA in the last some number of years, and group by first name. By comparing the number of girls to boys for a given name we find a very rough approximation of each names gender. This methodology is fundamentally flawed because it only considers names and genders assigned at birth, only considers people born/reported in the USA, and will only ever label individuals into two genders. To address these shortcomings:
- This tool can be configured to exclude gender neutral names or consider gender neutral as a third category. 
- For names that do not belong to many USA born children, we turn to an external API that considers records from across the world. However, the cost of this API makes it untenable to rely on for all names and the API remains Eurocentric. 
Despite the fundamental flaws in our methodology, by aggregating large number of rounds and explicitly calling out and considering the skew in our data, we believe the metrics this tool produces are better than no analysis. Have suggestions for improving our methodology? Please Reach out!


If you have any interest in learning about the rampant discrimination in United States Debate here are some great articles.
- https://sarahisomcenter.org/blog/2019/11/20/combatting-sexism-in-speech-and-debate-programs
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715996
- https://www.semanticscholar.org/paper/Gender-Disparities-in-Competitive-High-School-New-Tartakovsky/28818fee3ee742cbb88eabb93644ebf8ea8e4370

---
%% ## How can I use this tool?
This project collects judges records, guesses at debaters gender, and gives debate members a simple to use tool.

Debaters can use this tool to answer questions such as:
1. Does this judge vote more often for men than women?
2. What is the probability that this biases is the result of chance (what is the p-value)?
3. Out of a pool of judges, which should I whitelist and which should I blacklist?
4. What statistical evidence can I use to connect a Fem K to a particular league or tournament?

For tournament and leauge organisers, this tool can answer questions like:
1. Which judges in the league should I provide anti-bias training to?
2. Which judges should I hire/not hire?
3. If a debaeter comes foward with accusations of bias, can I strengthen their case with data?
4. Which debate tournaments should receive greater/lesser funding?
5. How does our league's structural sexism compare with nearby leagues?

For coaches this tool can answer questions like:
1. Which tournaments should I take my team to?
2. Which coaches should I hire? %%

## Shortcomings

- **Flawed Gender Methodology**: 
	- See above.
- **Garbage In, Garbage Out**: 
	- Because the API over-represents names from western countries. Debate rounds that include names less common in western countries may be more likely to be thrown out. Meaning intersectional bias will be underestimated by this tool.
- **It's Just a Number**: 
	- This is not meant to devalue your experiences with a judge. 
	- A failure to reject the null hypothesis has no meaning. In other words just because this tool does not identify bias does not mean that there is no bias. 
	- Technology is not the solution to rampant discrimination in debate. 
	- Who we demand proof from before we value their experiences and perception is colored by bias and historic power structures. 
	- This tool is simply meant to add another tool to those who are pushing the hard conversations
- **It's Not Intuitive to Interpret Probability**: 
	- While it is reasonable to consider a P-value of 0.05 the threshold for signs of statistically significant discrimination. If you repetitively ran this test on only 20 perfectly unbiased judges, you would expect to see (on average) one incorrectly identified as biased (See the family-wise error rate). 
	- Similarly, It is tempting to incorrectly assign a causal claim to a correlational analysis. This statistical analysis doesn't identify where the bias comes from. Perhaps the education system or social norms better equip one group to excel in debate. A judge who always votes for the better debater may consistently vote for the better prepared group causing a bias to appear in their voting record through no "fault" of the judge.
	- This tool works best when focusing on tournaments and leagues, rather than individual judges so more rounds are considered in each analysis. 
	- This tool should not be miss-used by trawling through hundreds of judges to find a handful with weak statistical significance as these are likely false positives. If you wish to check many judges, lower your significance threshold or find the family-wise error rate. Better yet, don't run many statistical tests and instead come with a specific hypothesis about a single or handful of judges.

## Index of Files

TODO

## How to run this project?

TODO
- Start up SQL database
- Launch Streamlit App