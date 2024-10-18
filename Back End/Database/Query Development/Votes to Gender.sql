SELECT count(*) AS count_of_joined_votes FROM (
	SELECT value, partial_name, lower(name), first_name, pairing.debater.team
	FROM pairing.speaker_points
	LEFT JOIN pairing.debater
	ON pairing.debater.team = speaker_points.team
	WHERE lower(name) LIKE '%' || partial_name || '%'
	ORDER BY pairing.debater.team
) as a;

SELECT count(*) AS vote_count FROM pairing.speaker_points;

-- Counts are off there are some double counts going on but its only off 1% of the time

CREATE TEMP VIEW speaker_points_and_gender AS
SELECT
	name,
	pairing.debater.first_name,
	value AS speaker_points,
	female_count,
	male_count,
	pairing.speaker_points.division,
	CASE
		WHEN female_count IS NULL THEN 'Unknown - Name Not in DB'
		WHEN female_count + male_count < 20 THEN 'Unknown - Too Few Names'
		WHEN LEAST(female_count, male_count) + ((female_count+male_count)/10) > GREATEST(female_count, male_count) THEN 'Unknown - Small Difference Between Counts'
		WHEN female_count > male_count THEN 'Female'
		WHEN male_count > female_count THEN 'Male'
		ELSE 'Error gender case never matched'
	END AS gender
FROM pairing.speaker_points
LEFT JOIN pairing.debater
ON pairing.debater.team = speaker_points.team
LEFT JOIN gender_binding
ON lower(gender_binding.first_name) = lower(pairing.debater.first_name)
WHERE lower(name) LIKE '%' || partial_name || '%'
AND value < 35
ORDER BY name;

SELECT female_count IS NOT NULL AS debater_gender_found, count(*)
FROM speaker_points_and_gender
GROUP BY female_count IS NOT NULL;

-- SELECT * from speaker_points_and_gender WHERE female_count IS NULL;


SELECT * FROM speaker_points_and_gender;

SELECT gender, count(*), AVG(speaker_points), STDDEV(speaker_points)
FROM speaker_points_and_gender
GROUP BY gender;

SELECT
    gender,
    speaker_points
FROM speaker_points_and_gender
WHERE gender IN ('Male', 'Female');

-- SELECT * FROM gender_binding;
