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


    setRegionButton.addEventListener("click", function() {

        var query = regionInputField.value;

        $.ajax({
            url: '/api/city/' + query + '/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // If the request is successful, store the received stop area names in a variable
                var stopAreas = data.stop_areas;
                window.currentArea = data.stop_areas[0];
                // Update the stop input with the received stop area names
                const stopInput = document.getElementById("stop");
                stopInput.value = stopAreas.join(', ');
                // Make the stop div visible
                stopDiv.style.display = "block";
            }
        });
    });
}

// Call the showStopDiv function when the page loads
window.onload = showStopDiv;



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
        listItem.addEventListener('click', function() {
          // Set the value of the input field to the selected stop area
          inputFieldR.value = this.innerHTML;

          // Remove the dropdown list
          dropdownList.remove();
        });
        dropdownList.appendChild(listItem);
      });

      // Replace the dropdown list in the input field
      const existingDropdownList = inputFieldR.parentNode.querySelector('.dropdown-list');
      if (existingDropdownList) {
        inputFieldR.parentNode.replaceChild(dropdownList, existingDropdownList);
      } else {
        inputFieldR.parentNode.appendChild(dropdownList);
      }
    });
});



// Get the input field element
const inputFieldS = document.getElementById('stop_input');

// Add an event listener for the input event
inputFieldS.addEventListener('input', function() {
  // Get the current value of the input field
  const query = this.value;
  const stop = currentArea;

  // Make a GET request to the Django view function
  fetch(`/api/stop/${stop}/${query}`)
    .then(response => response.json())
    .then(data => {
      // Get the list of unique stop area names from the response
      const stops = data.stops;

      // Create a dropdown list with the stop area names
      const dropdownList = document.createElement('ul');
      dropdownList.classList.add('dropdown-list');
      stops.forEach(stopPoint => {
        const listItem = document.createElement('li');
        listItem.innerHTML = stopPoint;
        listItem.addEventListener('click', function() {
          // Set the value of the input field to the selected stop area
          inputFieldS.value = this.innerHTML;

          // Remove the dropdown list
          dropdownList.remove();
        });
        dropdownList.appendChild(listItem);
      });

      // Replace the dropdown list in the input field
      const existingDropdownList = inputFieldS.parentNode.querySelector('.dropdown-list');
      if (existingDropdownList) {
        inputFieldS.parentNode.replaceChild(dropdownList, existingDropdownList);
      } else {
        inputFieldS.parentNode.appendChild(dropdownList);
      }
    });
});


let globalRoutesInfo = [];

function getRoutesByStop(stopId) {
  return fetch(`api/routes/${stopId}`)
    .then(response => response.json());
}

function createRouteButtons(routesInfo) {
  const routesDiv = document.getElementById('routes');
  routesDiv.style.display = 'block';

    // Delete all existing buttons
  routesDiv.innerHTML = '';

  routesInfo.forEach(route => {
    const button = document.createElement('button');
    console.log(route);
   // button.classList.add('btn btn-primary');
    button.classList.add('route');
    button.textContent = route.short_name;
    button.style.borderColor = '#' + route.color;
    button.style.color = '#' + route.color;
    button.value = JSON.stringify(route);

    routesDiv.appendChild(button);
  });
}


let setStopButton = document.getElementById('set_stop');
//et stopNameInput = document.getElementById('stop_input');
let stopId;


setStopButton.addEventListener('click', function() {
  let stopName = inputFieldS.value;
  let stopArea = currentArea;
  let xhr = new XMLHttpRequest();
  xhr.open('GET', 'api/idstop/' + stopArea + '/' + stopName);
  xhr.onload = function() {
    if (xhr.status === 200) {
      stopId = xhr.responseText;
      getRoutesByStop(stopId).then(routesInfo => {
        globalRoutesInfo = routesInfo;
        createRouteButtons(globalRoutesInfo);
        displayRoute();
      });
    } else {
      console.error(xhr.responseText);
    }
  };
  xhr.send();
});


function displayRoute() {
  const buttons = document.querySelectorAll('.route');
  const displayElement = document.getElementById('route_dis');

  buttons.forEach(button => {
    button.addEventListener('click', event => {
      const obj = JSON.parse(event.target.value);
      route_id = obj.id;
      displayElement.style.color = '#' + obj.color;
      displayElement.textContent = `${obj.short_name} : ${obj.long_name}`;
      createArrivalTable(stopId, route_id);
      console.log('The button is clicked');
    });
  });
}

displayRoute();




async function createArrivalTable(stopId, routeId) {
  // Make the GET request to the get_arrival_times view
  const response = await fetch(`api/times/${stopId}/${routeId}`);
  const json = await response.json();

  // Get the div element to insert the table into
  const arrivalsDiv = document.getElementById("arrivals");
  arrivalsDiv.innerHTML = ''

  // Create the table element
  const table = document.createElement("table");

  // Create the table header
  const headerRow = document.createElement("tr");
  const iconHeader = document.createElement("th");
  iconHeader.innerText = "";
  headerRow.appendChild(iconHeader);
  const arrivalTimeHeader = document.createElement("th");
  arrivalTimeHeader.innerText = "Arrival Time";
  headerRow.appendChild(arrivalTimeHeader);
  const timeLeftHeader = document.createElement("th");
  timeLeftHeader.innerText = "Time Left (min)";
  headerRow.appendChild(timeLeftHeader);
  table.appendChild(headerRow);

  // Sort the arrival times by time left
  json.arrival_times.sort((a, b) => a.time_left - b.time_left);

  // Create a row for each arrival time
  for (const arrival of json.arrival_times) {
    const row = document.createElement("tr");

    // Add the icon column
    const iconColumn = document.createElement("td");
    const iconImg = document.createElement("p");
    iconImg.textContent = "🚌";
    iconColumn.appendChild(iconImg);
    row.appendChild(iconColumn);

    // Add the arrival time column
    const arrivalTimeColumn = document.createElement("td");
    arrivalTimeColumn.innerText = arrival.arrival_time;
    row.appendChild(arrivalTimeColumn);

    // Add the time left column
    const timeLeftColumn = document.createElement("td");
    let timeLeft = arrival.time_left;

    timeLeftColumn.innerText = timeLeft;
    if (timeLeft < 0) {
      row.style.color = "red";
    }
    row.appendChild(timeLeftColumn);

    // Add the row to the table
    table.appendChild(row);
  }

  // Add the table to the arrivals div
  arrivalsDiv.appendChild(table);
}




