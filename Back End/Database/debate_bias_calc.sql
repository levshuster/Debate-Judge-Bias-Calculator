CREATE SCHEMA "tournament_group";

CREATE SCHEMA "pairing";

CREATE TABLE "tournament_group"."details" (
  "id" integer PRIMARY KEY,
  "name" text,
  "updated" timestamp,
  "url" text,
  "parent_group" integer,
  "to_scrape" bool,
  "details" json
);

CREATE TABLE "tournament_group"."bindings" (
  "group" integer,
  "tournament" integer
);

CREATE TABLE "tournament" (
  "id" integer PRIMARY KEY,
  "name" text,
  "url" text,
  "updated" timestamp,
  "details" json,
  "to_scrape" bool
);

CREATE TABLE "division" (
  "id" integer,
  "tournament" integer,
  "division_name" text,
  "format" text,
  "level" text,
  "round" text,
  "is_elimination" bool,
  "url" text,
  "details" json,
  "to_scrape" bool
);

CREATE TABLE "judge" (
  "id" integer PRIMARY KEY,
  "name" text,
  "first_name" text,
  "url" text,
  "to_scrape" bool,
  "updated" timestamp,
  "details" json
);

CREATE TABLE "gender_binding" (
  "first_name" text PRIMARY KEY,
  "gender" text,
  "confidance" decimal,
  "updated" timestamp,
  "source" text
);

CREATE TABLE "pairing"."team" (
  "url" text PRIMARY KEY,
  "to_scrape" bool
);

CREATE TABLE "pairing"."debater" (
  "name" text,
  "school" text,
  "first_name" text,
  "team" url
);

CREATE TABLE "pairing"."judge" (
  "url" text PRIMARY KEY,
  "id" integer,
  "to_scrape" bool
);

CREATE TABLE "pairing"."votes" (
  "judge" text,
  "team" text,
  "division" integer,
  "won" bool
);

CREATE TABLE "pairing"."speaker_points" (
  "judge" text,
  "team" text,
  "name" text,
  "division" integer,
  "value" decimal
);

COMMENT ON TABLE "tournament_group"."details" IS 'Examples: Washington State, TOC qualifiers, Urban Debate Leage, etc.';

COMMENT ON TABLE "tournament" IS 'Examples: UPS invitational, Rose City Round Robin, etc.';

COMMENT ON TABLE "division" IS 'Example: Novice Public Forum, Varsity Policy, Open Dramatic Interp';

COMMENT ON COLUMN "division"."format" IS 'Policy, LD, Public Forum';

COMMENT ON COLUMN "division"."level" IS 'Open, Novice, Varsity';

COMMENT ON COLUMN "division"."round" IS 'Semi-Final, Round 1, 3';

ALTER TABLE "tournament_group"."details" ADD FOREIGN KEY ("parent_group") REFERENCES "tournament_group"."details" ("id");

ALTER TABLE "tournament_group"."bindings" ADD FOREIGN KEY ("group") REFERENCES "tournament_group"."details" ("id");

ALTER TABLE "tournament_group"."bindings" ADD FOREIGN KEY ("tournament") REFERENCES "tournament" ("id");

ALTER TABLE "division" ADD FOREIGN KEY ("tournament") REFERENCES "tournament" ("id");

ALTER TABLE "pairing"."debater" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");

ALTER TABLE "pairing"."debater" ADD FOREIGN KEY ("team") REFERENCES "pairing"."team" ("url");

ALTER TABLE "pairing"."judge" ADD FOREIGN KEY ("id") REFERENCES "judge" ("id");

ALTER TABLE "pairing"."votes" ADD FOREIGN KEY ("judge") REFERENCES "pairing"."judge" ("url");

CREATE TABLE "pairing"."team_votes" (
  "team_url" text,
  "votes_team" text,
  PRIMARY KEY ("team_url", "votes_team")
);

ALTER TABLE "pairing"."team_votes" ADD FOREIGN KEY ("team_url") REFERENCES "pairing"."team" ("url");

ALTER TABLE "pairing"."team_votes" ADD FOREIGN KEY ("votes_team") REFERENCES "pairing"."votes" ("team");


ALTER TABLE "pairing"."votes" ADD FOREIGN KEY ("division") REFERENCES "division" ("id");

ALTER TABLE "pairing"."speaker_points" ADD FOREIGN KEY ("judge") REFERENCES "pairing"."judge" ("id");

CREATE TABLE "pairing"."debater_speaker_points" (
  "debater_team" url,
  "speaker_points_team" text,
  PRIMARY KEY ("debater_team", "speaker_points_team")
);

ALTER TABLE "pairing"."debater_speaker_points" ADD FOREIGN KEY ("debater_team") REFERENCES "pairing"."debater" ("team");

ALTER TABLE "pairing"."debater_speaker_points" ADD FOREIGN KEY ("speaker_points_team") REFERENCES "pairing"."speaker_points" ("team");


CREATE TABLE "pairing"."debater_speaker_points(1)" (
  "debater_name" text,
  "speaker_points_name" text,
  PRIMARY KEY ("debater_name", "speaker_points_name")
);

ALTER TABLE "pairing"."debater_speaker_points(1)" ADD FOREIGN KEY ("debater_name") REFERENCES "pairing"."debater" ("name");

ALTER TABLE "pairing"."debater_speaker_points(1)" ADD FOREIGN KEY ("speaker_points_name") REFERENCES "pairing"."speaker_points" ("name");


ALTER TABLE "pairing"."speaker_points" ADD FOREIGN KEY ("division") REFERENCES "division" ("id");

ALTER TABLE "judge" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");
