use reqwest::blocking::get;
use serde_json::to_writer;
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, fs::File, io::BufReader, alloc::System};
use crate::structs::{self, GenderType};
use std::sync::{Arc, RwLock};

static PERSON_JSON: &str = "person_dict.json";
struct ThreadSafeDict<K, V> {
	dict: Arc<RwLock<HashMap<K, V>>>,
}

impl<K: Eq + std::hash::Hash + Clone, V: Clone> ThreadSafeDict<K, V> {
	fn new() -> Self {
		Self {
			dict: Arc::new(RwLock::new(HashMap::new())),
		}
	}

	fn insert(&self, key: K, value: V) {
		let mut dict = self.dict.write().unwrap();
		dict.insert(key, value);
	}

	fn _remove(&self, key: &K) {
		let mut dict = self.dict.write().unwrap();
		dict.remove(key);
	}

	fn get(&self, key: &K) -> Option<V> {
		let dict = self.dict.read().unwrap();
		dict.get(key).cloned()
	}
	
	fn to_list(&self) -> Vec<(K, V)> {
		let dict = self.dict.read().unwrap();
		dict.iter().map(|(k, v)| (k.clone(), v.clone())).collect()
	}
	
}

pub struct GetGender {
	dict: ThreadSafeDict<String, Gender>,
	api_call_count: u32
}

impl GetGender {
	pub(crate) fn new() -> GetGender {
		GetGender{
			dict: read_from_json_file(),
			api_call_count: 0
		}
	}
	pub(crate) fn close(&self){
		write_to_json_file(&self.dict, self.api_call_count);
	}
	pub(crate) fn get(&self, name: String) -> structs::Gender {
		match get_gender(name, &self.dict){
			Some(gender) => gender,
			None => structs::Gender{
				confidance: 0.0, 
				get: GenderType::Unknown
			}
		}
	}
}


#[derive(Debug, Deserialize, Serialize, Clone)]
struct Gender {
	gender: Option<String>,
	probability: f32,
}

fn get_genders_with_api(name: &str) -> Option<Gender> {
	let api_url = format!("https://api.genderize.io?&name[1]={}", name);
	let response = get(&api_url)
		.unwrap()
		.json::<Vec<Gender>>();
	println!("API call: {}", api_url);
	match response {
		Ok(response) => Some(response[0].clone()),
		Err(_) => None,
	}
}

fn get_gender(name:String, existing_names: &ThreadSafeDict<String, Gender>) -> Option<structs::Gender> {
	let first_name = name.split_whitespace().next()?.to_string();
	let local = get_gender_to_local_type(first_name, existing_names)?;
	let binding = "unknown".to_string();
	let gender = local.gender
		.as_ref()
		.unwrap_or(&binding)
		.as_str();
		
	let gender_type = match gender {
		"male" => GenderType::Male,
		"female" => GenderType::Female,
		"nonbinary" => GenderType::Nonbinary,
		"unknown" => GenderType::Unknown,
		_ => panic!("Invalid gender type: {:?}", local), // handle invalid input
	};
	
	Some(structs::Gender {
		confidance: local.probability, 
		get: gender_type
	})
}

fn get_gender_to_local_type(name: String, existing_names:&ThreadSafeDict<String, Gender>)-> Option<Gender> {
	let gender = existing_names.get(&name);
	if let Some(g) = gender {
		// println!("Found a match: {:?}\n", g);
		return Some(g.clone());
	}
	let new_name = get_genders_with_api(&name);
	if new_name.is_none() {
		return None;
	}
	let result = new_name.unwrap();
	existing_names.insert(name.clone(), result.clone());
	return Some(result);
}

fn write_to_json_file(names: &ThreadSafeDict<String, Gender>, api_call_count: u32) {
	let file = File::create(PERSON_JSON).unwrap();
	to_writer(&file, &names.to_list()).unwrap();
	// println!("Wrote to file {} times", api_call_count);
}

fn read_from_json_file() -> ThreadSafeDict<String, Gender> {
	let reader = BufReader::new(File::open(PERSON_JSON).unwrap());
	let list: Vec<(String, Gender)> = serde_json::from_reader(reader).unwrap_or([].to_vec());
	let dict = ThreadSafeDict::new();
	for (k, v) in list {
		dict.insert(k, v);
	}
	dict
}
