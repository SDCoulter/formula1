-- Drop tables on instance creation.
DROP TABLE IF EXISTS data_exps;
DROP TABLE IF EXISTS constructor_standings;


-- Table for data explorations.
CREATE TABLE data_exps (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  url TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  date_created TEXT NOT NULL,
  function_name TEXT UNIQUE NOT NULL,
  function_url TEXT NOT NULL
);

-- Constructor Standings table.
CREATE TABLE constructor_standings (
  uid INTEGER UNIQUE NOT NULL,
  position INTEGER NOT NULL,
  constructor_name TEXT NOT NULL,
  points INTEGER NOT NULL,
  wins INTEGER NOT NULL,
  constructor_url TEXT NOT NULL,
  constructor_nationality TEXT NOT NULL,
  season_year INTEGER NOT NULL,
  round_number INTEGER NOT NULL
);
