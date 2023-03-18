use clap::{Args, Parser, Subcommand};


#[derive(Debug, Parser)]
#[clap(version = "0.0", author = "Lev Shuster", about = "A tool for Identifying probabamatic debate judges based on their tabroom records")]
pub struct Opts {
	/// Search tabroom to collect data
	#[clap(subcommand)]
	pub data_life_cycle: DataLifeCycle,
	
	// /// Analyze a previously generated judge file
	// #[clap(subcommand)]
	// pub analyze: Analyze,
	
	// /// View a previously generated judge file
	// #[clap(subcommand)]
	// pub view: View,
}

#[derive(Debug, Subcommand)]
pub enum DataLifeCycle {
	/// Search tabroom to collect data
	Generate(Generate),
	
	/// Analyze a previously generated judge file
	Analyze(Analyze),
	
	/// View a previously generated judge file
	View(View),
	
	/// Delete a previously generated judge file
	Delete(Delete),
}

#[derive(Debug, Args)]
pub struct View {
	/// What type of data to generate
	#[clap(subcommand)]
	pub view_type: Type,
}

#[derive(Debug, Args)]
pub struct Analyze {
	/// What type of analysis to perform
	#[clap(subcommand)]
	pub analyze_Type: AnalyzeType,
}

#[derive(Debug, Subcommand)]
pub enum AnalyzeType {
	/// Interegate a judge
	Judge(AnalyzeJudge),
	
	/// Interegate a list of judges
	Judges(AnalyzeJudges),
	
	/// Interegate a tournament
	Tournament(AnalyzeTournament),
} 

#[derive(Debug, Args)]
pub struct AnalyzeJudges {
	/// Search tab room for a judge with a matching first and last name
	#[arg(short, long)]
	name:bool,
	
	/// Scrapes judge information given a 
	#[arg(short, long)]
	id: bool,
	
	/// Specify that the file format the program must parse is a csv 
	#[arg(long)]
	csv: Option<bool>,
	
	/// Specify that the file format the program must parse is a json
	#[arg(long)]
	json: Option<bool>,
	
	/// Specify that the file format the program must parse is a txt
	#[arg(long)]
	txt: Option<bool>,
	
	/// Specify the path to the file that contains the list of judges
	#[arg(short, long, value_name = "FILE")]
	file_path: String,
	
	/// Specify the type of analysis to perform
	#[clap(subcommand)]
	pub analyze_method: AnalyzeMethod,
}


#[derive(Debug, Args)]
pub struct AnalyzeTournament {
	/// Scrapes judge information given a tabroom URL
	#[arg(short, long, value_name = "URL")]
	url: String,
	
	/// Specify the type of analysis to perform
	#[clap(subcommand)]
	pub analyze_method: AnalyzeMethod,
	
}

#[derive(Debug, Args)]
pub struct AnalyzeJudge {
	/// Search tab room for a judge with a matching first and last name
	#[arg(short, long, value_name = "NAME")]
	name: Option<String>,
	
	/// Scrapes judge information given a 
	#[arg(short, long, value_name = "ID")]
	id: Option<u32>,
	
	/// Specify the type of analysis to perform
	#[clap(subcommand)]
	pub analyze_method: AnalyzeMethod,
}

#[derive(Debug, Subcommand)]
pub enum AnalyzeMethod {
	// Interegate judge record to identify patterns in the gender of who the judge facors 
	Gender(AnalyzeGender),
	
	// Interegate judge record to identify patterns in the age of who the judge facors
	Age(AnalyzeGender),
	
	// Interegate judge record to identify patterns in how the judge votes on specific topics or debate formats
	Voting(AnalyzeVoting),
}

#[derive(Debug, Args)]
pub struct AnalyzeGender {
	/// Specify the type of analysis to perform
	#[clap(subcommand)]
	pub analyze_method: AnalyzeGenderMethod,
}

#[derive(Debug, Subcommand)]
pub enum AnalyzeGenderMethod {
	Distribution,
	VotintPatterns,
	Overview,
}

#[derive(Debug, Args)]
pub struct AnalyzeVoting {
	/// Specify the type of analysis to perform
	#[clap(subcommand)]
	pub analyze_method: AnalyzeVotingMethod,
}

#[derive(Debug, Subcommand)]
pub enum AnalyzeVotingMethod {
	/// Interegate judge record to identify patterns in how the judge votes on specific topics
	Topic,
	
	/// Interegate judge record to identify patterns in how the judge votes on specific debate formats
	Format,
}



#[derive(Debug, Args)]
pub struct Delete {
	/// What type content to delete
	#[clap(subcommand)]
	pub analyze_Type: Type,
}


#[derive(Debug, Args)]
pub struct Generate {
	/// What type of data to collect
	#[clap(subcommand)]
	pub scrape_type: Type,
}

#[derive(Debug, Subcommand)]
pub enum Type {
	/// Collect data on a single judge
	Judge(Judge),
	
	/// Collect data on a list of judges
	Judges(Judges),
	
	/// Collect data on a tournament
	Tournament(Tournament),
}

#[derive(Debug, Args)]
pub struct Judge {
	/// Search tab room for a judge with a matching first and last name
	#[arg(short, long, value_name = "NAME")]
	name: Option<String>,
	
	/// Scrapes judge information given a 
	#[arg(short, long, value_name = "ID")]
	id: Option<u32>,
}

#[derive(Debug, Args)]
pub struct Judges {
	/// Search tab room for a judge with a matching first and last name
	#[arg(short, long)]
	name:bool,
	
	/// Scrapes judge information given a 
	#[arg(short, long)]
	id: bool,
	
	/// Specify that the file format the program must parse is a csv 
	#[arg(long)]
	csv: Option<bool>,
	
	/// Specify that the file format the program must parse is a json
	#[arg(long)]
	json: Option<bool>,
	
	/// Specify that the file format the program must parse is a txt
	#[arg(long)]
	txt: Option<bool>,
	
	/// Specify the path to the file that contains the list of judges
	#[arg(short, long, value_name = "FILE")]
	file_path: String,
}


#[derive(Debug, Args)]
pub struct Tournament {
	/// Scrapes judge information given a tabroom URL
	#[arg(short, long, value_name = "URL")]
	url: String,
}