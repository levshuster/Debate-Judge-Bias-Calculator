use chrono::{DateTime, FixedOffset, TimeZone};
use reqwest::blocking::Client;
use regex::Regex;
mod structs;
mod api_and_storage;
use structs::{Judge, Paradigm, GenderType, Gender, Age, Round, Team, Debater};
use api_and_storage::get_gender;

fn main() -> Result<(), reqwest::Error> {
	println!("judge = {:}", get_paradim_html_from_judge_id(105729)?
		.get_judge_struct()?
		.to_string());

	Ok(())
}

fn get_paradim_html_from_judge_id(judge_id: u32)-> Result<HtmlUrlPair, reqwest::Error> {
	get_html_from_url(format!("https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={}", judge_id))
}

fn get_html_from_url(url: String) -> Result<HtmlUrlPair, reqwest::Error> {
	let response = Client::new().get(&url).send()?;
	let body = response.text()?;
	Ok(HtmlUrlPair {
		html: body,
		url: url,
	})
}

pub struct HtmlUrlPair {
	pub(crate) html: String,
	pub(crate) url: String,
}
impl HtmlUrlPair {
	fn get_judge_struct(&self) -> Result<Judge, reqwest::Error> {
		let name = get_name_from_paradim_html(self.html.clone())?;
		let name2 = name.clone();
		let judge = Judge {
			name: name,
			paradigm: get_paradim_struct_from_paradim_html(self.html.clone()),
			gender: get_gender(name2),
			age: get_age_struct_from_paradim_html(self.html.clone()),
			url: self.url.clone(),
			record: get_record_from_paradim_html(self.html.clone()),
		};
		Ok(judge)
	}
	fn get_team_struct(&self) -> Team{
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
}




fn get_name_from_paradim_html(html: String) -> Result<String, reqwest::Error> {
	let name_re = Regex::new(r"<h3>(.*)</h3>").unwrap();
	Ok(name_re.captures(&html)
		.unwrap()
		.get(1)
		.unwrap()
		.as_str()
		.to_string())
}

fn get_paradim_struct_from_paradim_html(html: String) -> Paradigm {
	let paradim = html.split(">\n\t\t\t\t\t<h5>Paradigm Statement</h5>\n\t\t\t\t</span>\n\n\t\t\t\t<span class=\"half rightalign semibold bluetext\">\n\t\t\t\t\t\t")
		.nth(1)
		.unwrap()
		.split("</p>\n\t\t\t</div>\n\t\t</div>\n\n\t<div")
		.nth(0)
		.unwrap()
		.to_string();

	let last_changed = paradim.split("\n")
		.nth(0)
		.unwrap()
		.split("Last changed ")
		.nth(1)
		.unwrap();

	let re = Regex::new(r"<.{0,7}>").unwrap();
	let paradigm = re
		.replace_all(paradim
			.split("ltborderbottom\">\n\t\t\t\t<p>")
			.nth(1)
			.unwrap(), "")
		.to_string();
	
	// TODO: the end of paradigm is a bunch of junk, so I need to remove it, perhaps one of the split statments isn't working correctly?
	// println!("\n\n\nparadigm = {:?}", paradigm);

	let dt = FixedOffset::west_opt(8 * 3600)
		.unwrap()
		.datetime_from_str(last_changed, "%e %B %Y %l:%M %p %Z")
		.unwrap();
	
	Paradigm {
		last_updated: dt,
		text: paradigm,
	}
}

fn get_gender_from_paradim_html(html: String) -> Gender {
	get_gender("name".to_string())
}

fn get_age_struct_from_paradim_html(html: String) -> Age {
	get_age_from_name("name".to_string())
}

fn get_age_from_name(name: String) -> Age {
	Age {
		confidance: 1.0,
		get: 18
	}
}

fn get_record_from_paradim_html(html: String) -> Vec<Round> {
	let rounds_html = html.split("<div class=\"round\">")
		.map(|x| x.to_string())
		.collect::<Vec<String>>();
	
	// make the map multithreaded
	rounds_html.iter()
		.map(|x| get_round_from_html(x.to_string()))
		.collect::<Vec<Round>>()
}

fn get_round_from_html(round_html: String) -> Round {
	let aff_url = "https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729".to_string();
	let neg_url = "https://www.tabroom.com/index/paradigm.mhtml?judge_person_id=105729".to_string();
	
	Round {
		judge: None,
		tournament_name: "Filler Tournament".to_string(),
		level: structs::Level::HighSchool,
		date: DateTime::parse_from_rfc3339("2020-01-01T00:00:00Z").unwrap(),
		event_format: structs::EventFormat::Policy,
		event_division: structs::EventDivision::Varsity,
		event_round: structs::EventRound::Finals,
		aff: get_html_from_url(aff_url).unwrap().get_team_struct(),
		neg: get_html_from_url(neg_url).unwrap().get_team_struct(),
		vote: get_vote_from_html(round_html.clone()),
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