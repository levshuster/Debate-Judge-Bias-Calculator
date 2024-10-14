# Install PostgreSQL

https://wiki.postgresql.org/wiki/Homebrew

# Load Database Schema

```bash
createdb debate_db

psql -d debate_db -f debate_bias_calc.sql # some unique constraint error are fine here

sudo -u postgres psql -d debate_db
CREATE USER debate_bias_user WITH PASSWORD 'debate_bias_user';

GRANT ALL ON ALL TABLES IN SCHEMA public TO debate_bias_user;
GRANT ALL ON ALL TABLES IN SCHEMA pairing TO debate_bias_user;
GRANT USAGE ON SCHEMA pairing TO debate_bias_user;

ALTER TABLE pairing.debater DROP CONSTRAINT debater_first_name_fkey;
ALTER TABLE pairing.judge DROP CONSTRAINT judge_id_fkey;
# TODO: ADD ALTER TABLE pairing.speaker_points DROP CONSTRAINT debater_id_fkey;

\q


```

# load in bogus data

```psql
INSERT INTO tournament (id, name, url, updated, details, to_scrape)
VALUES
    (1, 'Bogus Invitational', 'https://www.example.com/tournament/1', CURRENT_TIMESTAMP, '{"location": "Example City", "date": "2024-10-01"}', FALSE),
    (2, 'Fictional Championship', 'https://www.example.com/tournament/2', CURRENT_TIMESTAMP, '{"location": "Sample Town", "date": "2024-11-15"}', FALSE);
```

# Other Useful Commands
`psql -d debate_db`
`dropdb debate_db`
`psql -d debate_db -f ../../../Back\ End/Database/debate_bias_calc.sql`

```sql

ALTER DEFAULT PRIVILEGES IN SCHEMA public;
GRANT USAGE ON SCHEMA pairing TO postgres;
GRANT ALL PRIVILEGES ON TABLES TO postgres;


psql -d debate_db

GRANT SELECT, INSERT, UPDATE ON TABLE pairing.team TO postgres;
GRANT SELECT, INSERT, UPDATE ON TABLE pairing.judge TO postgres;
GRANT SELECT, INSERT, UPDATE ON TABLE pairing.debater TO postgres;
ALTER TABLE pairing.debater DROP CONSTRAINT debater_first_name_fkey;


ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO postgres;

ALTER DEFAULT PRIVILEGES IN SCHEMA pairing
GRANT ALL ON TABLES TO postgres;

\q
```
