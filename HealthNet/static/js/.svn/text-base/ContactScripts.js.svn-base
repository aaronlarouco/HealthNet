$(document).ready(function() {
  setupChangeContactScripts();
  setupAddContactScripts();
});

function setupAddContactScripts() {
  var token = $('input[name=\"csrfmiddlewaretoken\"]');
  var userHolder = document.getElementById('username-holder');
  var username = userHolder.getAttribute("username");

  $("#add-contact-button").click(function(e) {
    e.preventDefault();

    $.ajax({
        url: "/profiles/" + username + "/addcontact",
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#add-contact-form-content').html(data.html);
          forceInputSetup(document.getElementById("add-contact-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#add-contact-submit").click(function(e) {
    if ($('#add-contact-form')[0].checkValidity() == true) {
      e.preventDefault();

      $.ajax({
          url: "/profiles/" + username + "/addcontact",
          type: "POST",
          data: $('#add-contact-form').serialize(),
          success: function (data) {
            document.getElementById("contact-list").innerHTML = "";
            $('#contact-list').html(data.html);
            setupChangeContactScripts();
            initJPopInParent(document.getElementById('contact-list'));
            $('#jpop-faded-bg').click();
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });
}

function setupChangeContactScripts() {
  var token = $('input[name=\"csrfmiddlewaretoken\"]');

  $(".contact-list-edit-button").click(function(e) {
    e.preventDefault();
    var btn = e.target || e.srcElement;
    var contactId = btn.getAttribute("contactid");
    var username = btn.getAttribute("username");

    $.ajax({
        url: "/profiles/" + username + "/editcontact/" + contactId,
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#edit-contact-form-content').html(data.html);
          $('#edit-contact-form-content').append("<input id=\"editcontacthiddeninfo\" type=\"hidden\" contactid=\"" +
          contactId + "\" username=\"" +
          username + "\">");
          forceInputSetup(document.getElementById("edit-contact-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#edit-contact-submit").click(function(e) {
    if ($('#edit-contact-form')[0].checkValidity() == true) {
      e.preventDefault();

      var info = document.getElementById('editcontacthiddeninfo');
      var contactId = info.getAttribute("contactid");
      var username = info.getAttribute("username");

      $.ajax({
          url: "/profiles/" + username + "/editcontact/" + contactId,
          type: "POST",
          data: $('#edit-contact-form').serialize(),
          success: function (data) {
            document.getElementById("contact-list").innerHTML = "";
            $('#contact-list').html(data.html);
            setupChangeContactScripts();
            initJPopInParent(document.getElementById('contact-list'));
            $('#jpop-faded-bg').click();
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });

  $(".contact-list-delete-button").click(function(e) {
    e.preventDefault();
    var btn = e.target || e.srcElement;
    var contactId = btn.getAttribute("contactid");
    var username = btn.getAttribute("username");

    var info = document.getElementById('contact-delete-info');
    info.setAttribute("username", username);
    info.setAttribute("contactid", contactId);
  });
  $("#delete-contact-yes").click(function(e) {
    e.preventDefault();
    var info = document.getElementById('contact-delete-info');
    var contactId = info.getAttribute("contactid");
    var username = info.getAttribute("username");

    $.ajax({
        url: "/profiles/" + username + "/deletecontact/" + contactId,
        data: {
        },
        success: function (data) {
          $('#contact-list').html(data.html);
          setupChangeContactScripts();
          $('#jpop-faded-bg').click();
          initJPopInParent(document.getElementById('contact-list'));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#delete-contact-no").click(function(e) {
    e.preventDefault();
    $('#jpop-faded-bg').click();
  });
}
