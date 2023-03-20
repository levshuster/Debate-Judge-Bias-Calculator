mod structs;
mod search_for_judge;
mod args;
mod scrape;
mod dict_thread_safe_api_and_storage;
use args::Opts;
use clap::Parser;
use structs::{Debater, GenderType};

use crate::args::parse_cli;
use crate::structs::{Judge, Team};
use crate::scrape::get_paradim_html_from_judge_id;

// Next Step: clean code, test on more judges to catch errors and edge cases/exspand enum options
// save judge struts to a file so multiple can be compaired and data can be interpreted by a stats file

// start stats file
// write a function that will graph the confidance range to help pick a threshold
// write a function to caculate the judge score based on number for and against women
// write a function that will give the p value of the judge gender voting history


fn main() -> Result<(), reqwest::Error> {
	// let lev = 105729;
	// let laura = 26867;
	// let steve = 26335;
	// let names = dict_thread_safe_api_and_storage::GetGender::new();
	// println!("judge = {:}", Judge::read_from_json_file("Steve Rowe").to_string());

	// println!("judge = {:}", get_paradim_html_from_judge_id(steve)?
	// 	.get_judge_struct(&names)?
	// 	.to_json_file()
	// 	.to_string());
	
	// println!("judge = {:}", search_for_judge::search_tabroom_for_judge("Lev".to_string(), "Shuster".to_string())
	// 	.unwrap()
	// 	.get_judge_struct(&names)?
	// 	.to_string());
	
	parse_cli();
	
	// names.close();
	// search_for_judge::search_tabroom_for_judge();
	Ok(())
}

pub fn api_succsess_rate(judge: &Judge){
	let threshold = 0.5;
	
	let mut debaters: Vec<Debater> = Vec::new();
	for record in judge.record.iter(){
		for debater in record.aff.debaters.iter(){
			debaters.push(debater.clone());
		}
		for debater in record.neg.debaters.iter(){
			debaters.push(debater.clone());
		}
	}
	
	
	// get the total number of debaters
	let total = debaters.len() as u32;
	
	let unknown: u32 = debaters.iter().map(|debater| match debater.gender.get {
		GenderType::Unknown => 1,
		_ => 0,
	}).sum();
	
	// caculate then print the total number of debaters with a gender not of type Unknown
	println!("of the {} debaters, {} are unknown", total, unknown);
	println!("the api succsess rate is {}%", (total - unknown) as f32 / total as f32 * 100.0);

	
	
}

pub fn ballance_votes_for_and_against_women(judge: &Judge){
	let threshold = 0.5;

	let point_total:i32 = judge
		.record
		.iter()
		.map(|round| {			
			// if the vote total is greater than 1, the vote is invalid
			if round.vote.aff + round.vote.neg > 1{
				return 0;
			}
			
			let winner;
			let loser;
			if round.vote.aff == 1 {
				winner = &round.aff;
				loser = &round.neg;
			}
			else if round.vote.neg == 1 {
				winner = &round.neg;
				loser = &round.aff;
			}
			else {
				return 0;
			}
			fn get_score(team: &Team, threshold: f32)->(i32, bool){
				let mut invalid = false;
				(team.debaters.iter().map(|debater| {
					if debater.gender.confidance < threshold {
						invalid = true;
					};
					match debater.gender.get {
						GenderType::Male => -1,
						GenderType::Female => 1,
						_ => 0
					}
					
				}).sum(), invalid)
			}
			
			let winning_score = get_score(winner, threshold);
			let losing_score = get_score(loser, threshold);
			let result = match winning_score.1 || losing_score.1 {
				true => 0,
				false => winning_score.0 - losing_score.0,
			};
			// println!("round {} ", round.to_string());
			// println!("{} ", result);
			result
		})
		.sum();
	
	println!("the judge has given {} more ballots to women than men", point_total);
}