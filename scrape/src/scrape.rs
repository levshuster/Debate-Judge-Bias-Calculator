use dict_thread_safe_api_and_storage::GetGender;
use rayon::{iter::ParallelIterator, prelude::IntoParallelRefIterator};
use chrono::{FixedOffset, TimeZone, NaiveDate, Utc};
use reqwest::blocking::Client;
use table_extract::Row;
use regex::Regex;


use structs::{Judge, Paradigm, GenderType, Gender, Age, Round, Team, Debater};
use crate::structs;
use crate::dict_thread_safe_api_and_storage;


pub fn get_paradim_html_from_judge_id(judge_id: u32)-> Result<HtmlUrlPair, reqwest::Error> {
	get_html_from_url(&format!("https://www.tabroom.com/index/paradigm.mhtml?judge_person_id={}", judge_id))
}

pub fn get_html_from_url(url: &str) -> Result<HtmlUrlPair, reqwest::Error> {
	let response = Client::new().get(url).send()?;
	let body = response.text()?;
	Ok(HtmlUrlPair {
		html: body,
		url: url.to_string(),
		first_name: None,
		last_name: None,
		result_number: None,
	})
}

pub struct HtmlUrlPair {
	pub(crate) html: String,
	pub(crate) url: String,
	pub(crate) first_name: Option<String>,
	pub(crate) last_name: Option<String>,
	pub(crate) result_number: Option<u32>,
}

impl HtmlUrlPair {
	pub fn get_judge_struct(&self, names:&GetGender) -> Result<Judge, reqwest::Error> {
		let name = get_name_from_paradim_html(self.html.clone())?;
		let name2 = name.clone();
		let judge = Judge {
			name: name,
			paradigm: get_paradim_struct_from_paradim_html(self.html.clone()),
			gender: names.get(name2),
			age: get_age_struct_from_paradim_html(self.html.clone()),
			url: self.to_string(),
			record: get_record_from_paradim_html(self.html.clone(), names),
		};
		Ok(judge)
	}
	fn get_team_struct(&self, names_dict: &GetGender) -> Team{
		let after = "nospace semibold";
		let before = "full nospace martop semibold bluetext";
		if let Some(i) = self.html.find(after) {
			let (_, rest) = self.html.split_at(i + after.len());
			if let Some(j) = rest.find(before) {
				let first = String::from(&rest[..j]);
				if let Some(start_index) = first.find('>') {
					if let Some(end_index) = first[start_index + 1..].find('<') {
						let extracted = &first[start_index + 1..start_index + 1 + end_index];
						let names: Vec<&str> = extracted
							.trim()
							.split("&amp;")
							.map(|name| name.trim())
							.take(10)
							.collect();
						// println!("{:?}", names);
						let debaters:Vec<Debater> = names
							.iter()
							.map(|name| Debater{
								name: name.to_string(),
								gender: names_dict.get(name.to_string())
						})
						.collect();
						return Team {
							debaters: debaters
						}
					}
				}
			}
		}
		let debaters = Debater{
			name: "Unable to Find Name".to_string(),
			gender: Gender {
				confidance: 0.0,
				get: GenderType::Unknown
			}
		};
		
		Team {
			debaters: vec![debaters]
		}
	}
	fn to_string(&self) -> String {
		// if self has a first name and last name then use them
		// else use the url
		if self.first_name.is_some() && self.last_name.is_some() {
			format!("
			Url: {}
			First Name: {}
			Last Name: {}
			Result Number: {}
			", 
			self.url, 
			self.first_name.clone().unwrap(), 
			self.last_name.clone().unwrap(), 
			self.result_number.clone().unwrap())
		} else {
			self.url.clone()
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
		.unwrap_or("No Paradigm Statement Found")
		.split("</p>\n\t\t\t</div>\n\t\t</div>\n\n\t<div")
		.nth(0)
		.unwrap()
		.to_string();

	let last_changed = paradim.split("\n")
		.nth(0)
		.unwrap()
		.split("Last changed ")
		.nth(1)
		.unwrap_or("16 October 2021 3:32 AM PST");

	let re = Regex::new(r"<.{0,7}>").unwrap();
	let paradigm = re
		.replace_all(paradim
			.split("ltborderbottom\">\n\t\t\t\t<p>")
			.nth(1)
			.unwrap_or("no paradim"), "")
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

fn get_age_from_name(_name: String) -> Age {
	Age {
		confidance: 0.0,
		get: 0
	}
}

fn get_record_from_paradim_html(html: String, names: &GetGender) -> Vec<Round> {
	table_extract::Table::find_first(&html)
		.unwrap()
		.iter()
		.collect::<Vec<_>>()
		.par_iter()
		.map(|row| get_round_from_row(*row, names))
		.collect::<Vec<Round>>()
}

fn get_round_from_row(row: Row, names: &GetGender) -> Round {
	
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
	let teams = team
		.par_iter()
		.map(|s| "https://www.tabroom.com".to_string() + Regex::new(r#"href="([^"]+)""#)
			.unwrap()
			.captures(s)
			.unwrap()
			.get(1)
			.unwrap()
			.as_str())
		.map(|url| 
			get_html_from_url(&url)
			.unwrap()
			.get_team_struct(names))
		.collect::<Vec<Team>>();
	
	// print!("-------working on round {} round {}-------\r", tournament_name, round);
	// std::io::stdout().flush().unwrap(); // flush the output to ensure it's printed immediately
	
	Round {
		judge: None,
		tournament_name: tournament_name.to_string(),
		level: structs::Level::match_string(level),
		date: NaiveDate::parse_from_str(date, "%Y-%m-%d").unwrap(),
		event_format: structs::EventFormat::Unknown,
		event_division: structs::EventDivision::match_string(event_format),
		event_round: structs::EventRound::match_string(round),
		aff: teams[0].clone(),
		neg: teams[1].clone(),
		vote: get_vote_from_html(vote.to_string(), result.to_string()),
	}
}

fn get_vote_from_html(vote: String, result: String) -> structs::Vote {
	if result == "" {
		return match vote.as_str() {
			"Aff" => structs::Vote { aff: 1, ..Default::default() },
			"Neg" => structs::Vote { neg: 1, ..Default::default() },
			_ => structs::Vote { unknown: 1, ..Default::default() }
		}
	}
	
	let binding = result.chars().rev().collect::<String>();
	structs::Vote {
		aff: binding
			.chars()
			.nth(2)
			.unwrap()
			.to_digit(10)
			.unwrap(),
		neg: binding
			.chars()
			.nth(0)
			.unwrap()
			.to_digit(10)
			.unwrap(),
		..Default::default()
	}
}