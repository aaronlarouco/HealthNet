/**
 * Created by Adam on 12/5/2015.
 */

$(document).ready(function() {
  setupNewMessageScripts();
  setupViewMessageScripts();
});

function setupNewMessageScripts() {

  $("#new-message-button").click(function(e) {
    e.preventDefault();

    var btn = document.getElementById('new-message-button');
    var username = btn.getAttribute("username");

    $.ajax({
        url: "/messaging/" + username + "/newmessage",
        data: {
        },
        success: function (data) {
          $('#new-message-content').html(data.html);
          forceInputSetup(document.getElementById("new-message-content"));
          $('#new-message-content').append("<input id=\"messageinfo\" type=\"hidden\" username=\"" +
          username + "\">");
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#message-send").click(function(e) {
    if ($('#new-message-popup-form')[0].checkValidity() == true) {
      e.preventDefault();
      var hold = document.getElementById('username-holder');
      var username = hold.getAttribute("username");

      $.ajax({
          url: "/messaging/" + username + "/newmessage",
          type: "POST",
          data: $('#new-message-popup-form').serialize(),
          success: function (data) {
            $('#jpop-faded-bg').click();
          },
          error: function (jqXHR, textStatus, errorThrown) {
              alert("Message could not be sent. Please alert your local programmer.")
          }
      });
    }
  });
}

function setupViewMessageScripts() {
    var messages = document.getElementsByClassName("message-view-link");
    for(var x = 0; x < messages.length; x++) {
        messages[x].addEventListener('click', function (e) {
            var element = e.target;
            var pk = element.getAttribute("pk");
            var userHolder = document.getElementById('username-holder');
            var username = userHolder.getAttribute("username");
            var token = $('input[name=\"csrfmiddlewaretoken\"]');
            $.ajax({
                url: "/messaging/" + username + "/viewmessage/" + pk,
                data: {
                },
                success: function (data) {
                    $('#view-message-content').html(data.html);
                    forceInputSetup(document.getElementById("view-message-content"));
                    $("#message-reply").click(function (e) {
                        e.preventDefault();
                        $("#message-reply").addClass("hide");
                        $("#message-send-reply").removeClass("hide");
                        $.ajax({
                            url: "/messaging/" + username + "/reply/" + pk,
                            data: {},
                            success: function (data) {
                                $('#view-message-content').html(data.html);
                                forceInputSetup(document.getElementById("view-message-content"));
                                $("#message-send-reply").click(function(e) {
                                    if ($('#view-message-popup-form')[0].checkValidity() == true) {
                                        e.preventDefault();
                                        $.ajax({
                                            url: "/messaging/" + username + "/reply/" + pk,
                                            type: "POST",
                                            data: $('#view-message-popup-form').serialize(),
                                            success: function (data) {
                                                $('#jpop-faded-bg').click();
                                            },
                                            error: function (jqXHR, textStatus, errorThrown) {
                                                alert("Message could not be sent. Please alert your local programmer.")
                                            }
                                        });
                                    }
                                });

                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                alert("Something went wrong. Please alert your local programmer.")
                            }
                        });
                    });
                },
                error: function (jqXHR, textStatus, errorThrown) {
                }
            });
        });
    }
}
