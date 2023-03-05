use reqwest::blocking::get;
use serde::{Deserialize, Serialize};
use std::{fs::File, io::BufReader};
use serde_json::to_writer;

use crate::structs::{self, GenderType};
static PERSON_JSON: &str = "person.json";


#[derive(Debug, Deserialize, Serialize, Clone)]
struct Gender {
	name: String,
	gender: Option<String>,
	probability: f32,
}

fn get_genders_with_api(name: &str) -> Gender {
	let api_url = format!("https://api.genderize.io?&name[1]={}", name);

	get(&api_url)
		.unwrap()
		.json::<Vec<Gender>>()
		.unwrap()[0]
		.clone()
}

// pub(crate) fn main() {    
// 	let brian = get_gender_to_local_type("Brian".to_string());
// 	println!("{:?}", brian);
// }

pub(crate) fn get_gender(name:String) -> structs::Gender {
	let first_name = name.split_whitespace().next().unwrap().to_string();
	// let local = match get_gender_to_local_type(first_name) {
	// 	Some(value) => value,
	// 	None => panic!("get gender to local type returned none")
	// };
	
	let local = get_gender_to_local_type(first_name).unwrap();
	
	let gender = local.gender
		.as_ref()
		.unwrap()
		.as_str();
		
	let gender_type = match gender {
		"male" => GenderType::Male,
		"female" => GenderType::Female,
		"nonbinary" => GenderType::Nonbinary,
		"unknown" => GenderType::Unknown,
		_ => panic!("Invalid gender type: {:?}", local), // handle invalid input
	};

	structs::Gender {
		confidance: local.probability, 
		get: gender_type
	}
}

// todo: make this async as store existing_names so it doesn't have to be read every time from the json file
fn get_gender_to_local_type(name: String)-> Option<Gender> {
	let existing_names = read_from_json_file();
	let gender = existing_names.iter().find(|g| g.name == name);
	if let Some(g) = gender {
		// println!("Found a match: {:?}\n", g);
		return Some(g.clone());
	} else {
		let new_name = get_genders_with_api(&name);
		// println!("Got a new name: {:?}\n", new_name);
		write_to_json_file(&existing_names
			.into_iter()
			.chain(std::iter::once(new_name.clone()))
			.collect::<Vec<_>>());
		return Some(new_name);
	}
}

fn write_to_json_file(name: &Vec<Gender>) {
	let file = File::create(PERSON_JSON).unwrap();
	to_writer(&file, name).unwrap();
}

fn read_from_json_file() -> Vec<Gender> {
	let reader = BufReader::new(File::open(PERSON_JSON).unwrap());
	serde_json::from_reader(reader).unwrap()
}