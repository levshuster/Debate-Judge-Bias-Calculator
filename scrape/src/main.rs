mod structs;
mod search_for_judge;
mod args;
mod scrape;
mod dict_thread_safe_api_and_storage;
use args::Opts;
use clap::Parser;

use crate::structs::Judge;
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
	let steve = 26335;
	let names = dict_thread_safe_api_and_storage::GetGender::new();
	println!("judge = {:}", Judge::read_from_json_file("Steve Rowe").to_string());

	// println!("judge = {:}", get_paradim_html_from_judge_id(steve)?
	// 	.get_judge_struct(&names)?
	// 	.to_json_file()
	// 	.to_string());
	
	// println!("judge = {:}", search_for_judge::search_tabroom_for_judge("Lev".to_string(), "Shuster".to_string())
	// 	.unwrap()
	// 	.get_judge_struct(&names)?
	// 	.to_string());
	
	let args = Opts::parse();
	
	names.close();
	// search_for_judge::search_tabroom_for_judge();
	Ok(())
}

