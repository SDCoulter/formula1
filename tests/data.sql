-- Test data for testing the app.3
INSERT INTO data_exps (id, name, url, description, date_created, function_name, function_url)
VALUES
  (9000, "Drivers Standings Analysis", "guguigui", "View driver standings", "21-Nov-21", "whatwhy", "https://github.com"),
  (8000, "abc", "def", "ghi", "lmnop", "asdfghjkl;", "qrs");


INSERT INTO constructor_standings (uid, position, constructor_name, points, wins, constructor_url, constructor_nationality, season_year, round_number)
VALUES
  (11, 1, 'A Constructor Name', 0, 0, 'url_text', '1_national', 2021, 10),
  (12, 2, 'A Different Name', 0, 0, 'url_text2', '2_national', 2021, 11);
