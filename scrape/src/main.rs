use chrono::{DateTime, FixedOffset, TimeZone};
use reqwest::blocking::Client;
use regex::Regex;
mod structs;
use structs::{Judge, Paradigm, GenderType, Gender, Age, Round, Team, Debater};



fn main() -> Result<(), reqwest::Error> {
	println!("judge = {:}", get_paradim_html_from_judge_id(105729)?
		.get_judge_struct()?
		.to_string());
	Ok(())
}

fn get_paradim_html_from_judge_id(judge_id: u32)-> Result<HtmlUrlPair, reqwest::Error> {
	let url = format!("https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={}", judge_id);
	// let client = Client::new();
	let response = Client::new().get(&url).send()?;
	let body = response.text()?;
	// println!("body = {:?}", body);
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
		let judge = Judge {
			name: get_name_from_paradim_html(self.html.clone())?,
			paradigm: get_paradim_struct_from_paradim_html(self.html.clone()),
			gender: get_gender_from_paradim_html(self.html.clone()),
			age: get_age_struct_from_paradim_html(self.html.clone()),
			url: self.url.clone(),
			record: get_record_from_paradim_html(self.html.clone()),
		};
		Ok(judge)
	}
}




fn get_name_from_paradim_html(html: String) -> Result<String, reqwest::Error> {
	let name_re = Regex::new(r"<h3>(.*)</h3>").unwrap();
	Ok(name_re.captures(&html).unwrap().get(1).unwrap().as_str().to_string())
}

fn get_paradim_struct_from_paradim_html(html: String) -> Paradigm {
	let paradim = html.split(">\n\t\t\t\t\t<h5>Paradigm Statement</h5>\n\t\t\t\t</span>\n\n\t\t\t\t<span class=\"half rightalign semibold bluetext\">\n\t\t\t\t\t\t")
		.nth(1).unwrap()
		.split("</p>\n\t\t\t</div>\n\t\t</div>\n\n\t<div")
		.nth(0).unwrap().to_string();

	let last_changed = paradim.split("\n")
		.nth(0).unwrap()
		.split("Last changed ")
		.nth(1).unwrap();

	let re = Regex::new(r"<.{0,7}>").unwrap();
	let paradigm = re.replace_all(paradim.split("ltborderbottom\">\n\t\t\t\t<p>")
		.nth(1).unwrap(), "").to_string();
	
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