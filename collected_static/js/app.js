$(document).ready(function() {
  // Handle form submission for the search form
  $('#search-form').submit(function(event) {
    // Prevent the form from being submitted
    event.preventDefault();

    // Make an AJAX request to the server for the search results
    $.get('api/city/', {
      region: $('#').val()
    }, function(data) {
      // Update the drop-down menu with the search results
      $('#stop').autocomplete('option', 'source', data);
    });
  });

  // Handle form submission for the buses form
  $('#buses-form').submit(function(event) {
    // Prevent the form from being submitted
    event.preventDefault();

    // Make an AJAX request to the server for the buses
    $.get('api/stop/', {
      stop: $('#').val()
    }, function(data) {
      // Update the buses results div with the list of buses
      $('#buses-results').html(data);
    });
  });
});

function showStopDiv() {
    // Get the stop div and the set_region button
    var stopDiv = document.getElementById("stop");
    var setRegionButton = document.getElementById("set_region");
    var regionInputField = document.getElementById("region_input_field");

    // Add a click event listener to the set_region button
    setRegionButton.addEventListener("click", function() {
        // Get the value of the region_input_field input
        var query = regionInputField.value;
        // Make an AJAX request to the get_stop_area_tips view
        $.ajax({
            url: '/api/city/' + query + '/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // If the request is successful, store the received stop area names in a variable
                var stopAreas = data.stop_areas;
                // Update the stop input with the received stop area names
                var stopInput = document.getElementById("stop");
                stopInput.value = stopAreas.join(', ');
                // Make the stop div visible
                stopDiv.style.display = "block";
            }
        });
    });
}

// Call the showStopDiv function when the page loads
window.onload = showStopDiv;


// JavaScript code

// Get the input field element
const inputFieldR = document.getElementById('region_input_field');

// Add an event listener for the input event
inputFieldR.addEventListener('input', function() {
  // Get the current value of the input field
  const query = this.value;

  // Make a GET request to the Django view function
  fetch(`/api/city/${query}`)
    .then(response => response.json())
    .then(data => {
      // Get the list of unique stop area names from the response
      const stopAreas = data.stop_areas;

      // Create a dropdown list with the stop area names
      const dropdownList = document.createElement('ul');
      dropdownList.classList.add('dropdown-list');
      stopAreas.forEach(stopArea => {
        const listItem = document.createElement('li');
        listItem.innerHTML = stopArea;
        dropdownList.appendChild(listItem);
      });

      // Add the dropdown list to the input field
      inputFieldR.parentNode.appendChild(dropdownList);
    });
});
