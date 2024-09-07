# Install PostgreSQL

https://wiki.postgresql.org/wiki/Homebrew

# Load Database Schema

```bash
createdb debate_db
psql -d debate_db
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO postgres;
\q
psql -d postgres -f debate_bias_calc.sql

```

# load in bogus data

```psql
INSERT INTO tournament (id, name, url, updated, details, to_scrape)
VALUES
    (1, 'Bogus Invitational', 'https://www.example.com/tournament/1', CURRENT_TIMESTAMP, '{"location": "Example City", "date": "2024-10-01"}', TRUE),
    (2, 'Fictional Championship', 'https://www.example.com/tournament/2', CURRENT_TIMESTAMP, '{"location": "Sample Town", "date": "2024-11-15"}', FALSE);
```

# Other Useful Commands
`psql -d debate_db`
`dropdb debate_db`


