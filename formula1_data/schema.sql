-- Create tables to hold the Formula 1 data.

-- 21-11-16 - For now we are focusing on Constructor championship data.
DROP TABLE IF EXISTS constructor_standings;
-- 2020_constructorStandings.csv
CREATE TABLE constructor_standings (
  id INTEGER PRIMARY KEY,
  constructor TEXT UNIQUE NOT NULL,
  points INTEGER NOT NULL,
  wins INTEGER NOT NULL
);
