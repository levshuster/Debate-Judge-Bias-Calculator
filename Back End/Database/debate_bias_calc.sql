CREATE SCHEMA "tournament_group";

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

CREATE TABLE "pairing" (
  "id" integer PRIMARY KEY,
  "division" integer,
  "tournamet" integer,
  "first_url" text
);

CREATE TABLE "votes" (
  "pairing" integer,
  "judge" integer,
  "team" text,
  "won" bool
);

CREATE TABLE "speaker_points" (
  "pairing" integer,
  "judge" integer,
  "team" text,
  "name" text,
  "value" decimal
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

CREATE TABLE "debater" (
  "team" text,
  "name" text,
  "first_name" text,
  "tournament" integer
);

CREATE TABLE "gender_binding" (
  "first_name" text PRIMARY KEY,
  "gender" text,
  "confidance" decimal,
  "updated" timestamp,
  "source" text
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

ALTER TABLE "pairing" ADD FOREIGN KEY ("division") REFERENCES "division" ("id");

ALTER TABLE "pairing" ADD FOREIGN KEY ("tournamet") REFERENCES "tournament" ("id");

ALTER TABLE "votes" ADD FOREIGN KEY ("pairing") REFERENCES "pairing" ("id");

ALTER TABLE "votes" ADD FOREIGN KEY ("judge") REFERENCES "judge" ("id");

CREATE TABLE "debater_votes" (
  "debater_team" text,
  "votes_team" text,
  PRIMARY KEY ("debater_team", "votes_team")
);

ALTER TABLE "debater_votes" ADD FOREIGN KEY ("debater_team") REFERENCES "debater" ("team");

ALTER TABLE "debater_votes" ADD FOREIGN KEY ("votes_team") REFERENCES "votes" ("team");


ALTER TABLE "speaker_points" ADD FOREIGN KEY ("pairing") REFERENCES "pairing" ("id");

ALTER TABLE "speaker_points" ADD FOREIGN KEY ("judge") REFERENCES "judge" ("id");

CREATE TABLE "debater_speaker_points" (
  "debater_team" text,
  "speaker_points_team" text,
  PRIMARY KEY ("debater_team", "speaker_points_team")
);

ALTER TABLE "debater_speaker_points" ADD FOREIGN KEY ("debater_team") REFERENCES "debater" ("team");

ALTER TABLE "debater_speaker_points" ADD FOREIGN KEY ("speaker_points_team") REFERENCES "speaker_points" ("team");


CREATE TABLE "debater_speaker_points(1)" (
  "debater_name" text,
  "speaker_points_name" text,
  PRIMARY KEY ("debater_name", "speaker_points_name")
);

ALTER TABLE "debater_speaker_points(1)" ADD FOREIGN KEY ("debater_name") REFERENCES "debater" ("name");

ALTER TABLE "debater_speaker_points(1)" ADD FOREIGN KEY ("speaker_points_name") REFERENCES "speaker_points" ("name");


ALTER TABLE "judge" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");

ALTER TABLE "debater" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");

ALTER TABLE "debater" ADD FOREIGN KEY ("tournament") REFERENCES "tournament" ("id");
