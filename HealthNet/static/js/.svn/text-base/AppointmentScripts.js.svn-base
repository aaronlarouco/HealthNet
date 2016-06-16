$(document).ready(function () {
  setupDeleteAppointmentYesNo();
  setupCreateAppointmentScripts();
});

function setupCreateAppointmentScripts() {
    var token = $('input[name=\"csrfmiddlewaretoken\"]');

    $("#create-appointment-button").click(function (e) {
        e.preventDefault();

        var userHolder = document.getElementById('username-holder');
        var username = userHolder.getAttribute("username");

        $.ajax({
            url: "/appointments/" + username + "/createappointment",
            data: {},
            success: function (data) {
                $('#create-appointment-content').html(data.html);
                forceInputSetup(document.getElementById("create-appointment-content"));
                initSwagTp("start-time");
                $('#create-appointment-content').append("<input id=\"appointmentinfo\" type=\"hidden\" username=\"" +
                    username + "\">");

                $("#patient-select").click(function(e) {
                  $.ajax({
                      url: "/appointments/" + username + "/updatecases/" + $("#patient-select").val(),
                      data: {
                      },
                      success: function (data) {
                          $('#medical-case-select').html(data.html);
                      },
                      error: function (jqXHR, textStatus, errorThrown) {
                      }
                  });
                });
            },
            error: function (jqXHR, textStatus, errorThrown) {
            }
        });
    });
    $("#create-appointment-submit").click(function (e) {
        if ($('#create-appointment-popup-form')[0].checkValidity() == true) {
            e.preventDefault();

            // var info = document.getElementById('appointmentinfo');
            var userHolder = document.getElementById('username-holder');
            var username = userHolder.getAttribute("username");

            $.ajax({
                url: "/appointments/" + username + "/createappointment",
                type: "POST",
                data: $('#create-appointment-popup-form').serialize(),
                success: function (data) {
                    document.getElementById("maincalendar").innerHTML = "";
                    document.getElementById("daycalendar").innerHTML = "";
                    $('#maincalendar').html(data.maincal);
                    $('#daycalendar').html(data.daycal);

                    forceCloseJPop();
                },
                error: function (jqXHR, textStatus, errorThrown) {
                }
            });
        }
    });
}

function setupEditAppointmentButton() {
  $("#edit-appointment-button").click(function (e) {
      e.preventDefault();

      var info = document.getElementById('appointmentpk');
      var username = info.getAttribute("username");
      var pk = info.getAttribute("pk");

      $.ajax({
          url: "/appointments/" + username + "/" + pk + "/edit",
          data: {},
          success: function (data) {
              $('#view-appointment-content').html(data.html);
              setJpopTitle("view-appointment-popup", "Edit Appointment");
              $('#view-appointment-content').append("<input id=\"appointmentpk\" type=\"hidden\" pk=\"" +
                  pk + "\" username=\"" + username + "\">");
              var csrf = $('input[name=\"csrfmiddlewaretoken\"]').clone();
              $('#edit-appointment-form').append(csrf[0]);
              setupEditAppointmentSubmit();
              forceInputSetup(document.getElementById("view-appointment-content"));
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
  });
}

function setupEditAppointmentSubmit() {
  $("#appointment-edit-submit").click(function (e) {
      if ($('#edit-appointment-form')[0].checkValidity() == true) {
          e.preventDefault();

          var info = document.getElementById('appointmentpk');
          var username = info.getAttribute("username");
          var pk = info.getAttribute("pk");

          $.ajax({
              url: "/appointments/" + username + "/" + pk + "/edit",
              type: "POST",
              data: $('#edit-appointment-form').serialize(),
              success: function (data) {
                  document.getElementById("maincalendar").innerHTML = "";
                  document.getElementById("daycalendar").innerHTML = "";
                  $('#maincalendar').html(data.maincal);
                  $('#daycalendar').html(data.daycal);
                  forceCloseJPop();
              },
              error: function (jqXHR, textStatus, errorThrown) {
              }
          });
      }
  });
}

function setupDeleteAppointmentButton() {
  $("#delete-appointment-button").click(function (e) {
      e.preventDefault();

      forceCloseJPop(document.getElementById("view-appointment-popup"));

      var info = document.getElementById('appointmentpk');
      var username = info.getAttribute("username");
      var pk = info.getAttribute("pk");

      var delInfo = document.getElementById('delete-appointment-info');
      delInfo.setAttribute("username", username);
      delInfo.setAttribute("pk", pk);
  });
}

function setupDeleteAppointmentYesNo() {
  $("#delete-appointment-yes").click(function (e) {
      e.preventDefault();

      var info = document.getElementById('delete-appointment-info');
      var username = info.getAttribute("username");
      var pk = info.getAttribute("pk");

      $.ajax({
          url: "/appointments/" + username + "/" + pk + "/cancel",
          data: {},
          success: function (data) {
              document.getElementById("maincalendar").innerHTML = "";
              document.getElementById("daycalendar").innerHTML = "";
              $('#maincalendar').html(data.maincal);
              $('#daycalendar').html(data.daycal);
              forceCloseJPop();
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
  });

  $("#delete-appointment-no").click(function (e) {
      e.preventDefault();
      forceCloseJPop();
  });
}
