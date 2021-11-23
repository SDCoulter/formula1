$(document).ready(function() {

  // Target the selected element.
  let dropdown = $('#seasonYearDD');

  // Create a function to update Round Number dropdown when Season Year is changed.
  let updateSeasonYear = function(year) {
    // Get the number of rounds from the JSON file.
    let roundNumber = rql[year];
    // Select the Round Number dropdown.
    let rnDropdown = $('#roundNoDD');
    rnDropdown.empty();
    // Loop to add each round number to the dropdown.
    for (let i = roundNumber; i > 0; i--) {
      let roundName = i + " - " + r_names[year][i]['name']
      rnDropdown.append($('<option></option>').attr('value', roundName).text(roundName));
    };
  };

  // List of years imported from local JSON file.
  $.each(years, function(index, year) {
    dropdown.append($('<option></option>').attr('value', year).text(year));
  })

  // When the Season Year dropdown's value is changed, run updateSeasonYear() -
  // which updates the list of round numbers/names.
  $("select#seasonYearDD").on('change',function(){
    var selectedYear = $('#seasonYearDD option:selected').text();
    updateSeasonYear(selectedYear);
  });

});
