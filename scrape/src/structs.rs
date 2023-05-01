use std::{fs::File, io::{BufReader}};

use chrono::{DateTime, NaiveDate};
use serde::{Serialize, Deserialize};
use serde_json::to_writer; //, NaiveDate, NaiveDateTime, NaiveTime};

#[derive(Serialize, Deserialize)]
pub struct Paradigm {
	pub(crate) last_updated: DateTime<chrono::FixedOffset>,
	pub(crate) text: String,
}
impl Paradigm {
	fn to_string(&self) -> String {
		format!("Last Updated: {}\t\tText: {}", self.last_updated, self.text)
	}
}

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub enum GenderType {
	Male,
	Female,
	Nonbinary,
	Unknown,
}
// create a Gender type with a confidance float and a get which is an enum of "male, female, nonbinary, unknow  
#[derive(Clone, Serialize, Deserialize)]
pub struct Gender {
	pub(crate) confidance: f32,
	pub(crate) get: GenderType,
}
impl Gender{
	fn to_string(&self) -> String {
		format!("Confidance: {}\t\tGender: {:?}", self.confidance, self.get)
	}
}

#[derive(Serialize, Deserialize)]
pub struct Age {
	pub(crate) confidance: f32,
	pub(crate) get: u32,
}
impl Age {
	fn to_string(&self) -> String {
		format!("Confidance: {}\t\tAge: {}", self.confidance, self.get)
	}
}

#[derive(Serialize, Deserialize, Debug)]
pub enum Level {
	HighSchool,
	MiddleSchool,
	College,
}
impl Level {
	pub(crate) fn match_string(string: &str) -> Level {
		match string {
			"HS" => Level::HighSchool,
			"MS" => Level::MiddleSchool,
			"C" => Level::College,
			_ => panic!("Invalid level: {}", string),
		}
	}
}

#[derive(Serialize, Deserialize, Debug)]
pub enum EventFormat {
	_Policy,
	_LincolnDouglas,
	_PublicForum,
	Unknown,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum EventDivision {
	Varsity,
	JuniorVarsity,
	Novice,
	Unknown,
}
impl EventDivision {
	pub(crate) fn match_string(string: &str) -> EventDivision {
		match string {
			"Varsity" => EventDivision::Varsity,
			"V" => EventDivision::Varsity,
			"JV" => EventDivision::JuniorVarsity,
			s if s.contains("Nov") => EventDivision::Novice,
			_ => EventDivision::Unknown,
		}
	}
}

#[derive(Serialize, Deserialize, Debug)]
pub enum EventRound {
	Custom(u32),
	Octofinals,
	Quarterfinals,
	Semifinals,
	Finals,
	Unknown,
}

impl EventRound {
	pub(crate) fn match_string(string: &str) -> EventRound {
		match string {
			"Octas" => EventRound::Octofinals,
			"Quarterfinals" => EventRound::Quarterfinals,
			"Semifinals" => EventRound::Semifinals,
			"Finals" => EventRound::Finals,
			_ => {
				if string.contains("R") {
					let num_str = &string[1..];
					match num_str.parse::<u32>() {
						Ok(num) => EventRound::Custom(num),
						Err(_) => EventRound::Unknown,
					}
					// let num = num_str.parse::<u32>().unwrap();
					// EventRound::Custom(num)
				} else {
					EventRound::Unknown
				}
			},
		}
	}
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Team {
	pub(crate) debaters: Vec<Debater>,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Debater {
	pub(crate) name: String,
	// school: String,
	pub(crate) gender: Gender
}

#[derive(Debug)]
pub enum VoteResult {
	Aff,
	Neg,
	Tie,
	Unknown,
}
// a vote can be simplified to a single VoteResult, most rounds will have a single value in either aff or neg but pannel rounds could have multiple votes spread over the options
#[derive(Serialize, Deserialize, Default)]
pub struct Vote {
	pub(crate) aff: u32,
	pub(crate) neg: u32,
	pub(crate) tie: u32,
	pub(crate) unknown: u32,
}


#[derive(Serialize, Deserialize)]
pub struct Round {
	pub(crate) judge: Option<Judge>,
	pub(crate) tournament_name: String,
	pub(crate) level: Level,
	pub(crate) date: NaiveDate,
	pub(crate) event_format: EventFormat,
	pub(crate) event_division: EventDivision,
	pub(crate) event_round: EventRound,
	pub(crate) aff: Team,
	pub(crate) neg: Team,
	pub(crate) vote: Vote,
}
impl Round {
	pub fn to_string(&self) -> String {
		let mut string = String::new();
		string.push_str(&format!("Tournament Name: {}", self.tournament_name));
		string.push_str(&format!("\tLevel: {:?}", self.level));
		string.push_str(&format!("\tDate: {}", self.date));
		string.push_str(&format!("\tEvent Format: {:?}", self.event_format));
		string.push_str(&format!("\tEvent Division: {:?}", self.event_division));
		string.push_str(&format!("\tEvent Round: {:?}", self.event_round));
		string.push_str(&format!("\n\tAff:"));
		for debater in &self.aff.debaters {string.push_str(&format!("\n\t\t{}-{}", debater.name, debater.gender.to_string()));}
		string.push_str(&format!("\n\tNeg:"));
		for debater in &self.neg.debaters {string.push_str(&format!("\n\t\t{}-{}", debater.name, debater.gender.to_string()));}
		string.push_str(&format!("\tVote:"));
		string.push_str(&format!("\t\tAff: {}", self.vote.aff));
		string.push_str(&format!("\t\tNeg: {}", self.vote.neg));
		string.push_str(&format!("\t\tTie: {}", self.vote.tie));
		string.push_str(&format!("\t\tUnknown: {}", self.vote.unknown));
		string
	}
	fn to_string_short(&self) -> String {
		let mut string = String::new();
		string.push_str(&format!("\t{}", self.tournament_name));
		string.push_str(&format!("\t{:?}", self.level));
		string.push_str(&format!("\t{}", self.date));
		string.push_str(&format!("\t{:?}", self.event_format));
		string.push_str(&format!("\t{:?}", self.event_division));
		string.push_str(&format!("\t{:?}", self.event_round));
		string
	}
}

#[derive(Serialize, Deserialize)]
pub struct Judge {
	pub(crate) name: String,
	pub(crate) paradigm: Paradigm,
	pub(crate) gender: Gender,
	pub(crate) age: Age,
	pub(crate) url: String,
	pub(crate) record: Vec<Round>,
}

impl Judge {
	pub fn to_string(&self, is_short: bool) -> String {
		let mut string = String::new();
		string.push_str(&format!("\n\tName: {} ", self.name));
		string.push_str(&format!("\n\tParadim: {:?}...", self.paradigm.to_string().chars().take(100).collect::<String>()));
		string.push_str(&format!("\n\tGender: {}", self.gender.to_string()));
		string.push_str(&format!("\n\tAge: {}", self.age.to_string()));
		string.push_str(&format!("\n\tURL: {}", self.url));
		for round in &self.record {string.push_str(&format!("\n{}", if is_short {round.to_string_short()} else {round.to_string()}));}
		string
	}
	pub fn to_json_file(&self) -> &Judge {
		let file = File::create(format!("Judge {}.json", self.name)).unwrap();
		to_writer(&file, self).unwrap();
		// file.write_all(self.to_string().as_bytes()).unwrap();
		self
	}
	pub fn read_from_json_file(name: &str) -> Judge {
		// let mut file = File::open(format!("{}_judge.json", name)).unwrap();
		// let judge: Judge = from_reader(&file).unwrap();
		
		
		let reader = BufReader::new(File::open(format!("Judge {}.json", name)).unwrap());
		let judge: Judge = serde_json::from_reader(reader).unwrap();
		judge
		// let mut contents = String::new();
		// file.read_to_string(&mut contents).unwrap();
		// let judge: Judge = serde_json::from_str(&contents).unwrap();
		// judge
	}
}