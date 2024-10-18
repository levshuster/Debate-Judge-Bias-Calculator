# Install PostgreSQL

https://wiki.postgresql.org/wiki/Homebrew

# Start postgres Service
Linux - `sudo service postgresql start`

# Load Database Schema

```bash
createdb debate_db

psql -d debate_db -f debate_bias_calc.sql # some unique constraint error are fine here
psql -d debate_db -c "\copy gender_binding FROM '../../Helper Functions/Python/Scratch Work/Gender Analysis/gender_compendium.csv' WITH (FORMAT CSV, HEADER)"

sudo -u postgres psql -d debate_db

CREATE USER debate_bias_user WITH PASSWORD 'debate_bias_user';

GRANT ALL ON ALL TABLES IN SCHEMA public TO debate_bias_user;
GRANT ALL ON ALL TABLES IN SCHEMA pairing TO debate_bias_user;
GRANT USAGE ON SCHEMA pairing TO debate_bias_user;

ALTER TABLE pairing.debater DROP CONSTRAINT debater_first_name_fkey;
ALTER TABLE pairing.judge DROP CONSTRAINT judge_id_fkey;
ALTER TABLE pairing.votes DROP CONSTRAINT votes_judge_fkey;
ALTER TABLE judge DROP CONSTRAINT judge_first_name_fkey;

\q

```

# Other Useful Commands
`psql -d debate_db`
`dropdb debate_db`
`psql -d debate_db -f ../../../Back\ End/Database/debate_bias_calc.sql`
