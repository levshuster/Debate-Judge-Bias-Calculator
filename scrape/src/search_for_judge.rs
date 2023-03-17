use reqwest::header;
use std::collections::HashMap;

use crate::HtmlUrlPair;

// todo, add handeling for when there are multiple results
pub(crate) fn search_tabroom_for_judge(first_name: String, last_name: String) -> Result<HtmlUrlPair, Box<dyn std::error::Error>> {
	let url = "https://www.tabroom.com/index/paradigm.mhtml";

	// Prepare the request body as a HashMap of key-value pairs
	let mut params = HashMap::new();
	params.insert("search_first", first_name);
	params.insert("search_last", last_name);

	// Create a new client and POST request with the parameters
	let client = reqwest::blocking::Client::new();
	let response = client.post(url)
		.header(header::CONTENT_TYPE, "application/x-www-form-urlencoded")
		.form(&params)
		.send()?;

	let body = response.text()?;

	Ok(HtmlUrlPair {
		html: body,
		url: url.to_string(),
	})
}
