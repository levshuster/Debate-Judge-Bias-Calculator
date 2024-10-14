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
ALTER TABLE pairing.votes DROP CONSTRAINT votes_judge_fkey;

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
