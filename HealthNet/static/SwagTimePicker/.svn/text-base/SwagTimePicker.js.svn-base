
var clickedAmPm = false;

// Initialize a timepicker with the given id
function initSwagTp(pickerId) {

  var picker = document.getElementById(pickerId); // Get the picker from the DOM

  // If this picker has an input associated with it, initialize it to 12:00 PM
  if (picker.hasAttribute("inputId")) {
    var input = document.getElementById(picker.getAttribute("inputId"));
    input.value = "12:00 PM"
  }

  // Get the clock showing hours, and the clock showing minutes.
  // Add stp-display-none to minute clock to hide it.
  // Also set the active attributes.  Hour clock is true, minute is false.
  var hourClock = picker.getElementsByClassName("swag-tp-clock-hours");
  hourClock[0].setAttribute("active", "true");
  hourClock[0].classList.add("stp-display-block");
  var minuteClock = picker.getElementsByClassName("swag-tp-clock-minutes");
  minuteClock[0].classList.add("stp-display-none");
  minuteClock[0].setAttribute("active", "false");

  // Get the text in the header that says 'am' and 'pm'.
  // Set pm active to true and am active to false, essentially defaulting
  // to pm.
  var am = picker.getElementsByClassName("swag-tp-am");
  am[0].setAttribute("active", "false");
  var pm = picker.getElementsByClassName("swag-tp-pm");
  pm[0].setAttribute("active", "true");
  pm[0].classList.add("swag-tp-ampm-active");

  // Add a click event listener to the am text.
  // When it is clicked, set the right attributes and styles to indicate
  // that am is now selected.
  am[0].addEventListener('click', function(e) {
    e = window.event || e;
    if (this === e.target) {
      clickedAmPm = true; // Either am or pm was clicked recently

      // Set am active and pm not active
      am[0].setAttribute("active", "true");
      pm[0].setAttribute("active", "false");
      am[0].classList.add("swag-tp-ampm-active");
      pm[0].classList.remove("swag-tp-ampm-active");

      // If this picker has an associated input, set the input text to reflect
      // the change in period
      if (picker.hasAttribute("inputId")) {
        var ampm = "PM";
        var currentHour = picker.getElementsByClassName("swag-tp-h");
        var currentMinute = picker.getElementsByClassName("swag-tp-m");

        if (am[0].hasAttribute("active"))
          if (am[0].getAttribute("active") === "true")
            ampm = "AM";

        var input = document.getElementById(picker.getAttribute("inputId"));
        input.value = currentHour[0].innerHTML + ":" + currentMinute[0].innerHTML + " " + ampm;
      }

      // After 400ms reset clickedAmPm to false
      setTimeout(function() {
        clickedAmPm = false;
      }, 400);
    }
  } , false);

  // Add a click event listener to the pm text.
  // When it is clicked, set the right attributes and styles to indicate
  // that pm is now selected.
  pm[0].addEventListener('click', function(e) {
    e = window.event || e;
    if (this === e.target) {

      clickedAmPm = true; // Either am or pm was clicked recently

      // Set pm active and am not active
      am[0].setAttribute("active", "false");
      pm[0].setAttribute("active", "true");
      am[0].classList.remove("swag-tp-ampm-active");
      pm[0].classList.add("swag-tp-ampm-active");

      // If this picker has an associated input, set the input text to reflect
      // the change in period
      if (picker.hasAttribute("inputId")) {
        var ampm = "PM";
        var currentHour = picker.getElementsByClassName("swag-tp-h");
        var currentMinute = picker.getElementsByClassName("swag-tp-m");

        if (am[0].hasAttribute("active"))
          if (am[0].getAttribute("active") === "true")
            ampm = "AM";

        var input = document.getElementById(picker.getAttribute("inputId"));
        input.value = currentHour[0].innerHTML + ":" + currentMinute[0].innerHTML + " " + ampm;
      }

      // After 400ms reset clickedAmPm to false
      setTimeout(function() {
        clickedAmPm = false;
      }, 400);
    }
  } , false);

  // Obtain the contents of the clock, excluding the header.
  // We want to hide this at first, so set the entire picker's
  // height to 40px (the height of just the header), and translate the content
  // up 100% so it is hidden.
  var contents = picker.getElementsByClassName("swag-tp-content");
  contents[0].classList.add("stp-content-hidden");
  picker.classList.add("stp-height-40");

  // Get the picker's header and add a click event to it so the
  // content can be shown when clicked.
  var headers = picker.getElementsByClassName("swag-tp-header");
  headers[0].addEventListener('click', function(e) {
    if (clickedAmPm == false)
      showPicker(picker); // Show the picker when the header is clicked
  } , false);

  // Get the picker's ok button and add a click event to it so when
  // clicked, the picker content is hidden.
  var oks = picker.getElementsByClassName("swag-tp-ok");
  oks[0].addEventListener('click', function(e) {
    hidePicker(picker); // Hide the picker when the ok button is clicked
  } , false);

  // Get all of the picker's "hour bubbles" on the hour clock.
  // Add a click event to each of them to change the selected hour
  // and switch to the minute clock
  var hours = picker.getElementsByClassName("swag-tp-hour");
  for (var x = 0; x < hours.length; x++) {
    hours[x].addEventListener('click', function(e) {
      hourClicked(picker, e.srcElement); // An hour has been clicked
    } , false);
  }

  // Get all of the picker's "minute bubble" on the minute clock.
  // Add a click event to each of them to change the selected minute
  var minutes = picker.getElementsByClassName("swag-tp-minute");
  for (var x = 0; x < minutes.length; x++) {
    minutes[x].addEventListener('click', function(e) {
      minuteClicked(picker, e.srcElement); // A minute has been clicked
    } , false);
  }

  // Get the current hour text from the header and add a click event
  var currentHour = picker.getElementsByClassName("swag-tp-h");
  currentHour[0].classList.add("swag-tp-active"); // Set active
  currentHour[0].addEventListener('click', function(e) {
    currentHourClicked(picker); // The current hour text was clicked
  } , false);

  // Get the current minute text from the header and add a click event
  var currentMinute = picker.getElementsByClassName("swag-tp-m");
  currentMinute[0].classList.add("swag-tp-active"); // Set active
  currentMinute[0].addEventListener('click', function(e) {
    currentMinuteClicked(picker); // The current minute text was clicked
  } , false);
}

// Show the content of the picker.
function showPicker(picker) {
  // Obtain the content element
  var contents = picker.getElementsByClassName("swag-tp-content");
  var content = contents[0];

  // When the picker is shown from being hidden, we want to fade the
  // current minute text out so only the current hour text is bright,
  // indicating that it is what we're currently selecting a time for.
  var currentMinute = picker.getElementsByClassName("swag-tp-m");
  currentMinute[0].classList.remove("swag-tp-active");

  // Slide the content down into view
  content.classList.remove("stp-content-hidden");
  content.classList.remove("swag-tp-slide-up");
  content.classList.add("swag-tp-slide-down");

  // Set the height of the picker to allow room for the content to slide in
  picker.classList.remove("stp-height-40");
  picker.classList.remove("swag-tp-height-40");
  picker.classList.add("swag-tp-height-300");
}

// Hide the content of the picker.
function hidePicker(picker) {
  // Obtain the content element
  var contents = picker.getElementsByClassName("swag-tp-content");
  var content = contents[0];

  // Slide the content up out of view
  content.classList.remove("swag-tp-slide-down");
  content.classList.add("swag-tp-slide-up");

  // Change the picker height to only show the header
  picker.classList.remove("swag-tp-height-300");
  picker.classList.add("swag-tp-height-40");

  // Get the current hour text and set it to active so it isn't faded out
  var currentHour = picker.getElementsByClassName("swag-tp-h");
  currentHour[0].classList.add("swag-tp-active");

  // get the clock element
  var clock = picker.getElementsByClassName("swag-tp-clock");

  // Remove all animations
  clock[0].classList.remove("swag-tp-slide-in-right");
  clock[0].classList.remove("swag-tp-slide-in-left");
  clock[0].classList.remove("swag-tp-slide-out-right");
  clock[0].classList.remove("swag-tp-slide-out-left");

  // Get the hour clock element, set it to be active, and show it
  var hourClock = picker.getElementsByClassName("swag-tp-clock-hours");
  hourClock[0].setAttribute("active", "true");
  hourClock[0].classList.remove("stp-display-none");
  hourClock[0].classList.add("stp-display-block");

  // Get the minute clock element, set it to be not active, and hide it
  var minuteClock = picker.getElementsByClassName("swag-tp-clock-minutes");
  minuteClock[0].setAttribute("active", "false");
  minuteClock[0].classList.remove("stp-display-block");
  minuteClock[0].classList.add("stp-display-none");

  setTimeout(function() {
    // Get the current minute text and set it to active so it isn't faded out
    var currentMinute = picker.getElementsByClassName("swag-tp-m");
    currentMinute[0].classList.add("swag-tp-active");
  }, 400);
}

// An "hour bubble" has been clicked, update the selected hour to the one
// that was clicked and then switch to the minute clock.
function hourClicked(picker, hour) {

  // Get the current hour and minute text elements
  var currentHour = picker.getElementsByClassName("swag-tp-h");
  currentHour[0].innerHTML = hour.innerHTML; // Update the hour text to what was clicked
  var currentMinute = picker.getElementsByClassName("swag-tp-m");

  // If this picker has an associated input, update the input text
  if (picker.hasAttribute("inputId")) {
    var ampm = "PM";
    var am = picker.getElementsByClassName("swag-tp-am");

    if (am[0].hasAttribute("active"))
      if (am[0].getAttribute("active") === "true")
        ampm = "AM";

    var input = document.getElementById(picker.getAttribute("inputId"));
    input.value = currentHour[0].innerHTML + ":" + currentMinute[0].innerHTML + " " + ampm;
  }

  // Switch to the minute clock
  switchToMinutes(picker);
}

// A "minute bubble" has been clicked, update the selected minute to the one
// that was clicked.
function minuteClicked(picker, minute) {

  // Get the current hour and minute text elements
  var currentHour = picker.getElementsByClassName("swag-tp-h");
  var currentMinute = picker.getElementsByClassName("swag-tp-m");
  currentMinute[0].innerHTML = minute.innerHTML; // Update the minute text to what was clicked

  // If this picker has an associated input, update the input text
  if (picker.hasAttribute("inputId")) {
    var ampm = "PM";
    var am = picker.getElementsByClassName("swag-tp-am");

    if (am[0].hasAttribute("active"))
      if (am[0].getAttribute("active") === "true")
        ampm = "AM";

    var input = document.getElementById(picker.getAttribute("inputId"));
    input.value = currentHour[0].innerHTML + ":" + currentMinute[0].innerHTML + " " + ampm;
  }
}

// Switch from the hour clock to the minute clock.
function switchToMinutes(picker) {

  // get the clock element
  var clock = picker.getElementsByClassName("swag-tp-clock");

  // Slide the clock out to the left
  clock[0].classList.remove("swag-tp-slide-in-right");
  clock[0].classList.remove("swag-tp-slide-in-left");
  clock[0].classList.remove("swag-tp-slide-out-right");
  clock[0].classList.remove("swag-tp-slide-out-left");
  clock[0].classList.add("swag-tp-slide-out-left");

  // Wait 400ms and slide the clock back in from the right but as the minute clock
  setTimeout(function() {

    // Get the hour clock element, set it to not be active, and hide it
    var hourClock = picker.getElementsByClassName("swag-tp-clock-hours");
    hourClock[0].setAttribute("active", "false");
    hourClock[0].classList.remove("stp-display-block");
    hourClock[0].classList.add("stp-display-none");

    // Get the minute clock element, set it to be active, and show it
    var minuteClock = picker.getElementsByClassName("swag-tp-clock-minutes");
    minuteClock[0].setAttribute("active", "true");
    minuteClock[0].classList.remove("stp-display-none");
    minuteClock[0].classList.add("stp-display-block");

    // Update the current time text elements in the header to reflect that
    // you are now picking a minute
    var currentHour = picker.getElementsByClassName("swag-tp-h");
    currentHour[0].classList.remove("swag-tp-active");
    var currentMin = picker.getElementsByClassName("swag-tp-m");
    currentMin[0].classList.add("swag-tp-active");

    // Slide the clock in from the right
    clock[0].classList.remove("swag-tp-slide-out-left");
    clock[0].classList.add("swag-tp-slide-in-left");
  }, 400);
}

// Switch from the minute clock to the hour clock.
function switchToHours(picker) {

  // get the clock element
  var clock = picker.getElementsByClassName("swag-tp-clock");

  // Slide the clock out to the right
  clock[0].classList.remove("swag-tp-slide-in-right");
  clock[0].classList.remove("swag-tp-slide-in-left");
  clock[0].classList.remove("swag-tp-slide-out-right");
  clock[0].classList.remove("swag-tp-slide-out-left");
  clock[0].classList.add("swag-tp-slide-out-right");

  // Wait 400ms and slide the clock back in from the left but as the hour clock
  setTimeout(function() {

    // Get the hour clock element, set it to be active, and show it
    var hourClock = picker.getElementsByClassName("swag-tp-clock-hours");
    hourClock[0].setAttribute("active", "true");
    hourClock[0].classList.remove("stp-display-none");
    hourClock[0].classList.add("stp-display-block");

    // Get the minute clock element, set it to be not active, and hide it
    var minuteClock = picker.getElementsByClassName("swag-tp-clock-minutes");
    minuteClock[0].setAttribute("active", "false");
    minuteClock[0].classList.remove("stp-display-block");
    minuteClock[0].classList.add("stp-display-none");

    // Update the current time text elements in the header to reflect that
    // you are now picking a minute
    var currentHour = picker.getElementsByClassName("swag-tp-h");
    currentHour[0].classList.add("swag-tp-active");
    var currentMin = picker.getElementsByClassName("swag-tp-m");
    currentMin[0].classList.remove("swag-tp-active");

    // Slide the clock in from the left
    clock[0].classList.remove("swag-tp-slide-out-right");
    clock[0].classList.add("swag-tp-slide-in-right");
  }, 400);
}

// The current hour text was clicked.  If the hour clock is not active, show it.
function currentHourClicked(picker) {
  var hourClock = picker.getElementsByClassName("swag-tp-clock-hours");

  // If the hour clock is not active, switch to it
  if (hourClock[0].hasAttribute("active"))
    if(hourClock[0].getAttribute("active") === "false")
      switchToHours(picker);
}

// The current minute text was clicked.  If the minute clock is not active, show it.
function currentMinuteClicked(picker) {
  var minuteClock = picker.getElementsByClassName("swag-tp-clock-minutes");

  // If the minute clock is not active, switch to it
  if (minuteClock[0].hasAttribute("active"))
    if(minuteClock[0].getAttribute("active") === "false")
      switchToMinutes(picker);
}
