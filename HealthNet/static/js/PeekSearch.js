$(document).ready(function () {
    $("#search-input").keyup(function () {
        var text = $('#search-input');
        var token = $('input[name=\"csrfmiddlewaretoken\"]');
        var userHolder = document.getElementById('username-holder');
        var username = userHolder.getAttribute("username");

        $.ajax({
            url: "/profiles/" + username + "/search",
            type: "POST",
            data: {
                client_response: "",
                csrfmiddlewaretoken: token.val(),
                text: text.val()
            },
            success: function (data) {
              $('#search-results').html(data.html);
              setupSearchLinks();
            },
            error: function (jqXHR, textStatus, errorThrown) {
            }
        });
    });
});

function setupSearchLinks() {
  var results = document.getElementsByClassName("search-result-link");
  for (x = 0; x < results.length; x++) {
    results[x].addEventListener('click', function(e) {
      var element = e.target;
      var pk = element.getAttribute("pk");
      var userHolder = document.getElementById('username-holder');
      var username = userHolder.getAttribute("username");
      var token = $('input[name=\"csrfmiddlewaretoken\"]');

      $.ajax({
          url: "/profiles/" + username + "/peek",
          type: "POST",
          data: {
            csrfmiddlewaretoken: token.val(),
            pk: pk
          },
          success: function (data) {
            $('#jpop-faded-bg').click();
            showPeek(data.html);
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }, false);
  }
}

function showPeek(html) {
  var row = document.getElementById("row-id-1");
  row.classList.add("hide");
  $("#contacts-content").addClass("hide");

  $("#peek-row").html(html);

  $("#peek-row .animate-from-bottom").each(function(index) {
    $(this).removeClass("animate-from-bottom");
    $(this).addClass("scale-0");
    $(this).addClass("fade-grow-in");
  });

  $("#peek-row").removeClass("hide");
  initJPopInParent(document.getElementById('peek-row'));

  document.getElementById("profile-body").style.overflow = "hidden";
  setTimeout(function() {
    document.getElementById("profile-body").style.overflow = "auto";
  }, 400);

  var userHolder = document.getElementById('peek-username');
  var username = userHolder.getAttribute("username");
  var account = userHolder.getAttribute("account");

  if (account == 'P') {
    setupPictureUpload();
    setupBasicInfoEditPeek();
    setupPatientFileUpload();
    setupNewCaseButton();
    setupSaveNotes();
  }
  else {
    setupPeekContact();
  }
}

function setupPictureUpload() {
  var token = $('input[name=\"csrfmiddlewaretoken\"]');

  $("#patient-peek-picture #profile-pic-edit-id").click(function(e) {
    $("#ppic-form").append(token[0]);
  });

  var userHolder = document.getElementById('peek-username');
  var username = userHolder.getAttribute("username");

  $("#ppic-form").submit(function() {

    var formData = new FormData($(this)[0]);

    $.ajax({
        url: "/profiles/" + username + "/ajaxpicupload",
        type: 'POST',
        data: formData,
        async: true,
        success: function (data) {
          $("#profile-pic-pic-wrapper").html(data.html);
          $("#jpop-faded-bg").click();
        },
        cache: false,
        contentType: false,
        processData: false
    });

    return false;
});
}

function setupPeekAppointment() {

}

function setupPeekMessage() {

}

function setupPeekContact() {
  $("#staff-peek-contact-link").click(function(e) {
    var userHolder = document.getElementById('username-holder');
    var username = userHolder.getAttribute("username");
    var pk = $("#staff-peek-contact-link")[0].getAttribute("pk");

    $.ajax({
        url: "/profiles/" + username + "/peekcontact/" + pk,
        data: {
        },
        success: function (data) {
          alert("Contact added");
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
}
