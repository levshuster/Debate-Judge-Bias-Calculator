# Install PostgreSQL

https://wiki.postgresql.org/wiki/Homebrew

# Load Database Schema

```bash
createdb debate_db
psql -d debate_db -f debate_bias_calc.sql
```

# Other Useful Commands

`dropdb debate_db`
