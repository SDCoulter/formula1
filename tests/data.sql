-- Test data for testing the app.
INSERT INTO constructor_standings
VALUES
  (11, 1, 'A Constructor Name', 0, 0, 'url_text', '1_national', 2021, 10),
  (12, 2, 'A Different Name', 0, 0, 'url_text2', '2_national', 2021, 11);

INSERT INTO data_exps
  (1, "Constructor Standings Analysis", "/con_standings", "View constructor standings from different seasons and rounds with API calls.", "16-Nov-22", "con_standings", "https://github.com/SDCoulter/formula1/blob/main/formula1_data/f1data.py"),
  (1, "Drivers Standings Analysis", "/dri_standings", "View driver standings", "21-Nov-21", "dri_standings", "https://github.com/SDCoulter/formula1/blob/main/formula1_data/f1data.py");
