use chrono::{DateTime};//, NaiveDate, NaiveDateTime, NaiveTime};

pub struct Paradigm {
	pub(crate) last_updated: DateTime<chrono::FixedOffset>,
	pub(crate) text: String,
}
impl Paradigm {
	fn to_string(&self) -> String {
		format!("Last Updated: {}\t\tText: {}", self.last_updated, self.text)
	}
}

#[derive(Debug)]
pub enum GenderType {
	Male,
	Female,
	Nonbinary,
	Unknown,
}
// create a Gender type with a confidance float and a get which is an enum of "male, female, nonbinary, unknow  
pub struct Gender {
	pub(crate) confidance: f32,
	pub(crate) get: GenderType,
}
impl Gender{
	fn to_string(&self) -> String {
		format!("Confidance: {}\t\tGender: {:?}", self.confidance, self.get)
	}
}

pub struct Age {
	pub(crate) confidance: f32,
	pub(crate) get: u32,
}
impl Age {
	fn to_string(&self) -> String {
		format!("Confidance: {}\t\tAge: {}", self.confidance, self.get)
	}
}

#[derive(Debug)]
pub enum Level {
	HighSchool,
	MiddleSchool,
	College,
}

#[derive(Debug)]
pub enum EventFormat {
	Policy,
	LincolnDouglas,
	PublicForum,
	Unknown,
}

#[derive(Debug)]
pub enum EventDivision {
	Varsity,
	JuniorVarsity,
	Novice,
	Unknown,
}

#[derive(Debug)]
pub enum EventRound {
	Custom(u32),
	Octofinals,
	Quarterfinals,
	Semifinals,
	Finals,
	Unknown,
}

pub struct Team {
	pub(crate) debaters: Vec<Debater>,
}

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
pub struct Vote {
	pub(crate) aff: u32,
	pub(crate) neg: u32,
	pub(crate) tie: u32,
	pub(crate) unknown: u32,
}



pub struct Round {
	pub(crate) judge: Option<Judge>,
	pub(crate) tournament_name: String,
	pub(crate) level: Level,
	pub(crate) date: DateTime<chrono::FixedOffset>,
	pub(crate) event_format: EventFormat,
	pub(crate) event_division: EventDivision,
	pub(crate) event_round: EventRound,
	pub(crate) aff: Team,
	pub(crate) neg: Team,
	pub(crate) vote: Vote,
}
impl Round {
	fn to_string(&self) -> String {
		let mut string = String::new();
		string.push_str(&format!("\tTournament Name: {}", self.tournament_name));
		string.push_str(&format!("\tLevel: {:?}", self.level));
		string.push_str(&format!("\tDate: {}", self.date));
		string.push_str(&format!("\tEvent Format: {:?}", self.event_format));
		string.push_str(&format!("\tEvent Division: {:?}", self.event_division));
		string.push_str(&format!("\tEvent Round: {:?}", self.event_round));
		string.push_str(&format!("\tAff:"));
		for debater in &self.aff.debaters {
			string.push_str(&format!("\n\t\t{}", debater.name));
		}
		string.push_str(&format!("\tNeg:"));
		for debater in &self.neg.debaters {
			string.push_str(&format!("\n\t\t{}", debater.name));
		}
		string.push_str(&format!("\tVote:"));
		string.push_str(&format!("\t\tAff: {}", self.vote.aff));
		string.push_str(&format!("\t\tNeg: {}", self.vote.neg));
		string.push_str(&format!("\t\tTie: {}", self.vote.tie));
		string.push_str(&format!("\t\tUnknown: {}", self.vote.unknown));
		string
	}
}

pub struct Judge {
	pub(crate) name: String,
	pub(crate) paradigm: Paradigm,
	pub(crate) gender: Gender,
	pub(crate) age: Age,
	pub(crate) url: String,
	pub(crate) record: Vec<Round>,
}

impl Judge {
	pub fn to_string(&self) -> String {
		// create a string a usfin the to_string method of each struct
		let mut string = String::new();
		string.push_str(&format!("\n\tName: {} ", self.name));
		string.push_str(&format!("\n\tParadim: {} ", self.paradigm.to_string()));
		string.push_str(&format!("\n\tGender: {}", self.gender.to_string()));
		string.push_str(&format!("\n\tAge: {}", self.age.to_string()));
		string.push_str(&format!("\n\tURL: {}", self.url));
		// for each round in recored call the to_string method and add it to the string
		for round in &self.record {
			string.push_str(&format!("\n\t\t{}", round.to_string()));
		}
		string
	}
}