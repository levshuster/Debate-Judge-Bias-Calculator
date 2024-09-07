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
  "start_date" date,
  "updated" timestamp,
  "details" json,
  "to_scrape" bool
);

CREATE TABLE "division" (
  "id" integer PRIMARY KEY,
  "tournament" integer,
  "format" text,
  "level" text,
  "round" text,
  "is_elimination" bool,
  "url" text,
  "details" json
);

CREATE TABLE "pairing" (
  "id" integer PRIMARY KEY,
  "division" integer,
  "timestamp" timestamp
);

CREATE TABLE "school" (
  "id" integer PRIMARY KEY,
  "name" text,
  "to_scrape" bool,
  "url" text,
  "details" json
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
  "id" integer PRIMARY KEY,
  "name" text,
  "first_name" text
);

CREATE TABLE "gender_binding" (
  "first_name" text PRIMARY KEY,
  "gender" text,
  "confidance" decimal,
  "updated" timestamp,
  "source" text
);

CREATE TABLE "pairing"."team" (
  "id" integer PRIMARY KEY,
  "round" integer,
  "label" text,
  "school" integer
);

CREATE TABLE "pairing"."debater" (
  "id" integer,
  "team" integer
);

CREATE TABLE "pairing"."judge" (
  "round" integer,
  "vote" integer,
  "judge" integer,
  "school" integer
);

COMMENT ON TABLE "tournament_group"."details" IS 'Examples: Washington State, TOC qualifiers, Urban Debate Leage, etc.';

COMMENT ON TABLE "tournament" IS 'Examples: UPS invitational, Rose City Round Robin, etc.';

COMMENT ON TABLE "division" IS 'Example: Novice Public Forum, Varsity Policy, Open Dramatic Interp';

COMMENT ON COLUMN "division"."format" IS 'Policy, LD, Public Forum';

COMMENT ON COLUMN "division"."level" IS 'Open, Novice, Varsity';

COMMENT ON COLUMN "division"."round" IS 'Semi-Final, Round 1, 3';

COMMENT ON COLUMN "pairing"."team"."label" IS 'Examples include Aff, Neg, Pro, Con, etc.';

ALTER TABLE "tournament_group"."details" ADD FOREIGN KEY ("parent_group") REFERENCES "tournament_group"."details" ("id");

ALTER TABLE "tournament_group"."bindings" ADD FOREIGN KEY ("group") REFERENCES "tournament_group"."details" ("id");

ALTER TABLE "tournament_group"."bindings" ADD FOREIGN KEY ("tournament") REFERENCES "tournament" ("id");

ALTER TABLE "division" ADD FOREIGN KEY ("tournament") REFERENCES "tournament" ("id");

ALTER TABLE "pairing" ADD FOREIGN KEY ("division") REFERENCES "division" ("id");

ALTER TABLE "pairing"."team" ADD FOREIGN KEY ("round") REFERENCES "pairing" ("id");

ALTER TABLE "pairing"."team" ADD FOREIGN KEY ("school") REFERENCES "school" ("id");

ALTER TABLE "pairing"."debater" ADD FOREIGN KEY ("id") REFERENCES "debater" ("id");

ALTER TABLE "pairing"."debater" ADD FOREIGN KEY ("team") REFERENCES "pairing"."team" ("id");

ALTER TABLE "pairing"."judge" ADD FOREIGN KEY ("round") REFERENCES "pairing" ("id");

ALTER TABLE "pairing"."judge" ADD FOREIGN KEY ("vote") REFERENCES "pairing"."team" ("id");

ALTER TABLE "pairing"."judge" ADD FOREIGN KEY ("judge") REFERENCES "judge" ("id");

ALTER TABLE "pairing"."judge" ADD FOREIGN KEY ("school") REFERENCES "school" ("id");

ALTER TABLE "judge" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");

ALTER TABLE "debater" ADD FOREIGN KEY ("first_name") REFERENCES "gender_binding" ("first_name");
