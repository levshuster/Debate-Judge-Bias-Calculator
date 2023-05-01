# Debate-Judge-Bias-Calculator: Desktop program that aims to measure signs of debate judge bias from tabroom records.

## Introduction

After spendingsix years in competitive academic debate as a judge, team captain, and competitor I have found unique role of the Debate Judge facination. One of the unique things about debate is the role of a judge. In the wider world, judges apply rules, but in debate, the judge's only job is to decides who is more convincing. This introduces a huge amount of freedom to the judge. With this freedom comes a huge amount of room for bias in the judge’s decision. Because of the deeply personal nature of debate and the judge's freedom, coaches exspect to hear angered students accuse judges of bias. Because of the frequency coaches often dismiss or ignore these acusations. Debate aboslutle has a bias problem. This tool's goal is to aid debaters when they make claims and help coaches sort through the noise.

A benifit of moving from paper to a central tournaments managment software is the often decade long public record of every round a judge has prosided over. There are no tools to help debaters sort through this data because the data is relitively unhelpful in making future decisions (only including dividion, format, result, and the debaters' names). In 2021 I stumbled across an API that takes a name and returns the name's gender and condidance rating. While haldly a exact tool, by applying the API to guess at debater's genders, I can provide usful insights towards judges', tournaments', and leages', gender biases.

If you have any interest in learning about the rampant discrimination in United States Debate here are some great articles. 
TLDR: there is a disgusting amount of sexism in debate which causes women to be forced out of the activity at depressing rates. There has been quantitative research on the effect of sexism but no substantial work on the effect and existance of discriminatory Judges within the activity.
- https://sarahisomcenter.org/blog/2019/11/20/combatting-sexism-in-speech-and-debate-programs
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715996
- https://www.semanticscholar.org/paper/Gender-Disparities-in-Competitive-High-School-New-Tartakovsky/28818fee3ee742cbb88eabb93644ebf8ea8e4370

---
## How can I use this tool?
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
2. Which coaches should I hire?

## How to Quantify Discrimination?

Consider a Policy debate round (two teams of two debaters):

1. Each debater's name is looked up, if the confidance level is lower than the cutoff, the process stops and this round doesn't effect the judge's bias rating.
2. For each woman who wins the round, the rounds score increments
3. For each woman who loses the round, the round score decrements
4. For each man who wins the round, the round score decrements
5. For each man who loses the round, the round score decrements

This leaves a round score between -4 and 4

This same method works for any debate format with any number of debaters (Lincon Douglas ranges from 2 to -2).

A judge's bias rating is the sum of all of their round scores

### What does this look like?
- If two men win against two men, the round score is 0 (-1 + -1 + 1 + 1)
- If two women win against two women, the round score is 0 (1 + 1 + -1 + -1)
- If a man and a woman win against a man and a women, the round score is 0 (-1 + 1 + 1 + -1)
- If a man and a woman win agains a man and a person of unknown gender, the round score is 0 (if a name's gender confidance doesn't meet the threshold the entire round has no impact on the judge's bias rating) 
- If two men win against two women, the score is -4 (-1 + -1 + -1 + -1)
- If two women win against two men, the score is 4 (1 + 1 + 1 + 1)
- If two women win against a man and a woman, the score is 2 (1 + 1 + 1 + -1)

Consider the following Judge record:
|  | Aff Team | Neg Team | Winning Team | Round Score |
| --- | --- | --- | --- | --- |
| Round 1 | Male/Female | Female/Female | Neg | 2
| Round 2 | Male/Female | Female/Female | Aff | -2
| Round 3 | Female/Female | Male/Male | Neg | -4
| Round 4 | Male/Male | Male/Male | Aff | 0
| Round 5 | Female/Male | Male/Male | Neg | -2

This judge's bias rating is -6 which shows a preference for voting for men.

However with a p-value of 0.3, this preference is not significant (this could be explained by chance) so no conclusions can be make about the judge's bias.

## Shortcommings

- Doesn't count nonbinary people: Gender neutral names will be thrown out meaning that this tool has no chance of identifying bias against nonbinary people.

- Garbage in, garbage out: If the API is based on data from western countries, debate rounds that include names less common in western countries are more likely to be thrown out. Meaning intersectional bias will be underestimated by this tool.

- It's just a number: This tool doesn't devalue personal exsperences with a judge. This tool is meant to be used in conjunction with other evidence to make a case for bias. There is a hunderd ways for a judge to be biased without it showing up on this one particular measure. 

- It's all probability: When you consider 10,000 bias free judges, we would exspect 500 judges to have a p-value of 0.05 or less showing bias. This tool works best when focusing on tournaments and leauges, rather than individual judges. The larger the number of rounds considered, the more likely it is that a judge's bias rating is to reflect reality.

## Timeline
TODO: write timeline

## Index of Files
TODO: link to scrape readme

## How to run this project?
1. Install Rust: https://www.rust-lang.org/tools/install

2. Install this git repo: `git clone https://github.com/levshuster/Debate-Judge-Bias-Calculator.git`

3. Run the project by navigating to the src folder and entering `cargo run `