$(document).ready(function() {
  var calbtn = document.getElementById("calendar-btn");
  var contbtn = document.getElementById("contact-btn");
  var messagebtn = document.getElementById("message-btn");
  var notifybtn = document.getElementById("notify-btn");
  var notifynum = document.getElementById("notify-num");
  var staffPeekBtn = document.getElementById("staff-peek-btn");
  var peekSearchBtn = document.getElementById("peek-search-button");

  var calbtnTop = document.getElementById("top-calendar-btn");
  var contbtnTop = document.getElementById("top-contact-btn");
  var messagebtnTop = document.getElementById("top-message-btn");
  var notifybtnTop = document.getElementById("top-notify-btn");
  var notifynumTop = document.getElementById("top-notify-num");
  var staffPeekBtnTop = document.getElementById("top-staff-peek-btn");

  var cal = document.getElementById("cal-id");
  var cal2 = document.getElementById("cal2-id");
  var calTools = document.getElementById("cal-tools");
  var today = document.getElementsByClassName("fc-today-button");
  var row = document.getElementById("row-id-1");
  var contacts = document.getElementById("contacts-content");
  var messages = document.getElementById("profile-messages-pane");
  var messageContacts = document.getElementById("profile-messagecontacts-pane");
  var notifications = document.getElementById("notifications-pane");
  var peek = document.getElementById("peek-row");

  var notifyOpen = false;

  calTools.classList.remove("hide");
  cal.style.position = "static";
  cal.style.top = "0";

  cal2.style.position = "static";
  cal2.style.top = "0";

  notifybtn.addEventListener("click", showNotifications);
  notifynum.addEventListener("click", showNotifications);

  calbtn.addEventListener("click", switchToCalendar);
  contbtn.addEventListener("click", switchToContacts);
  messagebtn.addEventListener("click", switchToMessages);
  staffPeekBtn.addEventListener("click", switchToPeek);
  peekSearchBtn.addEventListener("click", showSearch);

  calbtnTop.addEventListener("click", function() {
    switchToCalendar();
    topbarToggle();
  });
  contbtnTop.addEventListener("click", function() {
    switchToContacts();
    topbarToggle();
  });
  messagebtnTop.addEventListener("click", function() {
    switchToMessages();
    topbarToggle();
  });
  notifybtnTop.addEventListener("click", function() {
    showNotifications();
    topbarToggle();
  });
  notifynumTop.addEventListener("click", function() {
    showNotifications();
    topbarToggle();
  });
  staffPeekBtnTop.addEventListener("click", function() {
    switchToPeek();
    topbarToggle();
  });

  $('#search-btn').click(function(e) {
    $('#search-input').focus();
    $('#search-input').val("");
    var results = document.getElementById('search-results');
    results.innerHTML = "";
  });

  $('#top-search-btn').click(function(e) {
    $('#search-input').focus();
    $('#search-input').val("");
    var results = document.getElementById('search-results');
    results.innerHTML = "";
  });

  function switchToCalendar() {
    peek.classList.add("hide");
    contacts.classList.add("hide");
    row.classList.remove("hide");
    messages.classList.add("hide");
    messageContacts.classList.add("hide");
    cal.children[0].classList.remove("animate-from-bottom");
    cal.children[0].classList.add("scale-0");
    cal.children[0].classList.add("fade-grow-in");
    cal.classList.remove("hide");
    cal2.children[0].classList.remove("animate-from-bottom");
    cal2.children[0].classList.add("scale-0");
    cal2.children[0].classList.add("fade-grow-in");
    cal2.classList.remove("hide");
    calTools.children[0].classList.remove("animate-from-bottom");
    calTools.children[0].classList.add("scale-0");
    calTools.children[0].classList.add("fade-grow-in");
    calTools.classList.remove("hide");

    cal.style.position = "static";
    cal.style.top = "0";

    cal2.style.position = "static";
    cal2.style.top = "0";
  }

  function switchToContacts() {
    peek.classList.add("hide");
    row.classList.add("hide");
    contacts.classList.remove("hide");
    contacts.classList.add("scale-0");
    contacts.classList.add("fade-grow-in");
  }

  function switchToMessages() {
    peek.classList.add("hide");
    contacts.classList.add("hide");
    row.classList.remove("hide");
    row.classList.remove("hide");
    cal.classList.add("hide");
    cal2.classList.add("hide");
    calTools.classList.add("hide");

    messages.children[0].classList.remove("animate-from-bottom");
    messages.children[0].classList.add("scale-0");
    messages.children[0].classList.add("fade-grow-in");
    messages.classList.remove("hide");

    messageContacts.children[0].classList.remove("animate-from-bottom");
    messageContacts.children[0].classList.add("scale-0");
    messageContacts.children[0].classList.add("fade-grow-in");
    messageContacts.classList.remove("hide");
  }

  function switchToPeek(html) {
    row.classList.add("hide");
    contacts.classList.add("hide");
    peek.classList.remove("hide");

    document.getElementById("profile-body").style.overflow = "hidden";
    setTimeout(function() {
      document.getElementById("profile-body").style.overflow = "auto";
    }, 400);
  }

  function showSearch() {
    $("#search-btn").click();
  }

  function showNotifications() {
    if (!notifyOpen) {
      notifications.classList.remove("fade-grow-out");
      notifications.classList.add("scale-0");
      notifications.classList.add("fade-grow-in");
      $(notifications).animate({
          width: "10px",
          height: "10px"
      }, 50, function () {
      });
      notifications.classList.remove("hide");
      $(notifications).animate({
          width: "400px",
          height: "300px"
      }, 300, function () {
      });

      notifyOpen = true;
    }
    else {
      notifications.classList.remove("scale-0");
      notifications.classList.remove("fade-grow-in");
      notifications.classList.add("fade-grow-out");
      $(notifications).animate({
          width: "10px",
          height: "10px"
      }, 250, function () {
      });
      setTimeout(function() {
        notifications.classList.add("hide");
      }, 250);

      notifyOpen = false;
    }
  }
});
