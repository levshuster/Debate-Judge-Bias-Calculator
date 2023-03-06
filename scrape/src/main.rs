use std::{io::Write};

use chrono::{FixedOffset, TimeZone, NaiveDate};
use reqwest::blocking::Client;
use regex::Regex;
mod structs;
mod api_and_storage;
use structs::{Judge, Paradigm, GenderType, Gender, Age, Round, Team, Debater};
use api_and_storage::get_gender;
use table_extract::Row;

// Next Step: get_round_from_html()

fn main() -> Result<(), reqwest::Error> {
	println!("judge = {:}", get_paradim_html_from_judge_id(105729)?
		.get_judge_struct()?
		.to_string());

	Ok(())
}

fn get_paradim_html_from_judge_id(judge_id: u32)-> Result<HtmlUrlPair, reqwest::Error> {
	get_html_from_url(&format!("https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={}", judge_id))
}

fn get_html_from_url(url: &str) -> Result<HtmlUrlPair, reqwest::Error> {
	let response = Client::new().get(url).send()?;
	let body = response.text()?;
	Ok(HtmlUrlPair {
		html: body,
		url: url.to_string(),
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

fn get_age_struct_from_paradim_html(html: String) -> Age {
	get_age_from_name(html)
}

fn get_age_from_name(name: String) -> Age {
	Age {
		confidance: 0.0,
		get: 0
	}
}

fn get_record_from_paradim_html(html: String) -> Vec<Round> {
	// make the map multithreaded
	table_extract::Table::find_first(&html)
		.unwrap()
		.iter()
		.map(|row| get_round_from_row(row))
		.collect::<Vec<Round>>()
}

fn get_round_from_row(row: Row) -> Round {
	
	let level = row.get("Lv").unwrap_or("Unknown Level");
	let event_format = row.get("Ev").unwrap_or("Unknown Event");
	let vote = row.get("Vote").unwrap_or("Unknown Vote");
	let result = row.get("Result").unwrap_or("Unknown Result");	

	let tournament = row.get("Tournament").unwrap_or("Unknown Tournament");
	let tournament_name = Regex::new(r#"<.*?>(.*?)</.*?>"#)
		.unwrap()
		.captures(tournament)
		.unwrap()
		.get(1)
		.unwrap()
		.as_str();

	let date_str = row.get("Date").unwrap_or("Unknown Date");
	let date = Regex::new(r"\d{4}-\d{2}-\d{2}")
		.unwrap()
		.captures(date_str)
		.unwrap()
		.get(0)
		.unwrap()
		.as_str();
	
	let event_round = row.get("Rd").unwrap_or("Unknown Round");
	let round = Regex::new(r#"<a.*?>(.*?)</a>"#)
		.unwrap()
		.captures(event_round)
		.unwrap()
		.get(1)
		.unwrap()
		.as_str()
		.trim();
	
	let team = [row.get("Aff").unwrap_or("Unknown Aff"), row.get("Neg").unwrap_or("Unknown Neg")];
	let urls: Vec<_> = team
		.iter()
		.map(|s| "https://www.tabroom.com".to_string() + Regex::new(r#"href="([^"]+)""#)
			.unwrap()
			.captures(s)
			.unwrap()
			.get(1)
			.unwrap()
			.as_str())
		.collect();
	
	print!("-------working on round {} round {}-------\r", tournament_name, round);
	std::io::stdout().flush().unwrap(); // flush the output to ensure it's printed immediately
	
	Round {
		judge: None,
		tournament_name: tournament_name.to_string(),
		level: structs::Level::match_string(level),
		date: NaiveDate::parse_from_str(date, "%Y-%m-%d").unwrap(),
		event_format: structs::EventFormat::Unknown,
		event_division: structs::EventDivision::match_string(event_format),
		event_round: structs::EventRound::match_string(round),
		aff: get_html_from_url(&urls[0]).unwrap().get_team_struct(),
		neg: get_html_from_url(&urls[1]).unwrap().get_team_struct(),
		vote: get_vote_from_html(vote.to_string()),
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