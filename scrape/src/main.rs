use chrono::DateTime;
use reqwest::blocking::Client;
mod structs;
use structs::{Judge, Paradigm, GenderType, Gender, Age, Round, Team, Debater};



fn main() -> Result<(), reqwest::Error> {
	let html_and_url = get_paradim_html_from_judge_id(105729)?;
	// todo: check if raw_html is an error and stop exicution instead of using ?
	let judge = get_judge_struct_from_paradim_html(html_and_url[0].clone(), html_and_url[1].clone())?;
	println!("judge = {:?}", judge.to_string());
	Ok(())
}


fn get_paradim_html_from_judge_id(judge_id: u32)-> Result<Vec<String>, reqwest::Error> {
	let url = format!("https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={}", judge_id);
	// let client = Client::new();
	let response = Client::new().get(&url).send()?;
	let body = response.text()?;
	// println!("body = {:?}", body);
	Ok(vec![body, url])
}

fn get_judge_struct_from_paradim_html(html: String, url: String) -> Result<Judge, reqwest::Error> {
	
	let judge = Judge {
		name: get_name_from_paradim_html(html.clone())?,
		paradigm: get_paradim_struct_from_paradim_html(html.clone()),
		gender: get_gender_from_paradim_html(html.clone()),
		age: get_age_struct_from_paradim_html(html.clone()),
		url: url,
		record: get_record_from_paradim_html(html.clone()),
	};
	Ok(judge)
}

fn get_name_from_paradim_html(html: String) -> Result<String, reqwest::Error> {
	// let name = html.split("Judge: ").collect::<Vec<&str>>()[1].split("</h1>").collect::<Vec<&str>>()[0].to_string();
	let name = "lev shuster".to_string();
	Ok(name)
}

fn get_paradim_struct_from_paradim_html(html: String) -> Paradigm {
	let test_date = DateTime::parse_from_rfc3339("2020-01-01T00:00:00Z").unwrap();
	Paradigm {
		last_updated: test_date,
		text: "Filler Text for Paradigm".to_string(),
	}
}

fn get_gender_from_paradim_html(html: String) -> Gender {
	Gender {
		confidance: 1.0,
		get: GenderType::Male
	}
}

fn get_age_struct_from_paradim_html(html: String) -> Age {
	Age {
		confidance: 1.0,
		get: 18
	}
}

fn get_record_from_paradim_html(html: String) -> Vec<Round> {
	let round_html = "Filler Round HTML".to_string();
	let aff_url = "FIller aff url".to_string();
	let neg_url = "Filler neg url".to_string();
	
	let example_round = Round {
		judge: None,
		tournament_name: "Filler Tournament".to_string(),
		level: structs::Level::HighSchool,
		date: DateTime::parse_from_rfc3339("2020-01-01T00:00:00Z").unwrap(),
		event_format: structs::EventFormat::Policy,
		event_division: structs::EventDivision::Varsity,
		event_round: structs::EventRound::Finals,
		aff: get_team_from_html(aff_url),
		neg: get_team_from_html(neg_url),
		vote: get_vote_from_html(round_html.clone()),
	};
	
	vec![example_round] //multithread each round
}

fn get_team_from_html(url: String) -> Team{
	let team_html = "Filler Team HTML".to_string();
	let debaters = Debater{
		name: "Lev Shuster".to_string(),
		gender: Gender {
			confidance: 1.0,
			get: GenderType::Male
		}
	};
	
	Team {
		debaters: vec![debaters]
	}
}

fn get_vote_from_html(html: String) -> structs::Vote {
	structs::Vote {
		aff: 1,
		neg: 0,
		tie: 0,
		unknown: 0,
	}
}