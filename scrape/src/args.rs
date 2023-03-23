use clap::{Args, Parser, Subcommand, ArgGroup};

use crate::{dict_thread_safe_api_and_storage, search_for_judge, scrape::get_paradim_html_from_judge_id, api_succsess_rate, ballance_votes_for_and_against_women};

#[derive(Debug, Parser)]
#[clap(version = "0.0", author = "Lev Shuster", about = "A tool for Identifying probabamatic debate judges based on their tabroom records")]
pub struct Opts {
	/// Search tabroom to collect data
	#[clap(subcommand)]
	pub data_life_cycle: DataLifeCycle,
	
	// #[clap(short, long, parse(from_occurrences))]
	// verbosity: usize,
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


pub fn parse_cli(){
	let args = Opts::parse();
	match args.data_life_cycle {
		DataLifeCycle::Generate(generate)  => parse_generate(generate),
		DataLifeCycle::Analyze(analyze)  => parse_analyze(analyze),
		DataLifeCycle::View(view)  => parse_view(view),
		DataLifeCycle::Delete(delete)  => parse_delete(delete),
	}
	// println!("args long = {:?}", args.long);
	
}

#[derive(Debug, Args)]
pub struct View {
	/// What type of data to generate
	#[clap(subcommand)]
	pub view_type: ViewType,
	
	/// Shorten the output
	#[arg(short, long)]
	short: bool,
}

#[derive(Debug, Subcommand)]
pub enum ViewType {
	/// Interegate a judge
	Judge(ViewJudge),
	
	/// Interegate a list of judges
	Judges(ViewJudges),
	
	/// Interegate a tournament
	Tournament(ViewTournament),
} 

#[derive(Debug, Args)]
pub struct ViewJudge {
	/// Search local judge .json files with a matching first and last name
	#[arg(short, long, value_name = "NAME")]
	name: String,

}


#[derive(Debug, Args)]
pub struct ViewJudges {
	/// Search local judge .json files with a matching first and last name
	#[arg(short, long)]
	name:bool,
	
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
pub struct ViewTournament {
	/// Scrapes judge information given a tabroom URL
	#[arg(short, long, value_name = "URL")]
	url: String,
	
}


// TODO
fn parse_view(args: View){
	match args.view_type{
		ViewType::Judge(judge) => parse_view_judge(judge, args.short),
		ViewType::Judges(judges) => parse_view_judges(judges, args.short),
		ViewType::Tournament(tournament) => parse_view_tournament(tournament, args.short),
	}
}

fn parse_view_judge(args: ViewJudge, is_short: bool){
	let judge = crate::structs::Judge::read_from_json_file(&args.name);
	println!("{}", judge.to_string(is_short));
}

fn parse_view_judges(args: ViewJudges, short: bool){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}

fn parse_view_tournament(args: ViewTournament, short: bool){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}


#[derive(Debug, Args)]
pub struct Analyze {
	/// What type of analysis to perform
	#[clap(subcommand)]
	pub analyze_type: AnalyzeType,
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
	/// Search local judge .json files with a matching first and last name
	#[arg(short, long, value_name = "NAME")]
	name: String,
	
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
	/// Analyzise the ability of this program to guess debaters genders\
	#[arg(short = 'r', long)]
	hit_rate: bool,
	
	/// analyze the ballance of vote for and against women
	#[arg(short, long)]
	ballance: bool,
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

fn parse_analyze(args: Analyze){
	// match statment to find if is judge, judges, or tournament
	match args.analyze_type {
		AnalyzeType::Judge(judge) => parse_analyze_judge(judge),
		AnalyzeType::Judges(judges) => parse_analyze_judges(judges),
		AnalyzeType::Tournament(tournament) => parse_analyze_tournament(tournament),
	}
}


fn parse_analyze_judge(args: AnalyzeJudge){
	let judge = crate::structs::Judge::read_from_json_file(&args.name);
	match args.analyze_method {
		AnalyzeMethod::Age(age) => println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧"),
		AnalyzeMethod::Voting(voting) => println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧"),
		AnalyzeMethod::Gender(gender) => parse_analyze_judge_gender(judge, gender)
	}
}

fn parse_analyze_judge_gender(judge: crate::structs::Judge, args: AnalyzeGender){
	if args.hit_rate {
		api_succsess_rate(&judge);
	}
	if args.ballance {
		ballance_votes_for_and_against_women(&judge);
	}
}

fn parse_analyze_judges(args: AnalyzeJudges){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}

fn parse_analyze_tournament(args: AnalyzeTournament){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}


#[derive(Debug, Args)]
pub struct Delete {
	/// What type content to delete
	#[clap(subcommand)]
	pub analyze_type: Type,
}

// TODO
fn parse_delete(args: Delete){
	println!("starting to parse the delete command");
}

#[derive(Debug, Args)]
pub struct Generate {
	/// What type of data to collect
	#[clap(subcommand)]
	pub scrape_type: Type,
	
	/// Shorten the output
	#[arg(short, long)]
	short: bool,
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
#[command(group(
	ArgGroup::new("search_type")
		.required(true)
		.args(["name", "id"]),
))]
pub struct Judge {
	/// Search tab room for a judge with a matching first and last name
	#[arg(short, long, value_name = "NAME", group = "search_type")]
	name: Option<String>,
	
	/// Scrapes judge information given a 
	#[arg(short, long, value_name = "ID", group = "search_type")]
	id: Option<u32>,
	
	// #[arg(long, value_parser = check_name_or_id)]
	// _required: bool,
}

// fn check_name_or_id(judge: &Judge) -> Result<(), String> {
// 	if judge.name.is_none() && judge.id.is_none() {
// 		Err("either 'name' or 'id' is required".to_string())
// 	} else {
// 		Ok(())
// 	}
// }

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


fn parse_generate(args: Generate){
	match args.scrape_type {
		Type::Judge(judge) => parse_judge(judge, args.short),
		Type::Judges(judges) => parse_judges(judges, args.short),
		Type::Tournament(tournament) => parse_tournament(tournament, args.short),
	}
}

fn parse_judge(args: Judge, is_short: bool){
	let names = dict_thread_safe_api_and_storage::GetGender::new();
	
	if (args.id.is_some()) {
		println!("judge = {:}", get_paradim_html_from_judge_id(args.id.unwrap())
			.unwrap()
			.get_judge_struct(&names)
			.unwrap()
			.to_json_file()
			.to_string(is_short)
		);
	}
	
	else if let Some(name) = args.name {
		let split_names = name
			.split(" ")
			.collect::<Vec<&str>>();
		
		let first_last_name = match split_names.len() {
			0 => panic!("{} is not a valid name", name),
			1 => vec![split_names[0].to_string(), "".to_string()],
			2 => vec![split_names[0].to_string(), split_names[1].to_string()],
			_ => vec![split_names[0].to_string(), split_names[1..].join(" ")],
		};
		
		println!("judge = {:}", search_for_judge::search_tabroom_for_judge(
				first_last_name[0].to_string(),
				first_last_name[1].to_string()
			)
			.unwrap()
			.get_judge_struct(&names)
			.unwrap()
			.to_json_file()
			.to_string(is_short)
		);
	}

	names.close();
}

fn parse_judges(_args: Judges, _is_short: bool){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}

fn parse_tournament(_args: Tournament, _is_short: bool){
	println!("🚧🚧 UNDER CONSTRUCTION 🚧🚧");
}
