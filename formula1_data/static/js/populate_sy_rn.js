$(document).ready(function() {

  // Target the selected element.
  let dropdown = $('#seasonYearDD');

  // Clear any left over options in element.
  //dropdown.empty();

  // Create a function to update Round Number dropdown when Season Year is changed.
  let updateSeasonYear = function(year) {
    // Get the number of rounds from the JSON file.
    let roundNumber = rql[year];
    // Select the Round Number dropdown.
    let rnDropdown = $('#roundNoDD');
    rnDropdown.empty();
    // Loop to add each round number to the dropdown.
    for (let i = roundNumber; i > 0; i--) {
      rnDropdown.append($('<option></option>').attr('value', i).text(i));
    };
  };

  // rq imported from local JSON file.
  // TODO: set up call to API on db init so it's covered for future seasons.
  $.each(rq, function(key) {
    dropdown.append($('<option></option>').attr('value', rq[key]['season_year']).text(rq[key]['season_year']));
  })

  $("select#seasonYearDD").on('change',function(){
    var selectedYear = $('#seasonYearDD option:selected').text();
    updateSeasonYear(selectedYear);
  });

});
