$(document).ready(function() {
  var calbtn = document.getElementById("calendar-btn");
  var homebtn = document.getElementById("profile-btn");
  var contbtn = document.getElementById("contact-btn");
  var medicalbtn = document.getElementById("medical-btn");
  var messagebtn = document.getElementById("message-btn");
  var notifybtn = document.getElementById("notify-btn");
  var notifynum = document.getElementById("notify-num");
  var calbtnTop = document.getElementById("top-calendar-btn");
  var homebtnTop = document.getElementById("top-profile-btn");
  var contbtnTop = document.getElementById("top-contact-btn");
  var medicalbtnTop = document.getElementById("top-medical-btn");
  var messagebtnTop = document.getElementById("top-message-btn");
  var notifybtnTop = document.getElementById("top-notify-btn");
  var notifynumTop = document.getElementById("top-notify-num");
  var notifyOpen = false;

  var profilePic = document.getElementById("profile-picture");
  var profileInfo = document.getElementById("profile-info-pane");
  var cal = document.getElementById("cal-id");
  var cal2 = document.getElementById("cal2-id");
  var calTools = document.getElementById("cal-tools");
  var today = document.getElementsByClassName("fc-today-button");
  var row = document.getElementById("row-id-1");
  var contacts = document.getElementById("contacts-content");
  var medical = document.getElementById("profile-medical-pane");
  var messages = document.getElementById("profile-messages-pane");
  var messageContacts = document.getElementById("profile-messagecontacts-pane");
  var notifications = document.getElementById("notifications-pane");
  var peek = document.getElementById("peek-row");

  calbtn.addEventListener("click", switchToCalendar);
  homebtn.addEventListener("click", switchToHome);
  contbtn.addEventListener("click", switchToContacts);
  medicalbtn.addEventListener("click", switchToMedical);
  messagebtn.addEventListener("click", switchToMessages);
  notifybtn.addEventListener("click", showNotifications);
  notifynum.addEventListener("click", showNotifications);

  calbtnTop.addEventListener("click", function() {
    switchToCalendar();
    topbarToggle();
  });
  homebtnTop.addEventListener("click", function() {
    switchToHome();
    topbarToggle();
  });
  contbtnTop.addEventListener("click", function() {
    switchToContacts();
    topbarToggle();
  });
  medicalbtnTop.addEventListener("click", function() {
    switchToMedical();
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
    profilePic.classList.add("hide");
    profileInfo.classList.add("hide");
    medical.classList.add("hide");
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

  function switchToHome() {
    peek.classList.add("hide");
    contacts.classList.add("hide");
    row.classList.remove("hide");
    cal.classList.add("hide");
    cal2.classList.add("hide");
    calTools.classList.add("hide");
    medical.classList.add("hide");
    messages.classList.add("hide");
    messageContacts.classList.add("hide");
    profilePic.children[0].classList.remove("animate-from-bottom");
    profilePic.children[0].classList.add("scale-0");
    profilePic.children[0].classList.add("fade-grow-in");
    profilePic.classList.remove("hide");
    profileInfo.children[0].classList.remove("animate-from-bottom");
    profileInfo.children[0].classList.add("scale-0");
    profileInfo.children[0].classList.add("fade-grow-in");
    profileInfo.classList.remove("hide");
  }

  function switchToContacts() {
    peek.classList.add("hide");
    row.classList.add("hide");
    contacts.classList.remove("hide");
    contacts.classList.add("scale-0");
    contacts.classList.add("fade-grow-in");
  }

  function switchToMedical() {
    peek.classList.add("hide");
    contacts.classList.add("hide");
    row.classList.remove("hide");
    row.classList.remove("hide");
    profilePic.classList.add("hide");
    profileInfo.classList.add("hide");
    cal.classList.add("hide");
    cal2.classList.add("hide");
    calTools.classList.add("hide");
    messages.classList.add("hide");
    messageContacts.classList.add("hide");

    medical.children[0].classList.remove("animate-from-bottom");
    medical.children[0].classList.add("scale-0");
    medical.children[0].classList.add("fade-grow-in");
    medical.classList.remove("hide");
  }

  function switchToMessages() {
    peek.classList.add("hide");
    contacts.classList.add("hide");
    row.classList.remove("hide");
    row.classList.remove("hide");
    profilePic.classList.add("hide");
    profileInfo.classList.add("hide");
    cal.classList.add("hide");
    cal2.classList.add("hide");
    calTools.classList.add("hide");
    medical.classList.add("hide");

    messages.children[0].classList.remove("animate-from-bottom");
    messages.children[0].classList.add("scale-0");
    messages.children[0].classList.add("fade-grow-in");
    messages.classList.remove("hide");

    messageContacts.children[0].classList.remove("animate-from-bottom");
    messageContacts.children[0].classList.add("scale-0");
    messageContacts.children[0].classList.add("fade-grow-in");
    messageContacts.classList.remove("hide");

    
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
