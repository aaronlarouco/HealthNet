function setupPatientFileUpload() {
  var csrf = $('input[name=\"csrfmiddlewaretoken\"]').clone();
  $('#patient-file-upload-form').append(csrf[0]);

  var name = document.getElementById('patient-file-name');
  $("#patient-file-input").change(function(e) {
    var text = $("#patient-file-input").val();
    newText = text.substring(text.lastIndexOf("\\") + 1, text.length);
    name.value = newText;
    document.getElementById("patient-file-label").innerHTML = newText;
  });

  setupAjaxFileUpload();
}

function setupAjaxFileUpload() {
  var userHolder = document.getElementById('peek-username');
  var username = userHolder.getAttribute("username");

  $("#patient-file-upload-form").submit(function() {

    var formData = new FormData($(this)[0]);

    $.ajax({
        url: "/profiles/" + username + "/fileupload",
        type: 'POST',
        data: formData,
        async: true,
        success: function (data) {
          document.getElementById("patient-file-label").innerHTML = "Click to choose a file...";
          $("#patient-file-input").replaceWith($("#patient-file-input").clone(true));

          $("#patient-files").html(data.html);
        },
        cache: false,
        contentType: false,
        processData: false
    });

    return false;
});
}

function setupNewCaseButton() {
  $("#new-case-button").click(function(e) {
    var userHolder = document.getElementById('peek-username');
    var username = userHolder.getAttribute("username");

    $.ajax({
        url: "/profiles/" + username + "/newcase",
        data: {},
        success: function (data) {
            $('#new-case-content').html(data.html);
            setupNewCaseCreate();
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
}

function setupNewCaseCreate() {
  $("#new-case-submit").click(function(e) {
    e.preventDefault();

    var userHolder = document.getElementById('peek-username');
    var username = userHolder.getAttribute("username");

    var csrf = $('input[name=\"csrfmiddlewaretoken\"]').clone();
    $('#new-case-form').append(csrf[0]);

    $.ajax({
        url: "/profiles/" + username + "/newcase",
        type: "POST",
        data: $('#new-case-form').serialize(),
        success: function (data) {
            $('#patient-cases').html(data.html);
            forceCloseJPop();
            setupSaveNotes();
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
}

function setupSaveNotes() {
  $(".case-notes").keyup(function(e) {
    var pk = $(this)[0].getAttribute("pk");
    $("#save-notes-button-" + pk).removeClass("save-notes-disabled");
  });

  $(".save-notes-button").click(function(e) {
    e.preventDefault();

    var userHolder = document.getElementById('peek-username');
    var username = userHolder.getAttribute("username");

    var pk = $(this)[0].getAttribute("pk");

    var csrf = $('input[name=\"csrfmiddlewaretoken\"]').clone();
    $('#case-notes-form-' + pk).append(csrf[0]);

    $.ajax({
        url: "/profiles/" + username + "/savecasenotes/" + pk,
        type: "POST",
        data: $('#case-notes-form-' + pk).serialize(),
        success: function (data) {
          $("#save-notes-button-" + pk).addClass("save-notes-disabled");
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
}
