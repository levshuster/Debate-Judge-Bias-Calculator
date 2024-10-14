import requests
import re
from bs4 import BeautifulSoup
from collections import namedtuple


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

def get_votes_and_speaker_points_for_a_tournament_from_judge_url(url):
	Vote = namedtuple("Vote", ['judge_id', 'team_link', 'division_id', 'tourn_id', 'won', 'side'])
	Speaker_Points = namedtuple("Speaker_Points", ['judge_id', 'team_link', 'name', 'division_id', 'tourn_id', 'points'])
	votes, speaker_points = [], []

	judge_id,tourn_id = url.split("judge_id=")[-1].split('&tourn_id=')

	response = requests.get(url)

	# judge = get_judge_info()

	soup = BeautifulSoup(response.content, 'html.parser')
	rows = soup.find_all('tr', class_='row smallish')

	for row in rows:
		columns = row.find_all('td')

		division_link, team_link = ['https://www.tabroom.com/index/tourn/postings/'+link['href'] for link in row.find_all('a', href=True)]
		division_id = division_link.split("round_id=")[-1].split('&')[0]
		result = columns[3].text.strip().lower()
		won = 'w' in result
		assert(won or 'l' in result)

		votes.append(Vote(
			judge_id=judge_id,
			team_link=team_link,
			division_id=division_id,
			tourn_id=tourn_id,
			won=won,
			side=columns[1].text.strip().lower()
		))

		names_and_points = [col.get_text(strip=True).lower() for col in columns[4:]]
		for name, points in zip(names_and_points[::2], names_and_points[1::2]):
			speaker_points.append(Speaker_Points(
				judge_id=judge_id,
				team_link=team_link,
				name=name,
				division_id=division_id,
				tourn_id=tourn_id,
				points=points
			))
	return votes, speaker_points

# votes, speaker_points = get_votes_and_speaker_points_for_a_tournament_from_judge_url('https://www.tabroom.com/index/tourn/postings/judge.mhtml?judge_id=1985775&tourn_id=26620')
# for vote in votes: print(vote)
# for points in speaker_points: print(points)
