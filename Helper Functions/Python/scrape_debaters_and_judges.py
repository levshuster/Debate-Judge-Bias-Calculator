import requests
import re
from bs4 import BeautifulSoup

def get_debater_and_team_from_url(url):
	html_content = requests.get(url).content
	soup = BeautifulSoup(html_content, 'html.parser')

	debater_info = soup.find('span', class_='twothirds nospace')
	debater_names = debater_info.find('h4', class_='nospace semibold').text.strip()
	team_name = debater_info.find('h6', class_='full nospace martop semibold bluetext').text.strip()

	debater_names = re.split(r'\s+&\s+', debater_names)
	team_name =(
		' '
		.join(team_name.split())
		.split(':')[0] # If team name is SCHOOL: DEBATER, DEBATER then return SCHOOL
		.split(debater_names[0])[0] # If team name is SCHOOL: FIRST DEBATER FIRST NAME... return SCHOOL
		.split(debater_names[1])[0] # If team name is SCHOOL: SECOND DEBATER FIRST NAME... return SCHOOL
		.split(debater_names[0].split()[-1])[0]  # if team name is SCHOOL: LAST NAME... return school
	)
	return debater_names, team_name

# get_debater_and_team_from_url(url)
