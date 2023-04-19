mod structs;
mod search_for_judge;
mod args;
mod scrape;
mod dict_thread_safe_api_and_storage;
use std::{io, fs};
use std::path::Path;
use statrs::distribution::{Binomial, Discrete, DiscreteCDF};


use structs::{Debater, GenderType};

use crate::args::parse_cli;
use crate::structs::{Judge, Team};

// Next Step: clean code, test on more judges to catch errors and edge cases/exspand enum options
// save judge struts to a file so multiple can be compaired and data can be interpreted by a stats file

// start stats file
// write a function that will graph the confidance range to help pick a threshold
// write a function that will give the p value of the judge gender voting history


fn main() -> Result<(), reqwest::Error> {
	parse_cli();
	// println!("{}", calculate_p_value(5., 5.));
	Ok(())
}


// fn calculate_p_value(w: f64, m: f64) -> f64 {
//     let n: u64 = w + m;
//     let p = 0.5;
//     let binomial_dist = Binomial::new(n, p).unwrap();
//     let p_value = 2.0 * f64::min(binomial_dist.cdf(w as u64), 1.0 - binomial_dist.cdf(m - 1));
//     p_value
// }

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
	
	let less_than_threshold: u32 = debaters.iter().map(|debater| match debater.gender.confidance < threshold {
		true => 1,
		false => 0,
	}).sum();
	
	// caculate then print the total number of debaters with a gender not of type Unknown
	println!("of the {} debaters, {} are unknown", total, unknown);
	println!("the api succsess rate is {}%", (total - unknown) as f32 / total as f32 * 100.0);
	println!("\nof the {} debaters, {} have a confidance less than {}", total, less_than_threshold, threshold);
	println!("the api returned results greather than the threshold {}% of the time", (total - less_than_threshold) as f32 / total as f32 * 100.0);
	
	
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

fn get_json_file_names(dir_path: &str, start_of_file: &str) -> io::Result<Vec<String>> {
	let entries = fs::read_dir(dir_path)?;

	let mut json_files = Vec::new();

	for entry in entries {
		let entry = entry?;
		let file_type = entry.file_type()?;

		if file_type.is_file() {
			let file_name = entry.file_name();
			let name_string = file_name.to_string_lossy().to_string();
				
			let ext = Path::new(&file_name)
				.extension()
				.and_then(|ext| ext.to_str());

			if ext == Some("json") && name_string.starts_with(start_of_file) {
				let truncated_name_string = name_string[6..name_string.len() - 5].to_owned();
				json_files.push(truncated_name_string);
			}
			
		}
	}

	Ok(json_files)
}
